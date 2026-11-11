"""Recipe loading and generation options."""
from __future__ import annotations

import json
import math
from pathlib import Path


def load_recipe(path, kind=None):
    recipe = json.loads(Path(path).read_text())
    if recipe.get("schema_version") != 1:
        raise ValueError("recipe schema_version must be 1")
    if kind is not None and recipe.get("kind") not in kind:
        raise ValueError(f"recipe kind must be one of {kind}")
    return recipe


def model_config(recipe_path, recipe):
    path = Path(recipe_path).resolve().parent.parent / "model.json"
    config = json.loads(path.read_text())
    if config.get("id", recipe["model_id"]) != recipe["model_id"]:
        raise ValueError("recipe model_id does not match model.json")
    return config


def patch_path(recipe_path, recipe):
    return (Path(recipe_path).resolve().parent / recipe["patch"]).resolve()


def sampling_options(sampling):
    temperature = float(sampling["temperature"])
    penalty = float(sampling.get("repetition_penalty", 1.0))
    if not math.isfinite(temperature) or temperature < 0 or not math.isfinite(penalty) or penalty <= 0:
        raise ValueError("temperature must be finite and nonnegative; repetition_penalty must be positive")
    options = {"repetition_penalty": penalty, "do_sample": temperature > 0}
    if temperature > 0:
        options.update(temperature=temperature, top_p=float(sampling["top_p"]), top_k=int(sampling["top_k"]))
    return options
