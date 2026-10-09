#!/usr/bin/env python3
"""Write checksums for project artefacts while preserving the separate source manifest."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ARTIFACT_SHA256SUMS.txt"
EXACT_EXCLUDES = {
    "ARTIFACT_SHA256SUMS.txt",
    "SHA256SUMS.txt",
    "quality_reports/repository_inventory.json",
}


def main() -> int:
    rows = []
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT).as_posix()
        if (
            rel in EXACT_EXCLUDES
            or rel.startswith("source_materials/")
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {rel}")
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{OUT}: {len(rows)} artefacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
