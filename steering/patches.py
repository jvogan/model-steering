"""Validate and rebuild safetensors checkpoints one shard at a time."""
from __future__ import annotations

import json
import math
import shutil
import tempfile
from pathlib import Path

import numpy as np
import torch
from safetensors import safe_open
from safetensors.torch import load_file, save_file

SIDECARS = frozenset({
    "config.json", "generation_config.json", "tokenizer.json", "tokenizer_config.json",
    "special_tokens_map.json", "added_tokens.json", "vocab.json", "merges.txt", "tokenizer.model",
    "chat_template.jinja", "preprocessor_config.json", "processor_config.json", "video_preprocessor_config.json",
})


def load_patch(path):
    with np.load(path, allow_pickle=False) as data:
        patch = {key: np.asarray(data[key]) for key in data.files}
    if not patch:
        raise ValueError("patch contains no arrays")
    for key, array in patch.items():
        name, sep, operation = key.rpartition("|")
        if not sep or not name or operation not in {"rowadd", "outer_v", "outer_a"}:
            raise ValueError(f"unsupported patch key: {key}")
        if array.ndim != 1 or array.dtype.kind not in "fiu" or not np.isfinite(array).all():
            raise ValueError(f"patch array must be a finite numeric vector: {key}")
        if not np.isfinite(array.astype(np.float32)).all():
            raise ValueError(f"patch array exceeds float32 range: {key}")
    targets = {key.rpartition("|")[0] for key in patch}
    for name in targets:
        if (f"{name}|outer_v" in patch) != (f"{name}|outer_a" in patch):
            raise ValueError(f"outer_v and outer_a must occur together: {name}")
    return patch


def validate_target(name, shape, patch):
    if len(shape) != 2:
        raise ValueError(f"patch target must be a matrix: {name}")
    for operation, size in (("rowadd", shape[1]), ("outer_v", shape[0]), ("outer_a", shape[1])):
        key = f"{name}|{operation}"
        if key in patch and patch[key].shape != (size,):
            raise ValueError(f"{key} needs shape {(size,)}, received {patch[key].shape}")


def apply_to_tensor(name, tensor, patch, scale=1.0):
    validate_target(name, tensor.shape, patch)
    if not tensor.is_floating_point() or not math.isfinite(scale):
        raise ValueError("patch targets must be floating tensors and scale must be finite")
    if scale == 0:
        return tensor
    edited = tensor.float()
    if f"{name}|rowadd" in patch:
        edited = edited + torch.from_numpy(patch[f"{name}|rowadd"]).float()[None, :] * scale
    if f"{name}|outer_v" in patch:
        v = torch.from_numpy(patch[f"{name}|outer_v"]).float()
        a = torch.from_numpy(patch[f"{name}|outer_a"]).float()
        edited = edited + torch.outer(v, a) * scale
    edited = edited.to(tensor.dtype)
    if not bool(torch.isfinite(edited).all()):
        raise ValueError(f"patch produced nonfinite values: {name}")
    return edited


def rebuild_checkpoint(stock, patch_path, out, scale=1.0):
    stock, out = Path(stock), Path(out)
    if out.exists():
        raise FileExistsError(f"output directory already exists: {out}")
    if not math.isfinite(scale):
        raise ValueError("scale must be finite")
    patch = load_patch(patch_path)
    targets = {key.rpartition("|")[0] for key in patch}
    index_path = stock / "model.safetensors.index.json"
    index = json.loads(index_path.read_text()) if index_path.is_file() else None
    if index is not None:
        shard_names = sorted(set(index["weight_map"].values()))
    elif (stock / "model.safetensors").is_file():
        shard_names = ["model.safetensors"]
    else:
        raise ValueError("stock needs model.safetensors or model.safetensors.index.json")
    names = {}
    metadata = {}
    for filename in shard_names:
        if Path(filename).name != filename or not filename.endswith(".safetensors"):
            raise ValueError("checkpoint index contains an invalid shard filename")
        with safe_open(stock / filename, framework="pt", device="cpu") as source:
            metadata[filename] = source.metadata()
            for name in source.keys():
                if name in names:
                    raise ValueError(f"duplicate tensor: {name}")
                names[name] = filename
                if name in targets:
                    validate_target(name, source.get_slice(name).get_shape(), patch)
    if index is not None and names != index["weight_map"]:
        raise ValueError("checkpoint tensor index does not match its shards")
    if targets - names.keys():
        raise ValueError(f"patch targets missing from checkpoint: {sorted(targets - names.keys())}")
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{out.name}-", dir=out.parent))
    try:
        for filename in shard_names:
            tensors = load_file(stock / filename)
            for name in targets.intersection(tensors):
                tensors[name] = apply_to_tensor(name, tensors[name], patch, scale)
            save_file(tensors, temporary / filename, metadata=metadata[filename])
            del tensors
        for filename in SIDECARS:
            source = stock / filename
            if source.is_file():
                shutil.copyfile(source, temporary / filename)
        if index is not None:
            (temporary / index_path.name).write_text(json.dumps(index, indent=2) + "\n")
        if out.exists():
            raise FileExistsError(f"output directory already exists: {out}")
        temporary.rename(out)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return len(targets)


def apply_bias_patch(model, path, scale=1.0):
    """Add exported down-projection biases to the loaded Glimmer model."""
    if not math.isfinite(scale):
        raise ValueError("scale must be finite")
    tensors = load_file(path)
    if not tensors:
        raise ValueError("bias patch contains no tensors")
    updates = []
    for name, value in tensors.items():
        prefix, separator, suffix = name.rpartition(".")
        if not separator or suffix != "bias" or not prefix.endswith(".mlp.down_proj"):
            raise ValueError(f"unsupported bias target: {name}")
        module = model.get_submodule(prefix)
        if value.shape != (module.weight.shape[0],) or not bool(torch.isfinite(value).all()):
            raise ValueError(f"bias patch has an invalid shape or nonfinite values: {name}")
        if module.bias is not None and module.bias.shape != value.shape:
            raise ValueError(f"existing bias shape differs: {name}")
        base = torch.zeros_like(value, device=module.weight.device, dtype=torch.float32) if module.bias is None else module.bias.float()
        edited = (base + value.to(base.device).float() * scale).to(module.weight.dtype)
        if not bool(torch.isfinite(edited).all()):
            raise ValueError(f"bias patch produced nonfinite values: {name}")
        updates.append((module, edited))
    if scale:
        for module, value in updates:
            module.bias = torch.nn.Parameter(value, requires_grad=False)
