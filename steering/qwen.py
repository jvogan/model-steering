"""Apply Qwen checkpoint patches and generate text with thinking disabled."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch

from .common import load_recipe, patch_path, sampling_options
from .patches import rebuild_checkpoint


class PresencePenalty:
    """Subtract a fixed penalty from tokens already generated in this reply."""

    def __init__(self, penalty, prompt_length):
        if not math.isfinite(penalty):
            raise ValueError("presence_penalty must be finite")
        self.penalty, self.prompt_length = penalty, prompt_length

    def __call__(self, input_ids, scores):
        scores = scores.clone()
        for row, ids in enumerate(input_ids[:, self.prompt_length:]):
            scores[row, ids.unique()] -= self.penalty
        return scores


def generate(model, tokenizer, recipe, prompt, *, seed=42, max_new_tokens=None):
    from transformers import LogitsProcessorList

    sampling = recipe["sampling"]
    messages = ([{"role": "system", "content": sampling["system"]}] if sampling.get("system") else [])
    messages.append({"role": "user", "content": prompt})
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    encoded = tokenizer(text, return_tensors="pt", add_special_tokens=False).to(model.device)
    count = recipe["max_new_tokens"] if max_new_tokens is None else max_new_tokens
    if count <= 0:
        raise ValueError("max_new_tokens must be positive")
    options = sampling_options(sampling)
    options["logits_processor"] = LogitsProcessorList([PresencePenalty(
        float(sampling.get("presence_penalty", 0)), encoded["input_ids"].shape[1])])
    torch.manual_seed(seed)
    with torch.inference_mode():
        output = model.generate(**encoded, max_new_tokens=count, **options)
    return tokenizer.decode(output[0, encoded["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    apply = sub.add_parser("apply", help="rebuild a checkpoint from a numeric patch")
    apply.add_argument("--stock", required=True)
    apply.add_argument("--recipe", required=True)
    apply.add_argument("--out", required=True)
    apply.add_argument("--scale", type=float, default=1.0)
    generate_parser = sub.add_parser("generate", help="generate with thinking disabled")
    generate_parser.add_argument("--model", required=True)
    generate_parser.add_argument("--recipe", help="override the recipe saved in the patched checkpoint")
    generate_parser.add_argument("--prompt", required=True)
    generate_parser.add_argument("--max-new-tokens", type=int)
    generate_parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.command == "apply":
        recipe = load_recipe(args.recipe, {"weight_patch"})
        count = rebuild_checkpoint(args.stock, patch_path(args.recipe, recipe), args.out, args.scale)
        (Path(args.out) / "steering_recipe.json").write_text(json.dumps(recipe, indent=2) + "\n")
        print(f"Patched {count} tensors: {args.out}")
        return
    if args.max_new_tokens is not None and args.max_new_tokens <= 0:
        parser.error("--max-new-tokens must be positive")
    from transformers import AutoModelForImageTextToText, AutoTokenizer

    recipe = load_recipe(args.recipe or Path(args.model) / "steering_recipe.json", {"weight_patch"})
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=torch.bfloat16, device_map="auto")
    model.eval().requires_grad_(False)
    print(generate(model, tokenizer, recipe, args.prompt,
                                seed=args.seed, max_new_tokens=args.max_new_tokens))


if __name__ == "__main__":
    main()
