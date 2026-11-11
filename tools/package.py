"""Validate the repository and create dist/model-steering.zip."""
from __future__ import annotations

import hashlib
import zipfile

from check_repo import ROOT, check


def main() -> None:
    errors, files = check(hashes=False)
    if errors:
        raise SystemExit("\n".join(errors))
    manifest = ROOT / "SHA256SUMS"
    manifest.write_text("".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}\n"
        for path in files if path != manifest
    ))
    errors, files = check()
    if errors:
        raise SystemExit("\n".join(errors))
    output = ROOT / "dist" / "model-steering.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            entry = zipfile.ZipInfo("model-steering/" + path.relative_to(ROOT).as_posix(), (2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            entry.create_system = 3
            archive.writestr(entry, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(f"{digest}  {output.name}\n")
    print(f"Created dist/{output.name} ({len(files)} files, {output.stat().st_size:,} bytes).")


if __name__ == "__main__":
    main()
