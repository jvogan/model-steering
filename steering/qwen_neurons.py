"""Generate with prompt-calibrated Qwen3.5-4B neuron interventions."""
from __future__ import annotations

import argparse
import math
from collections.abc import Callable, Sequence
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from torch import Tensor, nn

from .common import load_recipe, model_config


@dataclass(frozen=True)
class SteeringTarget:
    layer: int
    neuron: int
    coefficient: float


@dataclass(frozen=True)
class CalibratedTarget:
    layer: int
    neuron: int
    dose: float
    residual_median: float
    column_norm: float
    alpha: float


def _finite(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


def _index(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def normalize_recipe(recipe: dict) -> tuple[SteeringTarget, ...]:
    if recipe.get("schema_version") != 1 or recipe.get("kind") != "calibrated_neuron_add":
        raise ValueError("expected schema_version 1 and kind calibrated_neuron_add")
    if recipe.get("normalization") != "prompt_residual":
        raise ValueError("normalization must be prompt_residual")
    if recipe.get("timing") != "prompt_and_decode":
        raise ValueError("timing must be prompt_and_decode")
    sampling = recipe.get("sampling", {})
    for name, expected in (("temperature", 0), ("top_p", 1), ("top_k", 0), ("repetition_penalty", 1)):
        if _finite(sampling.get(name), name) != expected:
            raise ValueError(f"{name} must be {expected} for these greedy recipes")
    if sampling.get("enable_thinking") is not False or sampling.get("system"):
        raise ValueError("recipes require a user-only prompt with enable_thinking false")
    if _index(recipe.get("max_new_tokens"), "max_new_tokens") == 0:
        raise ValueError("max_new_tokens must be positive")
    raw_targets = recipe.get("targets")
    if not isinstance(raw_targets, list) or not raw_targets:
        raise ValueError("recipe must contain targets")
    targets = []
    for raw in raw_targets:
        if not isinstance(raw, dict):
            raise ValueError("each target must be an object")
        targets.append(SteeringTarget(
            _index(raw.get("layer"), "layer"),
            _index(raw.get("neuron"), "neuron"),
            _finite(raw.get("coefficient"), "coefficient"),
        ))
    return tuple(targets)


def get_text_layers(model: nn.Module) -> Sequence[nn.Module]:
    base = getattr(model, "model", None)
    if base is None:
        raise ValueError("model has no .model attribute")
    language_model = getattr(base, "language_model", None)
    text_model = language_model if language_model is not None else base
    layers = getattr(text_model, "layers", None)
    if layers is None:
        raise ValueError("could not locate Qwen text decoder layers")
    return layers


def _residual_tensor(output: Any) -> Tensor:
    residual = output[0] if isinstance(output, tuple) else output
    if not isinstance(residual, Tensor) or residual.ndim != 3:
        raise ValueError("decoder layer must return [batch, tokens, hidden]")
    return residual


def residual_median_excluding_first_token(residual: Tensor) -> float:
    if residual.ndim != 3 or residual.shape[0] != 1:
        raise ValueError("calibration expects one unpadded prompt")
    if residual.shape[1] <= 1:
        raise ValueError("calibration prompt must contain at least two tokens")
    norms = torch.linalg.vector_norm(residual[0, 1:].detach().float(), dim=-1)
    if not bool(torch.isfinite(norms).all()) or bool((norms <= 0).any()):
        raise ValueError("calibration produced invalid residual norms")
    # torch.median selects the lower middle value when the token count is even.
    return float(torch.median(norms).cpu())


def collect_residual_medians(
    layers: Sequence[nn.Module], layer_indices: Sequence[int], forward: Callable[[], Any],
) -> dict[int, float]:
    captured: dict[int, float] = {}
    handles: list[Any] = []

    def make_hook(layer: int):
        def hook(_module, _args, output):
            captured[layer] = residual_median_excluding_first_token(_residual_tensor(output))
        return hook

    try:
        for layer in sorted(set(layer_indices)):
            _index(layer, "layer")
            if layer >= len(layers):
                raise ValueError(f"layer {layer} outside 0..{len(layers) - 1}")
            handles.append(layers[layer].register_forward_hook(make_hook(layer)))
        forward()
    finally:
        for handle in handles:
            handle.remove()
    missing = sorted(set(layer_indices) - set(captured))
    if missing:
        raise RuntimeError(f"calibration hooks did not fire for layers {missing}")
    return captured


def _down_proj(layers: Sequence[nn.Module], target: SteeringTarget | CalibratedTarget):
    _index(target.layer, "layer")
    _index(target.neuron, "neuron")
    if target.layer >= len(layers):
        raise ValueError(f"layer {target.layer} outside 0..{len(layers) - 1}")
    down_proj = layers[target.layer].mlp.down_proj
    if down_proj.weight.ndim != 2:
        raise ValueError("down_proj weight must be a matrix")
    if target.neuron >= down_proj.weight.shape[1]:
        raise ValueError(f"neuron {target.neuron} outside down_proj width")
    return down_proj


def calibrate_targets(
    layers: Sequence[nn.Module], targets: Sequence[SteeringTarget],
    residual_medians: dict[int, float], scale: float,
) -> tuple[CalibratedTarget, ...]:
    scale = _finite(scale, "scale")
    if scale < 0:
        raise ValueError("scale must be nonnegative")
    calibrated = []
    for target in targets:
        weight = _down_proj(layers, target).weight
        column_norm = float(torch.linalg.vector_norm(weight[:, target.neuron].detach().float()).cpu())
        if not math.isfinite(column_norm) or column_norm <= 0:
            raise ValueError("down_proj column norm must be finite and positive")
        residual_median = _finite(residual_medians[target.layer], "residual median")
        if residual_median <= 0:
            raise ValueError("residual median must be positive")
        dose = scale * _finite(target.coefficient, "coefficient")
        alpha = dose * residual_median / column_norm
        if not math.isfinite(alpha):
            raise ValueError("calibrated alpha must be finite")
        calibrated.append(CalibratedTarget(target.layer, target.neuron, dose, residual_median, column_norm, alpha))
    return tuple(calibrated)


class SteeringHooks:
    """Add fixed, calibrated values to every down-projection input token."""

    def __init__(self, layers: Sequence[nn.Module], targets: Sequence[CalibratedTarget]):
        self.layers, self.targets = layers, targets
        self.handles: list[Any] = []
        self.call_shapes: dict[int, list[tuple[int, ...]]] = {}

    def _make_hook(self, target: CalibratedTarget):
        def hook(_module, args):
            activation = args[0]
            if not isinstance(activation, Tensor) or activation.ndim != 3 or activation.shape[0] != 1:
                raise ValueError("down_proj input must be [1, tokens, neurons]")
            if target.neuron >= activation.shape[-1]:
                raise ValueError("steering neuron is outside live activation width")
            self.call_shapes.setdefault(target.layer, []).append(tuple(activation.shape))
            changed = activation.clone()
            # Cast before adding to preserve the reference's BF16 rounding order.
            changed[..., target.neuron] += changed.new_tensor(target.alpha)
            return (changed, *args[1:])
        return hook

    def __enter__(self):
        if self.handles:
            raise RuntimeError("steering hooks are already installed")
        modules = []
        for target in self.targets:
            module = _down_proj(self.layers, target)
            _finite(target.alpha, "alpha")
            modules.append(module)
        try:
            for module, target in zip(modules, self.targets, strict=True):
                if target.alpha != 0:
                    self.handles.append(module.register_forward_pre_hook(self._make_hook(target)))
        except BaseException:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, exc_type, exc, traceback):
        for handle in self.handles:
            handle.remove()
        self.handles.clear()


def generate(model, tokenizer, recipe, prompt, *, scale=1.0, seed=42, max_new_tokens=None):
    targets = normalize_recipe(recipe)
    scale = _finite(scale, "scale")
    if scale < 0:
        raise ValueError("scale must be nonnegative")
    count = recipe["max_new_tokens"] if max_new_tokens is None else max_new_tokens
    if _index(count, "max_new_tokens") == 0:
        raise ValueError("max_new_tokens must be positive")
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False,
        add_generation_prompt=True, enable_thinking=False,
    )
    encoded = tokenizer(text, return_tensors="pt", add_special_tokens=False)
    inputs = {key: value.to(model.device) for key, value in encoded.items()}
    ids = inputs["input_ids"]
    if ids.ndim != 2 or ids.shape[0] != 1 or ids.shape[1] < 2:
        raise ValueError("generation expects one prompt with at least two tokens")
    if "attention_mask" in inputs and not bool((inputs["attention_mask"] == 1).all()):
        raise ValueError("calibration expects an unpadded prompt")
    layers = get_text_layers(model)
    for target in targets:
        _down_proj(layers, target)
    with torch.inference_mode():
        hooks = nullcontext()
        if scale != 0:
            medians = collect_residual_medians(
                layers, [target.layer for target in targets],
                lambda: model(**inputs, use_cache=False, logits_to_keep=1),
            )
            hooks = SteeringHooks(layers, calibrate_targets(layers, targets, medians, scale))
        torch.manual_seed(seed)
        with hooks:
            output = model.generate(
                **{key: value.clone() for key, value in inputs.items()},
                # A dynamic cache is constructed per call, including hybrid linear-attention state.
                past_key_values=None, cache_implementation="dynamic", use_cache=True, do_sample=False,
                temperature=1.0, top_p=1.0, top_k=0, repetition_penalty=1.0,
                num_beams=1, num_return_sequences=1,
                max_new_tokens=count, pad_token_id=tokenizer.eos_token_id,
            )
    return tokenizer.decode(output[0, ids.shape[1]:], skip_special_tokens=True).strip()


def compare(model, tokenizer, recipe, prompt, *, scale=1.0, seed=42, max_new_tokens=None):
    options = {"seed": seed, "max_new_tokens": max_new_tokens}
    return {
        "baseline": generate(model, tokenizer, recipe, prompt, scale=0, **options),
        "steered": generate(model, tokenizer, recipe, prompt, scale=scale, **options),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", help="existing local snapshot; defaults to the pinned Hub revision")
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-new-tokens", type=int)
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args()
    recipe = load_recipe(args.recipe, {"calibrated_neuron_add"})
    normalize_recipe(recipe)
    if not math.isfinite(args.scale) or args.scale < 0:
        parser.error("--scale must be finite and nonnegative")
    if args.max_new_tokens is not None and args.max_new_tokens <= 0:
        parser.error("--max-new-tokens must be positive")
    metadata = model_config(args.recipe, recipe)
    if metadata["hub_id"] != "Qwen/Qwen3.5-4B" or not metadata.get("revision"):
        raise ValueError("recipe must identify a pinned Qwen/Qwen3.5-4B model")
    if args.model and not Path(args.model).is_dir():
        parser.error("--model must be an existing local snapshot directory")
    if not torch.cuda.is_available():
        raise RuntimeError("Qwen3.5-4B generation requires a CUDA GPU")
    from transformers import AutoModelForImageTextToText, AutoTokenizer

    location = args.model or metadata["hub_id"]
    source_options = {"local_files_only": True} if args.model else {"revision": metadata["revision"]}
    tokenizer = AutoTokenizer.from_pretrained(location, **source_options)
    model = AutoModelForImageTextToText.from_pretrained(
        location, dtype=torch.bfloat16, device_map="cuda", **source_options,
    )
    model.eval().requires_grad_(False)
    layers = get_text_layers(model)
    if len(layers) != 32 or any(tuple(layer.mlp.down_proj.weight.shape) != (2560, 9216) for layer in layers):
        raise ValueError("model does not match Qwen3.5-4B dimensions (32, 2560, 9216)")
    options = {"scale": args.scale, "seed": args.seed, "max_new_tokens": args.max_new_tokens}
    if args.compare:
        outputs = compare(model, tokenizer, recipe, args.prompt, **options)
        print(f"Baseline:\n{outputs['baseline']}\n\nSteered:\n{outputs['steered']}")
    else:
        print(generate(model, tokenizer, recipe, args.prompt, **options))


if __name__ == "__main__":
    main()
