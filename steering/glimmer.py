"""Run a Muse Glimmer recipe with request-local token masks."""
from __future__ import annotations

import argparse
import math
import re

import torch

from .common import load_recipe, model_config, patch_path, sampling_options
from .hooks import NeuronSteering, normalize_specs
from .patches import apply_bias_patch
from .tracking import LineTracker


def final_text(raw):
    protocol = "<|start|>assistant" + raw
    channels = re.findall(r"<\|start\|>assistant(?:\s+to=([^<\s]+))?<\|message\|>(.*?)(?=<\|(?:eom|eot|start)\|>|$)", protocol, re.DOTALL)
    if not channels and "<|" not in raw and not raw.lstrip().startswith("to="):
        return raw.strip()
    return "\n\n".join(body.strip() for recipient, body in channels if recipient in ("", "user"))


def generate(model, tokenizer, recipe, prompt, *, scale=1.0, seed=42, max_new_tokens=None):
    sampling = recipe["sampling"]
    messages = ([{"role": "system", "content": sampling["system"]}] if sampling.get("system") else [])
    messages.append({"role": "user", "content": prompt})
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                              reasoning_strength=sampling["reasoning_strength"])
    layers = model.model.language_model.layers
    device = layers[0].mlp.down_proj.weight.device
    encoded = tokenizer(rendered, return_tensors="pt", add_special_tokens=False)
    encoded = {key: value.to(device) for key, value in encoded.items()}
    specs = normalize_specs(recipe.get("interventions", []), layers, scale) if recipe["kind"] == "neuron_add" else []
    tags = {name: tokenizer.convert_tokens_to_ids(token) for name, token in (
        ("start", "<|start|>"), ("message", "<|message|>"), ("eom", "<|eom|>"), ("eot", "<|eot|>"))}
    if any(value is None or value == tokenizer.unk_token_id for value in tags.values()) or len(set(tags.values())) != 4:
        raise ValueError("tokenizer is missing the four ATEM tags")
    special = set(tokenizer.all_special_ids) | set(tags.values()) | {
        index for index, token in getattr(tokenizer, "added_tokens_decoder", {}).items() if token.special}
    lines = recipe.get("skip_lines")
    if lines is not None and (isinstance(lines, bool) or not isinstance(lines, int) or lines < 0):
        raise ValueError("skip_lines must be a nonnegative integer")
    if lines is not None and any(not spec["skip_special"] for spec in specs):
        raise ValueError("skip_lines requires skip_special on every intervention")
    newlines = frozenset(i for i in range(len(tokenizer)) if i not in special and "\n" in tokenizer.decode([i])) if lines is not None and specs else frozenset()
    tracker = LineTracker(special, tags, lambda ids: tokenizer.decode(ids, skip_special_tokens=False),
                          encoded.get("attention_mask"), int(sampling.get("skip_special_after", 0)),
                          lines=[lines] if lines is not None else None, newlines=newlines)
    count = recipe["max_new_tokens"] if max_new_tokens is None else max_new_tokens
    if count <= 0:
        raise ValueError("max_new_tokens must be positive")
    torch.manual_seed(seed)
    with torch.inference_mode(), NeuronSteering(layers, specs, tracker, model.model.language_model.embed_tokens):
        output = model.generate(**encoded, max_new_tokens=count, use_cache=True, logits_to_keep=1,
                                cache_implementation="static", disable_compile=True,
                                pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
                                **sampling_options(sampling))
    if specs and scale != 0 and tracker.forwards == 0:
        raise RuntimeError("token tracker observed no model forwards")
    ids = output[0, encoded["input_ids"].shape[1]:].tolist()
    eos = model.generation_config.eos_token_id
    stops = set(eos if isinstance(eos, list) else [eos]) | {tokenizer.eos_token_id}
    ids = ids[:next((i for i, token in enumerate(ids) if token in stops), len(ids))]
    return final_text(tokenizer.decode(ids, skip_special_tokens=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-new-tokens", type=int)
    parser.add_argument("--compare", action="store_true", help="print baseline and steered answers with the same seed")
    args = parser.parse_args()
    if not math.isfinite(args.scale):
        parser.error("--scale must be finite")
    if args.max_new_tokens is not None and args.max_new_tokens <= 0:
        parser.error("--max-new-tokens must be positive")
    recipe = load_recipe(args.recipe, {"neuron_add", "bias_patch"})
    config = model_config(args.recipe, recipe)
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("Glimmer generation requires a CUDA GPU with BF16 support")
    from transformers import AutoModelForImageTextToText, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(config["hub_id"], revision=config["revision"])
    model = AutoModelForImageTextToText.from_pretrained(config["hub_id"], revision=config["revision"],
        dtype=torch.bfloat16, device_map={"": "cuda:0"}, low_cpu_mem_usage=True, attn_implementation="sdpa")
    model.eval().requires_grad_(False)
    decoder = model.model.language_model.layers
    geometry = config["architecture"]
    if len(decoder) != geometry["num_layers"] or tuple(decoder[0].mlp.down_proj.weight.shape) != (
        geometry["hidden_size"], geometry["intermediate_size"]
    ):
        raise ValueError("loaded Glimmer decoder dimensions differ from model.json")
    options = {"seed": args.seed, "max_new_tokens": args.max_new_tokens}
    if args.compare:
        print("Baseline\n" + generate(model, tokenizer, recipe, args.prompt, scale=0, **options) + "\n\nSteered")
    if recipe["kind"] == "bias_patch":
        apply_bias_patch(model, patch_path(args.recipe, recipe), args.scale)
    print(generate(model, tokenizer, recipe, args.prompt, scale=args.scale, **options))


if __name__ == "__main__":
    main()
