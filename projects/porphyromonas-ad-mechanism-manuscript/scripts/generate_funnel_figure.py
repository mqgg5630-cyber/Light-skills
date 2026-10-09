#!/usr/bin/env python3
"""Generate an editable SVG figure for the aggregate prioritization funnel."""
from __future__ import annotations

from html import escape
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "manuscript" / "figures"
SVG = FIG / "prioritization_funnel.svg"
PNG = FIG / "prioritization_funnel.png"


def box(x, y, w, h, fill, title, lines, stroke="#18324A", title_size=31, body_size=25):
    body = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" stroke="{stroke}" stroke-width="4"/>',
        f'<text x="{x+w/2}" y="{y+42}" class="title" font-size="{title_size}" text-anchor="middle">{escape(title)}</text>',
    ]
    start = y + 79
    for i, line in enumerate(lines):
        body.append(f'<text x="{x+w/2}" y="{start+i*34}" class="body" font-size="{body_size}" text-anchor="middle">{escape(line)}</text>')
    return "\n".join(body)


def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#355B75" stroke-width="6" marker-end="url(#arrow)"/>'


def unresolved_handoff(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#829AB1" stroke-width="5" stroke-dasharray="14 12"/>'


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1540" viewBox="0 0 1800 1540">',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#355B75"/></marker></defs>',
        '<style>.title{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#102A43}.body{font-family:Arial,Helvetica,sans-serif;font-weight:400;fill:#243B53}.small{font-family:Arial,Helvetica,sans-serif;fill:#486581}.note{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#7C2D12}</style>',
        '<rect width="1800" height="1540" fill="#FFFFFF"/>',
        '<text x="900" y="58" font-family="Arial,Helvetica,sans-serif" font-size="42" font-weight="700" fill="#102A43" text-anchor="middle">Evidence-bounded aggregate computational prioritization</text>',
        '<text x="900" y="98" class="small" font-size="24" text-anchor="middle">Source-reported counts; operational thresholds; no subject-level inference or experimental confirmation</text>',
        box(110, 145, 700, 180, "#E7F5FF", "Healthy branch: descriptive context", ["11,269,961 raw sORFs", "31,510 evidence-filtered candidates", "BBB-high: 3,359 short + 40 long"]),
        box(990, 145, 700, 180, "#FFF4E6", "Periodontitis branch", ["11,721,988 raw sORFs", "33,786 evidence-filtered candidates", "BBB-high: 3,446 short + 72 long"]),
        arrow(1340, 325, 1340, 365),
        box(930, 375, 820, 180, "#FFF4E6", "BBB-high periodontitis candidates", ["UniDL4BioPep output ≥ 0.80", "3,446 short + 72 long = 3,518"]),
        arrow(1340, 555, 1340, 620),
        box(930, 630, 820, 180, "#F3E8FF", "NTxPred2", ["3,299 evaluated (7–50 aa)", "923 predicted neurotoxic; 219 <7 aa not evaluated"]),
        unresolved_handoff(1340, 810, 1340, 875),
        box(930, 885, 820, 180, "#E6FCF5", "mebipred", ["Threshold 0.50; Cu/Fe/Zn potential", "111 source-reported downstream positives"], body_size=24),
        '<text x="515" y="942" class="small" font-size="25" text-anchor="middle">Dashed transition: row-level handoff unavailable</text>',
        '<text x="515" y="978" class="small" font-size="25" text-anchor="middle">111/923 is not reported as an audited rate</text>',
        '<line x1="800" y1="963" x2="910" y2="963" stroke="#829AB1" stroke-width="3" stroke-dasharray="10 8"/>',
        arrow(1340, 1065, 1340, 1130),
        box(930, 1140, 820, 215, "#FFF9DB", "AnOxPePred prioritization", ["CHEL ≥ 0.25: n = 15", "CHEL ≥ 0.25 and FRS < 0.50: n = 12", "Stricter FRS < 0.45: n = 8"], body_size=24),
        '<rect x="110" y="1185" width="650" height="175" rx="20" fill="#FFF1F2" stroke="#9F1239" stroke-width="4"/>',
        '<text x="435" y="1235" class="note" font-size="29" text-anchor="middle">Interpretation boundary</text>',
        '<text x="435" y="1275" class="small" font-size="22" text-anchor="middle">Prioritization signals are not evidence of</text>',
        '<text x="435" y="1307" class="small" font-size="22" text-anchor="middle">brain exposure, toxicity, pro-oxidant activity,</text>',
        '<text x="435" y="1339" class="small" font-size="22" text-anchor="middle">taxonomic origin, or AD causation</text>',
        '<text x="900" y="1460" class="small" font-size="23" text-anchor="middle">BBB, blood–brain barrier; CHEL, predicted chelating score; FRS, predicted free-radical-scavenging score.</text>',
        '<text x="900" y="1500" class="small" font-size="21" text-anchor="middle">Principal-source identities are unavailable; the external source record reports 12 sequences, but row-level lineage remains unresolved.</text>',
        '</svg>',
    ]
    SVG.write_text("\n".join(parts), encoding="utf-8")
    cmd = ["convert", "-density", "160", str(SVG), "-resize", "1800x1540", str(PNG)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Some minimal ImageMagick builds declare an SVG delegate but do not ship it.
        # Draw the same content directly to a PNG with ImageMagick primitives.
        raster = ["convert", "-size", "1800x1540", "xc:white", "-font", "DejaVu-Sans"]

        def rbox(x, y, w, h, fill, title, lines, title_size=31, body_size=25):
            raster.extend(["-fill", fill, "-stroke", "#18324A", "-strokewidth", "4", "-draw", f"roundrectangle {x},{y} {x+w},{y+h} 22,22"])
            raster.extend(["-fill", "#102A43", "-stroke", "none", "-pointsize", str(title_size), "-gravity", "NorthWest", "-draw", f"text-anchor middle text {x+w/2},{y+42} '{title}'"])
            for i, line in enumerate(lines):
                raster.extend(["-fill", "#243B53", "-pointsize", str(body_size), "-draw", f"text-anchor middle text {x+w/2},{y+79+i*34} '{line}'"])

        def rtext(x, y, text, size, fill="#486581", bold=False):
            if bold:
                raster.extend(["-font", "DejaVu-Sans-Bold"])
            raster.extend(["-fill", fill, "-stroke", "none", "-pointsize", str(size), "-draw", f"text-anchor middle text {x},{y} '{text}'"])
            if bold:
                raster.extend(["-font", "DejaVu-Sans"])

        def rarrow(x1, y1, x2, y2):
            raster.extend(["-fill", "#355B75", "-stroke", "#355B75", "-strokewidth", "6", "-draw", f"line {x1},{y1} {x2},{y2} polygon {x2-12},{y2-20} {x2+12},{y2-20} {x2},{y2}"])

        raster.extend(["-gravity", "NorthWest", "-font", "DejaVu-Sans-Bold"])
        rtext(900, 58, "Evidence-bounded aggregate computational prioritization", 42, "#102A43")
        raster.extend(["-font", "DejaVu-Sans"])
        rtext(900, 98, "Source-reported counts; operational thresholds; no subject-level inference or experimental confirmation", 24)
        rbox(110, 145, 700, 180, "#E7F5FF", "Healthy branch: descriptive context", ["11,269,961 raw sORFs", "31,510 evidence-filtered candidates", "BBB-high: 3,359 short + 40 long"])
        rbox(990, 145, 700, 180, "#FFF4E6", "Periodontitis branch", ["11,721,988 raw sORFs", "33,786 evidence-filtered candidates", "BBB-high: 3,446 short + 72 long"])
        rarrow(1340, 325, 1340, 365)
        rbox(930, 375, 820, 180, "#FFF4E6", "BBB-high periodontitis candidates", ["UniDL4BioPep output >= 0.80", "3,446 short + 72 long = 3,518"])
        rarrow(1340, 555, 1340, 620)
        rbox(930, 630, 820, 180, "#F3E8FF", "NTxPred2", ["3,299 evaluated (7-50 aa)", "923 predicted neurotoxic; 219 <7 aa not evaluated"])
        raster.extend(["-stroke", "#829AB1", "-strokewidth", "5", "-draw", "line 1340,810 1340,830 line 1340,845 1340,865"])
        rbox(930, 885, 820, 180, "#E6FCF5", "mebipred", ["Threshold 0.50; Cu/Fe/Zn potential", "111 source-reported downstream positives"], body_size=24)
        rtext(515, 942, "Dashed transition: row-level handoff unavailable", 25)
        rtext(515, 978, "111/923 is not reported as an audited rate", 25)
        raster.extend(["-stroke", "#829AB1", "-strokewidth", "3", "-draw", "line 800,963 910,963"])
        rarrow(1340, 1065, 1340, 1130)
        rbox(930, 1140, 820, 215, "#FFF9DB", "AnOxPePred prioritization", ["CHEL >= 0.25: n = 15", "CHEL >= 0.25 and FRS < 0.50: n = 12", "Stricter FRS < 0.45: n = 8"], body_size=24)
        raster.extend(["-fill", "#FFF1F2", "-stroke", "#9F1239", "-strokewidth", "4", "-draw", "roundrectangle 110,1185 760,1360 20,20"])
        rtext(435, 1235, "Interpretation boundary", 29, "#7C2D12", bold=True)
        rtext(435, 1275, "Prioritization signals are not evidence of", 22)
        rtext(435, 1307, "brain exposure, toxicity, pro-oxidant activity,", 22)
        rtext(435, 1339, "taxonomic origin, or AD causation", 22)
        rtext(900, 1460, "BBB, blood-brain barrier; CHEL, predicted chelating score; FRS, predicted free-radical-scavenging score.", 23)
        rtext(900, 1500, "Principal-source identities unavailable; the external source record reports 12 sequences, but row-level lineage remains unresolved.", 21)
        raster.append(str(PNG))
        subprocess.run(raster, check=True)
    print(PNG)
    print(SVG)


if __name__ == "__main__":
    main()
