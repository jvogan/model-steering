"""Check recipes, patch contents, file links, and distributable files."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "dist", "outputs", "checkpoints", "build"}
PATTERNS = {
    "home directory": rb"/(?:Users|home)/[A-Za-z0-9_.-]+/",
    "mounted volume": rb"/(?:Volumes|mnt)/[A-Za-z0-9_.-]+/",
    "temporary directory": rb"/(?:private/(?:var|tmp)|var/folders)/",
    "email address": rb"\b[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "access token": rb"\b(?:sk-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
    "private key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "account endpoint": rb"https?://[^\s\"'<>]+\.(?:modal\.run|ngrok\.app)",
    "local endpoint": rb"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)(?::\d+)?\b",
    "local file URL": rb"file:" + rb"///",
}
SECRET_NAMES = re.compile(r"^(?:\.env(?:\..*)?|id_(?:rsa|ed25519)|credentials(?:\..*)?|.*\.(?:pem|key))$", re.I)


def release_files(root: Path = ROOT) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED or part.endswith(".egg-info") for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"{relative}: replace the symbolic link with a file")
        if path.is_file() and path.name != ".DS_Store" and path.suffix not in {".pyc", ".pyo"}:
            files.append(path)
    return files


def privacy_payload(path: Path, data: bytes) -> bytes:
    """Scan PNG metadata; compressed pixel bytes are not text."""
    if path.suffix.lower() != ".png":
        return data
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("PNG file has an invalid signature")
    parts, position = [], 8
    while position + 12 <= len(data):
        length = struct.unpack(">I", data[position:position + 4])[0]
        kind = data[position + 4:position + 8]
        end = position + 8 + length
        if end + 4 > len(data):
            raise ValueError("PNG file has a truncated chunk")
        chunk = data[position + 8:end]
        if kind in {b"tEXt", b"eXIf"}:
            parts.append(chunk)
        elif kind in {b"zTXt", b"iCCP"}:
            keyword, remainder = chunk.split(b"\0", 1)
            if not remainder or remainder[0] != 0:
                raise ValueError("PNG metadata uses an unknown compression method")
            parts.extend((keyword, zlib.decompress(remainder[1:])))
        elif kind == b"iTXt":
            keyword, remainder = chunk.split(b"\0", 1)
            flag, method = remainder[:2]
            language, translated, value = remainder[2:].split(b"\0", 2)
            if flag not in (0, 1) or method != 0:
                raise ValueError("PNG text uses an unknown compression method")
            parts.extend((keyword, language, translated, zlib.decompress(value) if flag else value))
        elif kind not in {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM", b"sRGB", b"sBIT", b"bKGD", b"hIST", b"pHYs", b"sPLT", b"tIME"}:
            parts.append(chunk)
        position = end + 4
        if kind == b"IEND":
            parts.append(data[position:])
            return b"\n".join(parts)
    raise ValueError("PNG file has no IEND chunk")


def inside(base: Path, value: str, root: Path) -> Path:
    target = (base / value).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("file reference leaves the repository")
    if not target.is_file():
        raise ValueError(f"missing file reference: {value}")
    return target


def numeric_npy(data: bytes) -> tuple[tuple[int, ...], str]:
    if data[:6] != b"\x93NUMPY":
        raise ValueError("patch member is not a NumPy array")
    version = data[6]
    offset = 10 if version == 1 else 12
    length = int.from_bytes(data[8:offset], "little")
    header = ast.literal_eval(data[offset:offset + length].decode("latin1").strip())
    dtype, shape = header["descr"], header["shape"]
    if dtype not in {"<f4", ">f4", "=f4"} or len(shape) != 1:
        raise ValueError("patch arrays must be one-dimensional float32 vectors")
    values = data[offset + length:]
    if len(values) != math.prod(shape) * 4:
        raise ValueError("patch array length differs from its shape")
    endian = ">" if dtype.startswith(">") else "<"
    if not all(math.isfinite(value[0]) for value in struct.iter_unpack(endian + "f", values)):
        raise ValueError("patch contains a nonfinite value")
    return shape, dtype


def check_patch(path: Path) -> int:
    if path.suffix == ".npz":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if not names or len(names) != len(set(names)):
                raise ValueError("patch must contain unique numeric arrays")
            for member in names:
                if not re.fullmatch(r"model\.language_model\.(?:embed_tokens|layers\.\d+\.mlp\.down_proj)\.weight\|(?:rowadd|outer_v|outer_a)\.npy", member):
                    raise ValueError("patch contains an unexpected member")
                numeric_npy(archive.read(member))
            targets = {name.removesuffix(".npy") for name in names}
            for key in targets:
                if "|outer_" in key:
                    stem = key.rsplit("|", 1)[0]
                    if {stem + "|outer_v", stem + "|outer_a"} - targets:
                        raise ValueError("rank-one patch is missing a vector")
            return len(names)
    if path.suffix == ".safetensors":
        data = path.read_bytes()
        length = struct.unpack("<Q", data[:8])[0]
        header = json.loads(data[8:8 + length])
        count = 0
        intervals = []
        for key, value in header.items():
            if key == "__metadata__":
                continue
            if not re.fullmatch(r"model\.language_model\.layers\.\d+\.mlp\.down_proj\.bias", key):
                raise ValueError("bias patch contains an unexpected tensor")
            if value["dtype"] != "F32" or value["shape"] != [6656]:
                raise ValueError("bias patch has an unexpected shape or dtype")
            start, end = value["data_offsets"]
            if not (0 <= start < end <= len(data) - 8 - length) or end - start != 6656 * 4:
                raise ValueError("bias patch has invalid tensor offsets")
            values = data[8 + length + start:8 + length + end]
            if not all(math.isfinite(v[0]) for v in struct.iter_unpack("<f", values)):
                raise ValueError("bias patch contains a nonfinite value")
            intervals.append((start, end))
            count += 1
        cursor = 0
        for start, end in sorted(intervals):
            if start != cursor:
                raise ValueError("bias patch contains unaccounted bytes")
            cursor = end
        if not count or cursor != len(data) - 8 - length:
            raise ValueError("bias patch contains unaccounted bytes")
        return count
    raise ValueError("patch must use npz or safetensors")


def check_recipe(path: Path, root: Path) -> None:
    recipe = json.loads(path.read_text())
    for key in ("schema_version", "id", "title", "model_id", "kind", "description", "sampling", "max_new_tokens"):
        if key not in recipe:
            raise ValueError(f"recipe is missing {key}")
    if recipe["schema_version"] != 1 or recipe["id"] != path.stem:
        raise ValueError("recipe version or filename differs from its id")
    model = json.loads((path.parent.parent / "model.json").read_text())
    if recipe["model_id"] != model["id"]:
        raise ValueError("recipe model_id differs from model.json")
    if not isinstance(recipe["max_new_tokens"], int) or recipe["max_new_tokens"] <= 0:
        raise ValueError("max_new_tokens must be a positive integer")
    if recipe["kind"] in {"weight_patch", "bias_patch"}:
        check_patch(inside(path.parent, recipe["patch"], root))
        return
    architecture = model.get("architecture", {})
    layers, width = architecture.get("num_layers"), architecture.get("intermediate_size")
    if not isinstance(layers, int) or not isinstance(width, int) or layers <= 0 or width <= 0:
        raise ValueError("neuron recipes need model layer count and intermediate size")
    if recipe["kind"] == "calibrated_neuron_add":
        if recipe.get("normalization") != "prompt_residual":
            raise ValueError("calibrated recipes need prompt_residual normalization")
        if recipe.get("timing") != "prompt_and_decode" or not recipe.get("targets"):
            raise ValueError("calibrated recipes need prompt_and_decode targets")
        seen = set()
        for target in recipe["targets"]:
            layer, neuron, coefficient = target["layer"], target["neuron"], target["coefficient"]
            if type(layer) is not int or not 0 <= layer < layers:
                raise ValueError("target layer is outside the model decoder")
            if type(neuron) is not int or not 0 <= neuron < width:
                raise ValueError("target neuron is outside the model width")
            if type(coefficient) not in (int, float) or not math.isfinite(coefficient):
                raise ValueError("target coefficient must be finite")
            if (layer, neuron) in seen:
                raise ValueError("target coordinates must be distinct")
            seen.add((layer, neuron))
        return
    if recipe["kind"] != "neuron_add" or not recipe.get("interventions"):
        raise ValueError("recipe needs neuron_add interventions, calibrated targets, or a patch")
    for spec in recipe["interventions"]:
        if spec["type"] != "neuron_add":
            raise ValueError("expected a neuron_add intervention")
        if type(spec["layer"]) is not int or not 0 <= spec["layer"] < layers:
            raise ValueError("layer is outside the model decoder")
        neurons, values = spec["neurons"], spec["values"]
        if not neurons or len(neurons) != len(set(neurons)) or any(type(n) is not int or not 0 <= n < width for n in neurons):
            raise ValueError("neuron indices must be unique and within the model width")
        if len(values) != len(neurons) or any(type(v) not in (float, int) or not math.isfinite(v) for v in values):
            raise ValueError("each neuron needs one finite value")
        if spec.get("positions", "all") not in {"all", "prompt", "decode", "reasoning", "final"}:
            raise ValueError("unknown positions setting")
        schedule = spec.get("schedule", {"type": "constant"})
        if schedule["type"] not in {"constant", "cosine", "until_phrase"}:
            raise ValueError("unknown schedule")
        if schedule["type"] == "cosine":
            if schedule.get("period", 24) <= 0 or schedule.get("ramp", 1) <= 0:
                raise ValueError("cosine period and ramp must be positive")
            if schedule.get("anchor", "final_header") not in {"decode_start", "final_header"}:
                raise ValueError("unknown cosine anchor")
        if schedule["type"] == "until_phrase" and not schedule.get("phrase"):
            raise ValueError("until_phrase needs a phrase")
    if "skip_lines" in recipe and (type(recipe["skip_lines"]) is not int or recipe["skip_lines"] < 0):
        raise ValueError("skip_lines must be a nonnegative integer")


def example_records(value, recipe_id=None):
    if isinstance(value, list):
        for item in value:
            yield from example_records(item, recipe_id)
    elif isinstance(value, dict):
        recipe_id = value.get("recipe_id", value.get("recipe", recipe_id))
        prompt = value.get("prompt")
        response = value.get("final_text", value.get("response", value.get("steered")))
        if isinstance(recipe_id, str) and isinstance(prompt, str) and isinstance(response, str):
            if not prompt.strip() or not response.strip():
                raise ValueError("example prompt and response must be nonempty")
            digest = value.get("final_text_sha256")
            if digest and hashlib.sha256(response.encode()).hexdigest() != digest:
                raise ValueError("example response differs from its saved hash")
            yield recipe_id
        if "examples" in value:
            yield from example_records(value["examples"], recipe_id)


def check(root: Path = ROOT, hashes: bool = True) -> tuple[list[str], list[Path]]:
    errors = []
    files = release_files(root)
    for path in files:
        relative = path.relative_to(root).as_posix()
        if SECRET_NAMES.fullmatch(path.name):
            errors.append(f"{relative}: credential filename")
        try:
            payload = privacy_payload(path, path.read_bytes())
        except (ValueError, IndexError, zlib.error) as exc:
            errors.append(f"{relative}: {exc}")
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, payload):
                errors.append(f"{relative}: {label}")
        if path.suffix == ".md":
            for destination in re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)", path.read_text()):
                destination = destination.strip("<>").split("#", 1)[0]
                if destination and not re.match(r"[a-z]+:", destination):
                    try:
                        inside(path.parent, destination, root)
                    except ValueError as exc:
                        errors.append(f"{relative}: {exc}")
    recipes = sorted((root / "models").glob("*/recipes/*.json"))
    if not recipes:
        errors.append("models: no recipe files")
    for path in recipes:
        try:
            check_recipe(path, root)
        except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    for path in sorted((root / "models").glob("*/model.json")):
        relative = path.relative_to(root)
        try:
            model = json.loads(path.read_text())
            if model["schema_version"] != 1 or model["id"] != path.parent.name:
                raise ValueError("model id differs from its directory")
            if not re.fullmatch(r"[0-9a-f]{40}", model["revision"]):
                raise ValueError("model revision must be a full commit")
            declared = [inside(path.parent, entry, root) for entry in model["recipes"]]
            discovered = sorted((path.parent / "recipes").glob("*.json"))
            if len(declared) != len(set(declared)) or set(declared) != {p.resolve() for p in discovered}:
                raise ValueError("model catalog differs from the recipe files")
            ids = {p.stem for p in declared}
            if not set(model.get("featured", [])).issubset(ids):
                raise ValueError("featured recipe is missing")
            covered = set()
            for example in sorted((path.parent / "examples").glob("*.json")):
                covered.update(example_records(json.loads(example.read_text())))
            if ids - covered:
                raise ValueError("recipes without saved examples: " + ", ".join(sorted(ids - covered)))
            if covered - ids:
                raise ValueError("examples name unknown recipes: " + ", ".join(sorted(covered - ids)))
        except (ValueError, KeyError, TypeError, OSError) as exc:
            errors.append(f"{relative}: {exc}")
    manifest = root / "SHA256SUMS"
    if hashes and manifest.exists():
        expected = {}
        for line in manifest.read_text().splitlines():
            digest, name = line.split("  ", 1)
            expected[name] = digest
        actual = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in files if p != manifest}
        if expected != actual:
            errors.append("SHA256SUMS: files changed; rebuild with tools/package.py")
    return errors, files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--skip-hashes", action="store_true")
    args = parser.parse_args()
    try:
        errors, files = check(args.root.resolve(), hashes=not args.skip_hashes)
    except (ValueError, OSError) as exc:
        print(f"Check failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    recipes = list((args.root / "models").glob("*/recipes/*.json"))
    print(f"Checked {len(files)} files and {len(recipes)} recipes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
