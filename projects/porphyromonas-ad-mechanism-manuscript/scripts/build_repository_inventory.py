#!/usr/bin/env python3
"""Create a deterministic size/hash inventory of the complete project tree."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "quality_reports" / "repository_inventory.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = []
    by_group_files: Counter[str] = Counter()
    by_group_bytes: Counter[str] = Counter()
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT).as_posix()
        if (
            rel == "quality_reports/repository_inventory.json"
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        group = rel.split("/", 1)[0] if "/" in rel else "project_root"
        size = path.stat().st_size
        rows.append({"path": rel, "size_bytes": size, "sha256": sha256(path)})
        by_group_files[group] += 1
        by_group_bytes[group] += size
    report = {
        "schema": "local.repository_inventory.v1",
        "inventory_excludes": [
            "quality_reports/repository_inventory.json (self-referential output)",
            "Python bytecode caches (__pycache__ and *.pyc)",
        ],
        "total_files": len(rows),
        "total_bytes": sum(item["size_bytes"] for item in rows),
        "by_top_level_group": {
            group: {"files": by_group_files[group], "bytes": by_group_bytes[group]}
            for group in sorted(by_group_files)
        },
        "files": rows,
        "verdict": "INFORMATIONAL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{OUT}: {len(rows)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
