#!/usr/bin/env python3
"""离线 skill 检索器（find-skills 的本地回退实现）。

背景
----
vercel-labs 的 `find-skills` 技能依赖 Skills CLI (`npx skills find`) 去查询
skills.sh 注册表。本沙箱内 skills.sh / raw.githubusercontent.com 不可达
（`curl https://skills.sh/` 返回 000，`npx skills find <query>` 一律 "No skills found"），
因此按 find-skills 的工作流（理解意图 → 检索 → 核验来源 → 呈现 → 安装）
改为对**已安装到本地技能目录的 SKILL.md 清单**做关键词/同义词打分检索。

用法
----
    PYTHONUTF8=1 python3 skill_finder.py --query "molecular docking" "molecular dynamics" ...
    PYTHONUTF8=1 python3 skill_finder.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_ROOTS = [
    Path.home() / "Light-skills" / ".claude" / "skills",
    Path.home() / ".claude" / "skills",
]

# 任务 → 检索词（对应本课题的 8 个机制模块与交付需求）
DEFAULT_QUERIES = [
    "protein peptide molecular docking pose prediction",
    "molecular dynamics simulation trajectory free energy",
    "protein structure prediction language model embedding",
    "cheminformatics rdkit ligand",
    "systematic literature review pubmed citation",
    "paper lookup doi metadata verification",
    "hypothesis generation mechanism",
    "critical appraisal reviewer attack",
    "statistics power reproducibility experiment design",
    "pharmacokinetics PBPK exposure modeling",
    "scientific manuscript writing provenance",
    "word document docx report formatting",
    "figure plotting publication quality",
]


@dataclass
class SkillHit:
    name: str
    path: str
    score: float
    matched: list[str]
    description: str


def parse_frontmatter(md: str) -> dict[str, str]:
    if not md.startswith("---"):
        return {}
    end = md.find("\n---", 3)
    if end == -1:
        return {}
    block = md[3:end]
    out: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key = m.group(1)
            out[key] = m.group(2).strip().strip('>|').strip()
        elif key and line.strip():
            out[key] = (out.get(key, "") + " " + line.strip()).strip()
    return out


def index_skills(roots: list[Path]) -> list[tuple[str, Path, str, str]]:
    """返回 (name, path, description, full_text_lower)。"""
    seen: dict[str, tuple[str, Path, str, str]] = {}
    for root in roots:
        if not root.exists():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            text = skill_md.read_text(encoding="utf-8", errors="ignore")
            fm = parse_frontmatter(text)
            name = fm.get("name") or skill_md.parent.name
            desc = re.sub(r"\s+", " ", fm.get("description", ""))[:400]
            seen.setdefault(name, (name, skill_md.parent, desc, text.lower()))
    return list(seen.values())


def search(index, query: str, top_k: int = 5) -> list[SkillHit]:
    terms = [t for t in re.split(r"[^a-zA-Z0-9\u4e00-\u9fff]+", query.lower()) if len(t) > 2]
    hits: list[SkillHit] = []
    for name, path, desc, blob in index:
        matched, score = [], 0.0
        for t in terms:
            n = blob.count(t)
            if n:
                matched.append(t)
                # 名称/描述命中权重更高
                score += 2.0 if t in name.lower() else 0.0
                score += 1.5 if t in desc.lower() else 0.0
                score += min(n, 10) * 0.15
        if score > 0:
            hits.append(SkillHit(name, str(path), round(score, 2), matched, desc))
    hits.sort(key=lambda h: (-h.score, h.name))
    return hits[:top_k]


def selftest() -> int:
    idx = index_skills(DEFAULT_ROOTS)
    assert idx, "未发现任何已安装 skill（先运行 bootstrap_agent_skills.py 或安装第三方技能）"
    hits = search(idx, "molecular dynamics simulation")
    assert hits, "检索不应为空"
    assert all(h.score > 0 for h in hits)
    print(f"selftest ok: indexed={len(idx)} top={hits[0].name} score={hits[0].score}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", nargs="*", default=DEFAULT_QUERIES)
    ap.add_argument("--roots", nargs="*", default=[str(p) for p in DEFAULT_ROOTS])
    ap.add_argument("--top-k", type=int, default=4)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    idx = index_skills([Path(r) for r in args.roots])
    report = {"indexed_skills": len(idx), "results": {}}
    for q in args.query:
        hits = search(idx, q, args.top_k)
        report["results"][q] = [asdict(h) for h in hits]
        if not args.json:
            print(f"\n### {q}")
            for h in hits:
                print(f"  - {h.name:<32} score={h.score:<6} :: {h.description[:120]}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
