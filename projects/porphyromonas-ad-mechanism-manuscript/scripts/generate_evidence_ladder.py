#!/usr/bin/env python3
"""Generate a programmatic evidence ladder distinguishing results from future tests."""
from __future__ import annotations

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "manuscript" / "figures"
SVG = FIG / "evidence_ladder.svg"
PNG = FIG / "evidence_ladder.png"

stages = [
    ("1", "Aggregate screening", "counts and thresholds", "REACHED", "#DFF3E4", "#176B3A"),
    ("2", "Twelve sequences", "external source record", "PARTIAL", "#E7F5FF", "#0B6E99"),
    ("3", "Docking scores", "external summary only", "PARTIAL", "#E7F5FF", "#0B6E99"),
    ("4", "MD protocol", "analysis pending", "METHOD ONLY", "#E7F5FF", "#0B6E99"),
    ("5", "Translation and BBB", "transport / toxicity", "NOT TESTED", "#F3F4F6", "#5B6472"),
    ("6", "Metal-dependent", "biochemical mechanism", "NOT TESTED", "#F3F4F6", "#5B6472"),
    ("7", "Disease association", "or causality", "NOT TESTED", "#F3F4F6", "#5B6472"),
]


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    width, height = 1800, 980
    box_w, box_h = 215, 245
    x0, gap, y = 45, 30, 275
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#78909C"/></marker></defs>',
        '<rect width="1800" height="980" fill="#FFFFFF"/>',
        '<style>.t{font-family:Arial,Helvetica,sans-serif;fill:#102A43}.b{font-family:Arial,Helvetica,sans-serif;fill:#334E68}.s{font-family:Arial,Helvetica,sans-serif;fill:#486581}</style>',
        '<text x="900" y="70" class="t" font-size="44" font-weight="700" text-anchor="middle">Evidence ladder: where the present study stops</text>',
        '<text x="900" y="116" class="s" font-size="25" text-anchor="middle">External sequence/score summaries improve prioritization but do not replace raw lineage, poses, exposure, phenotype, or mechanism</text>',
    ]
    for i, (num, line1, line2, status, fill, accent) in enumerate(stages):
        x = x0 + i * (box_w + gap)
        if i:
            parts.append(f'<line x1="{x-gap+8}" y1="{y+box_h/2}" x2="{x-14}" y2="{y+box_h/2}" stroke="#78909C" stroke-width="5" marker-end="url(#arrow)"/>')
        parts += [
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="22" fill="{fill}" stroke="{accent}" stroke-width="4"/>',
            f'<circle cx="{x+box_w/2}" cy="{y+48}" r="28" fill="{accent}"/>',
            f'<text x="{x+box_w/2}" y="{y+58}" font-family="Arial,Helvetica,sans-serif" fill="#FFFFFF" font-size="28" font-weight="700" text-anchor="middle">{num}</text>',
            f'<text x="{x+box_w/2}" y="{y+112}" class="t" font-size="17" font-weight="700" text-anchor="middle">{line1}</text>',
            f'<text x="{x+box_w/2}" y="{y+145}" class="t" font-size="17" font-weight="700" text-anchor="middle">{line2}</text>',
            f'<rect x="{x+35}" y="{y+180}" width="{box_w-70}" height="42" rx="16" fill="{accent}"/>',
            f'<text x="{x+box_w/2}" y="{y+208}" font-family="Arial,Helvetica,sans-serif" fill="#FFFFFF" font-size="20" font-weight="700" text-anchor="middle">{status}</text>',
        ]
    parts += [
        '<rect x="205" y="650" width="1390" height="175" rx="26" fill="#FFF7ED" stroke="#C2410C" stroke-width="4"/>',
        '<text x="900" y="704" font-family="Arial,Helvetica,sans-serif" fill="#9A3412" font-size="30" font-weight="700" text-anchor="middle">Required progression</text>',
        '<text x="900" y="746" class="b" font-size="23" text-anchor="middle">Release row-level screening lineage and raw docking inputs, logs and poses; reproduce the reported ranking.</text>',
        '<text x="900" y="780" class="b" font-size="23" text-anchor="middle">Confirm translation/expression, BBB transport, toxicity and metal-dependent effects with controls and replication.</text>',
        '<text x="900" y="814" class="b" font-size="23" text-anchor="middle">Only then evaluate a defined disease-relevant mechanism.</text>',
        '<text x="900" y="912" class="s" font-size="23" text-anchor="middle">BBB, blood–brain barrier. Grey stages are future evidence requirements and are not results of this study.</text>',
        '</svg>',
    ]
    SVG.write_text("\n".join(parts), encoding="utf-8")

    # Rasterize with ImageMagick primitives because this environment lacks an SVG renderer.
    cmd = ["convert", "-size", f"{width}x{height}", "xc:white", "-gravity", "NorthWest", "-font", "DejaVu-Sans"]

    def text(x: float, yy: float, value: str, size: int, color="#334E68", bold=False):
        if bold:
            cmd.extend(["-font", "DejaVu-Sans-Bold"])
        cmd.extend(["-fill", color, "-stroke", "none", "-pointsize", str(size), "-draw", f"text-anchor middle text {x},{yy} '{value}'"])
        if bold:
            cmd.extend(["-font", "DejaVu-Sans"])

    text(900, 70, "Evidence ladder: where the present study stops", 44, "#102A43", True)
    text(900, 116, "External sequence/score summaries improve prioritization but do not replace raw lineage, poses, exposure, phenotype, or mechanism", 25, "#486581")
    for i, (num, line1, line2, status, fill, accent) in enumerate(stages):
        x = x0 + i * (box_w + gap)
        if i:
            yy = y + box_h / 2
            cmd.extend(["-fill", "#78909C", "-stroke", "#78909C", "-strokewidth", "5", "-draw", f"line {x-gap+8},{yy} {x-14},{yy} polygon {x-14},{yy} {x-30},{yy-10} {x-30},{yy+10}"])
        cmd.extend(["-fill", fill, "-stroke", accent, "-strokewidth", "4", "-draw", f"roundrectangle {x},{y} {x+box_w},{y+box_h} 22,22"])
        cmd.extend(["-fill", accent, "-stroke", "none", "-draw", f"circle {x+box_w/2},{y+48} {x+box_w/2+28},{y+48}"])
        text(x+box_w/2, y+58, num, 28, "white", True)
        text(x+box_w/2, y+112, line1, 17, "#102A43", True)
        text(x+box_w/2, y+145, line2, 17, "#102A43", True)
        cmd.extend(["-fill", accent, "-stroke", "none", "-draw", f"roundrectangle {x+35},{y+180} {x+box_w-35},{y+222} 16,16"])
        text(x+box_w/2, y+208, status, 20, "white", True)
    cmd.extend(["-fill", "#FFF7ED", "-stroke", "#C2410C", "-strokewidth", "4", "-draw", "roundrectangle 205,650 1595,825 26,26"])
    text(900, 704, "Required progression", 30, "#9A3412", True)
    text(900, 746, "Release screening lineage plus raw docking inputs, logs and poses; reproduce the reported ranking.", 23)
    text(900, 780, "Confirm expression, BBB transport, toxicity and metal effects with controls and replication.", 23)
    text(900, 814, "Only then evaluate a defined disease-relevant mechanism.", 23)
    text(900, 912, "BBB, blood-brain barrier. Grey stages are future evidence requirements and are not results of this study.", 23, "#486581")
    cmd.append(str(PNG))
    subprocess.run(cmd, check=True)
    print(PNG)
    print(SVG)


if __name__ == "__main__":
    main()
