#!/usr/bin/env python3
"""Build a section-parallel bilingual manuscript from English and Chinese Markdown."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "manuscript" / "manuscript_en.md"
ZH = ROOT / "manuscript" / "manuscript_zh.md"
OUT = ROOT / "manuscript" / "manuscript_bilingual.md"


def split_document(text: str):
    lines = text.splitlines()
    title = lines[0].removeprefix("# ").strip()
    preamble = []
    sections = []
    current_title = None
    current = []
    for line in lines[1:]:
        if line.startswith("## "):
            if current_title is None:
                preamble = current
            else:
                sections.append((current_title, current))
            current_title = line[3:].strip()
            current = []
        else:
            current.append(line)
    if current_title is not None:
        sections.append((current_title, current))
    return title, preamble, sections


def clean_block(lines, shift_headings=True):
    out = []
    for line in lines:
        if shift_headings and re.match(r"^#{3,6} ", line):
            line = "#" + line
        out.append(line)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def main():
    en_title, en_pre, en_sections = split_document(EN.read_text(encoding="utf-8"))
    zh_title, zh_pre, zh_sections = split_document(ZH.read_text(encoding="utf-8"))
    if len(en_sections) != len(zh_sections):
        raise SystemExit(f"section mismatch: en={len(en_sections)} zh={len(zh_sections)}")

    paired_titles = [
        "Abstract / 摘要",
        "1. Introduction / 1 引言",
        "2. Materials and Methods / 2 材料与方法",
        "3. Results / 3 结果",
        "4. Discussion / 4 讨论",
        "5. Conclusions / 5 结论",
        "Declarations / 声明",
    ]
    out = [
        f"# {en_title}",
        "",
        f"# {zh_title}",
        "",
        "**Bilingual section-parallel scientific-content draft / 中英文分节对照科学内容草案**",
        "",
    ]
    out.extend(clean_block(en_pre, shift_headings=False))
    out.append("")
    out.extend(clean_block(zh_pre, shift_headings=False))
    out.append("")

    # Pair all sections except the duplicated reference lists.
    for idx, ((en_name, en_lines), (zh_name, zh_lines)) in enumerate(zip(en_sections, zh_sections)):
        if en_name == "References" and zh_name == "参考文献":
            out.extend(["## References / 参考文献", ""])
            # One shared numbered list is enough; identifiers and metadata are language-independent.
            out.extend(clean_block(en_lines, shift_headings=False))
            out.extend([
                "",
                "*The reference list is shared by both language versions. / 中英文版本共用同一参考文献表。*",
                "",
            ])
            continue
        heading = paired_titles[idx]
        out.extend([f"## {heading}", "", "### English", ""])
        out.extend(clean_block(en_lines))
        out.extend(["", "### 中文", ""])
        out.extend(clean_block(zh_lines))
        out.append("")

    OUT.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
