#!/usr/bin/env python3
"""Plot local three-run AutoDock Vina scores with best-run markers."""
from __future__ import annotations

import csv
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "manuscript" / "figures"
SVG = FIG / "fig5_docking_scores.svg"
PNG = FIG / "fig5_docking_scores.png"
PDF = FIG / "fig5_docking_scores.pdf"
SOURCE = ROOT / "source_materials" / "md_results" / "local_vina_docking_summary.csv"
ORDER = [
    "FLLHTTR", "YLSLLQR", "ALLLHRC", "FCLHLQLR", "YHHLLCRR", "LLHLPKRTT",
    "LLHPLRL", "WLLVHLKK", "LLHPLRC", "HLLTLKKHV", "HLPLLHRCC", "HVLLLRQCA",
]
Y_MIN, Y_MAX = -10.6, -6.8  # more negative at the top
PLOT_TOP, PLOT_BASE = 170, 700


def load_rows() -> list[tuple[str, float, float, float]]:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        indexed = {row["Ligand"].strip().upper(): row for row in csv.DictReader(handle)}
    rows = []
    for name in ORDER:
        row = indexed[name]
        rows.append((
            name,
            float(row["Best_Affinity_kcal_mol"]),
            float(row["Mean_Affinity_kcal_mol"]),
            float(row["SD_Affinity"]),
        ))
    return rows


def ymap(value: float) -> float:
    return PLOT_TOP + (Y_MIN - value) / (Y_MIN - Y_MAX) * (PLOT_BASE - PLOT_TOP)


def diamond(cx: float, cy: float, size: float = 11) -> str:
    return (
        f"{cx},{cy - size} {cx + size},{cy} {cx},{cy + size} {cx - size},{cy}"
    )


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    data = load_rows()
    width, height = 1600, 940
    left, right = 150, 1540
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1600" height="940" fill="#FFFFFF"/>',
        '<style>.t{font-family:Arial,Helvetica,sans-serif;fill:#000000}.s{font-family:Arial,Helvetica,sans-serif;fill:#333333}</style>',
        '<text x="150" y="48" class="t" font-size="30" font-weight="700">Local AutoDock Vina scores against human AChE (PDB 4EY6)</text>',
        '<text x="150" y="82" class="s" font-size="20">Mean ± SD from three independent successful runs (n = 3); orange diamonds mark the best-run affinity</text>',
        f'<line x1="{left}" y1="{PLOT_BASE}" x2="{right}" y2="{PLOT_BASE}" stroke="#000000" stroke-width="3"/>',
        f'<line x1="{left}" y1="{PLOT_TOP}" x2="{left}" y2="{PLOT_BASE}" stroke="#000000" stroke-width="3"/>',
    ]
    for tick in (-10.5, -10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0):
        y = ymap(tick)
        parts += [
            f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#D0D0D0" stroke-width="1"/>',
            f'<text x="{left - 14}" y="{y + 7}" class="s" font-size="20" text-anchor="end">{tick:.1f}</text>',
        ]
    gap = (right - left - 80) / (len(data) - 1)
    for i, (name, best, mean, sd) in enumerate(data):
        x = left + 40 + i * gap
        y_mean = ymap(mean)
        y_lo = ymap(mean - sd)
        y_hi = ymap(mean + sd)
        y_best = ymap(best)
        parts += [
            f'<line x1="{x}" y1="{y_lo}" x2="{x}" y2="{y_hi}" stroke="#000000" stroke-width="3"/>',
            f'<line x1="{x - 10}" y1="{y_lo}" x2="{x + 10}" y2="{y_lo}" stroke="#000000" stroke-width="3"/>',
            f'<line x1="{x - 10}" y1="{y_hi}" x2="{x + 10}" y2="{y_hi}" stroke="#000000" stroke-width="3"/>',
            f'<circle cx="{x}" cy="{y_mean}" r="8" fill="#0072B2" stroke="#000000" stroke-width="1.5"/>',
            f'<polygon points="{diamond(x, y_best)}" fill="#D55E00" stroke="#000000" stroke-width="1.5"/>',
            f'<text x="{x}" y="{PLOT_BASE + 28 + (i % 2) * 26}" class="t" font-size="17" text-anchor="middle">{name}</text>',
        ]
    parts += [
        '<rect x="150" y="860" width="14" height="14" fill="#0072B2" stroke="#000000"/>',
        '<text x="172" y="872" class="s" font-size="18">Mean affinity</text>',
        '<polygon points="330,867 341,854 352,867 341,880" fill="#D55E00" stroke="#000000"/>',
        '<text x="362" y="872" class="s" font-size="18">Best-run affinity</text>',
        '<text x="150" y="122" class="t" font-size="20">AutoDock Vina score (kcal/mol); more negative = stronger predicted binding</text>',
        '<text x="1540" y="920" class="s" font-size="16" text-anchor="end">Descriptive within-set ranking only; scores are not experimental binding free energies.</text>',
        '</svg>',
    ]
    SVG.write_text("\n".join(parts), encoding="utf-8")
    svg_png = subprocess.run(
        ["convert", "-density", "150", str(SVG), "-resize", "1600x940", str(PNG)],
        capture_output=True, text=True,
    )
    if svg_png.returncode != 0:
        cmd = [
            "convert", "-size", "1600x940", "xc:white", "-gravity", "NorthWest",
            "-font", "DejaVu-Sans",
        ]

        def draw(spec: str, *, fill="none", stroke="#000000", sw=2) -> None:
            cmd.extend(["-fill", fill, "-stroke", stroke, "-strokewidth", str(sw), "-draw", spec])

        def text(x: float, y: float, value: str, size: int, color="#000000", anchor="start", bold=False) -> None:
            if bold:
                cmd.extend(["-font", "DejaVu-Sans-Bold"])
            cmd.extend([
                "-fill", color, "-stroke", "none", "-pointsize", str(size),
                "-draw", f"text-anchor {anchor} text {x},{y} '{value}'",
            ])
            if bold:
                cmd.extend(["-font", "DejaVu-Sans"])

        text(150, 48, "Local AutoDock Vina scores against human AChE (PDB 4EY6)", 30, bold=True)
        text(150, 82, "Mean +/- SD from three independent successful runs (n = 3); orange diamonds mark the best-run affinity", 18, "#333333")
        text(150, 122, "AutoDock Vina score (kcal/mol); more negative = stronger predicted binding", 20)
        draw(f"line {left},{PLOT_BASE} {right},{PLOT_BASE}", sw=3)
        draw(f"line {left},{PLOT_TOP} {left},{PLOT_BASE}", sw=3)
        for tick in (-10.5, -10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0):
            yy = ymap(tick)
            draw(f"line {left},{yy} {right},{yy}", stroke="#D0D0D0", sw=1)
            text(left - 14, yy + 7, f"{tick:.1f}", 20, "#333333", "end")
        for i, (name, best, mean, sd) in enumerate(data):
            xx = left + 40 + i * gap
            y_mean = ymap(mean)
            y_lo = ymap(mean - sd)
            y_hi = ymap(mean + sd)
            y_best = ymap(best)
            draw(f"line {xx},{y_lo} {xx},{y_hi}", sw=3)
            draw(f"line {xx - 10},{y_lo} {xx + 10},{y_lo}", sw=3)
            draw(f"line {xx - 10},{y_hi} {xx + 10},{y_hi}", sw=3)
            draw(f"circle {xx},{y_mean} {xx + 8},{y_mean}", fill="#0072B2", stroke="#000000", sw=1)
            draw(
                f"polygon {xx},{y_best - 11} {xx + 11},{y_best} {xx},{y_best + 11} {xx - 11},{y_best}",
                fill="#D55E00", stroke="#000000", sw=1,
            )
            text(xx, PLOT_BASE + 28 + (i % 2) * 26, name, 16, anchor="middle")
        draw("rectangle 150,858 164,872", fill="#0072B2", stroke="#000000", sw=1)
        text(172, 872, "Mean affinity", 18, "#333333")
        draw("polygon 330,867 341,854 352,867 341,880", fill="#D55E00", stroke="#000000", sw=1)
        text(362, 872, "Best-run affinity", 18, "#333333")
        text(1540, 920, "Descriptive within-set ranking only; scores are not experimental binding free energies.", 16, "#333333", "end")
        cmd.append(str(PNG))
        subprocess.run(cmd, check=True)
    pdf_run = subprocess.run(["convert", str(PNG), str(PDF)], capture_output=True, text=True)
    print(SVG)
    print(PNG)
    if pdf_run.returncode == 0:
        print(PDF)
    else:
        print("pdf_conversion_skipped")


if __name__ == "__main__":
    main()
