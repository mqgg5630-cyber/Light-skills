#!/usr/bin/env python3
"""程序化生成论文示意图（非数据图，仅机制/流程示意）。

说明：沙箱内无中文字体，图内标注一律使用英文，中文说明放在 docx 图题中。
运行：PYTHONUTF8=1 python3 make_figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#3B6FB6"
GREEN = "#2E8B67"
ORANGE = "#D98A2B"
GREY = "#5A5A5A"


def box(ax, x, y, w, h, text, fc, ec=None, fs=8, tc="white", weight="normal"):
    ec = ec or fc
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                linewidth=1.1, facecolor=fc, edgecolor=ec))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, wrap=True, weight=weight)


def arrow(ax, p1, p2, color=GREY, style="-|>", lw=1.2, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=11,
                                 linewidth=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


def fig1_mechanism_map() -> Path:
    fig, ax = plt.subplots(figsize=(11.0, 5.8), dpi=300)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")

    for x0, w, label, col in [(0.10, 3.10, "I. Gut lumen / epithelium", "#EAF1FA"),
                              (3.40, 3.10, "II. Circulation / barriers", "#EAF6F0"),
                              (6.70, 3.25, "III. Brain parenchyma", "#FBF1E3")]:
        ax.add_patch(FancyBboxPatch((x0, 0.35), w, 5.35, boxstyle="round,pad=0.02,rounding_size=0.04",
                                    facecolor=col, edgecolor="#CCCCCC", linewidth=0.8))
        ax.text(x0 + w / 2, 5.50, label, ha="center", va="center", fontsize=8.5, color="#333333", weight="bold")

    box(ax, 0.25, 4.55, 2.80, 0.62, "Gut metagenome-derived AMP\n(c_AMP candidate)", BLUE, fs=8.0, weight="bold")

    box(ax, 0.25, 3.62, 2.80, 0.62, "M8a  AMP x bacterial amyloid\nCsgA / FapC assembly interface", GREEN, fs=7.2)
    box(ax, 0.25, 2.78, 2.80, 0.62, "M8b  Microbiome remodelling\ncommunity FBA: LPS / SCFA shift", GREEN, fs=7.2)
    box(ax, 0.25, 1.94, 2.80, 0.62, "M7  AMP self-assembly\ncross-alpha / cross-beta seeds", GREEN, fs=7.2)
    box(ax, 0.25, 1.10, 2.80, 0.62, "Local readouts: barrier, ENS,\nvagal / immune signalling", "#7A9CC6", fs=7.2)

    box(ax, 3.55, 3.62, 2.80, 0.62, "Route R1  BBB permeation\nB3Pred + PMF + RMT docking", ORANGE, fs=7.2)
    box(ax, 3.55, 2.78, 2.80, 0.62, "Route R3  Peripheral action\nAbeta sink: TTR / albumin / ApoE", ORANGE, fs=7.2)
    box(ax, 3.55, 1.94, 2.80, 0.62, "M6  Clearance-enzyme competition\nIDE / NEP catalytic chamber", ORANGE, fs=7.2)
    box(ax, 3.55, 1.10, 2.80, 0.62, "PBPK exposure model\ngut - plasma - brain ISF", "#C79A5C", fs=7.2)

    box(ax, 6.85, 4.40, 2.95, 0.62, "M1  AChE PAS ternary complex\nAMP / Abeta / AChE 344-361", "#B4562B", fs=7.2)
    box(ax, 6.85, 3.56, 2.95, 0.62, "M2  Cross-nucleation with Abeta\nends / surface / beta-barrel", "#B4562B", fs=7.2)
    box(ax, 6.85, 2.72, 2.95, 0.62, "M4  Innate-immune receptors\nFPR2 / CLIC1 / TLR4 / RAGE", "#B4562B", fs=7.2)
    box(ax, 6.85, 1.88, 2.95, 0.62, "M5  Neuronal membrane interface\nGM1 / cholesterol, pore, Ca2+", "#B4562B", fs=7.2)
    box(ax, 6.85, 1.04, 2.95, 0.62, "M3  Tau PHF6 hetero-assembly\n(optional module)", "#C98C6B", fs=7.2)

    arrow(ax, (1.65, 4.55), (1.65, 4.24), BLUE)
    arrow(ax, (1.65, 3.62), (1.65, 3.40), GREEN)
    arrow(ax, (1.65, 2.78), (1.65, 2.56), GREEN)
    arrow(ax, (1.65, 1.94), (1.65, 1.72), GREEN)
    arrow(ax, (3.05, 4.86), (3.55, 3.93), BLUE, rad=-0.15)
    arrow(ax, (3.05, 2.25), (3.55, 2.25), GREEN)
    arrow(ax, (3.05, 1.41), (3.55, 1.41), GREEN, ls="--")
    arrow(ax, (6.35, 3.93), (6.85, 4.55), ORANGE, rad=0.12)
    arrow(ax, (6.35, 3.93), (6.85, 3.87), ORANGE)
    arrow(ax, (6.35, 3.09), (6.85, 3.03), ORANGE, ls="--")
    arrow(ax, (6.35, 2.25), (6.85, 2.19), ORANGE, ls="--")
    arrow(ax, (6.35, 1.41), (6.85, 1.41), "#C79A5C", ls="--")

    ax.text(5.0, 0.12, "solid arrow = direct molecular event tested by docking/MD;  dashed arrow = indirect / signal-mediated link",
            ha="center", fontsize=7.4, color="#444444")
    p = OUT / "fig1_mechanism_map.png"
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


def fig2_workflow() -> Path:
    fig, ax = plt.subplots(figsize=(11.5, 4.9), dpi=300)
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.0); ax.axis("off")

    stages = [
        ("Stage 0", "Sequence triage", "AMPSphere / c_AMP set\nnet charge, hydroph. moment\nAmyloGram / WALTZ\nZipperDB; B3Pred (BBB)", BLUE),
        ("Stage 1", "Structure", "ESMFold / ColabFold\nAlphaFold3\npH 7.4 and pH 6.0 states\nensemble of 5 models", "#4C7FBF"),
        ("Stage 2", "Docking", "HADDOCK2.4 data-driven\nClusPro-PeptiDock\nHPEPDOCK blind docking\nAF-Multimer ipTM check", GREEN),
        ("Stage 3", "MD + free energy", "GROMACS; CHARMM36m\nand a99SB-disp; 3 x 1 us\nMartini 3 coarse grained\nREST2 / metaD / PMF", ORANGE),
        ("Stage 4", "Systems + wet-lab", "PBPK exposure model\ncommunity FBA (MICOM)\nThT / TEM / SPR / CD\nTranswell BBB; in vivo", "#8E5AA8"),
    ]
    x = 0.20
    w, gap = 2.06, 0.30
    for i, (tag, title, body, col) in enumerate(stages):
        box(ax, x, 2.35, w, 2.25, f"{tag}\n{title}\n\n{body}", col, fs=6.6)
        if i < len(stages) - 1:
            arrow(ax, (x + w + 0.02, 3.47), (x + w + gap - 0.04, 3.47), GREY, lw=1.4)
        x += w + gap

    gates = [
        "G1  exposure gate: predicted free concentration at the target site > 0.1 x binding Kd, otherwise re-assign the route",
        "G2  pose gate: at least 2 of 3 docking engines agree; top cluster >= 30 % of decoys; AF-Multimer ipTM >= 0.6",
        "G3  stability gate: interface contact occupancy >= 60 % over the last 500 ns in at least 2 of 3 replicas",
        "G4  direction gate: sign of dG(elongation) plus secondary-nucleation rate decides accelerate / inhibit / remodel",
        "G5  falsification gate: scrambled-sequence and charge-matched control peptides must fail G2-G4",
    ]
    ax.text(0.22, 2.02, "Pass / fail gates", fontsize=8.4, weight="bold", color="#222222", va="center")
    for i, g in enumerate(gates):
        ax.text(0.22, 1.70 - i * 0.33, g, fontsize=7.3, color="#333333", va="center")

    p = OUT / "fig2_workflow.png"
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


if __name__ == "__main__":
    for f in (fig1_mechanism_map(), fig2_workflow()):
        print("wrote", f)
