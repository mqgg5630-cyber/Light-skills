#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 ppt-master 可用的 SVG 页面（1600x900），再由 svg_to_pptx.py 导出原生 PPTX。

运行：PYTHONUTF8=1 python3 make_slides.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "ppt" / "svg_output"
SVG_DIR.mkdir(parents=True, exist_ok=True)

BG = "#0E1A2B"
PANEL = "#15283F"
ACCENT = "#E0A458"
ACCENT2 = "#5BA6A8"
TEXT = "#F2F6FA"
MUTED = "#9FB3CF"
W, H = 1600, 900


def wrap(text: str, per_line: int) -> list[str]:
    """按字符数折行，中文按宽度近似，英文与数字按半宽计。"""
    lines, cur, width = [], "", 0.0
    for ch in text:
        w = 0.55 if ord(ch) < 128 else 1.0
        if ch == "\n" or width + w > per_line:
            if ch != "\n":
                lines.append(cur)
                cur, width = ch, w
            else:
                lines.append(cur)
                cur, width = "", 0.0
            continue
        cur += ch
        width += w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, content, *, size=22, fill=TEXT, per_line=40, lh=36, weight=None):
    lines = wrap(content, per_line)
    out = [f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"'
           + (f' font-weight="{weight}"' if weight else "") + ">"]
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else lh
        out.append(f'<tspan x="{x}" dy="{dy}">{escape(ln)}</tspan>')
    out.append("</text>")
    return "\n    ".join(out), y + lh * (len(lines) - 1)


def page(name: str, body: str, bounds: str = "100 60 1400 800") -> None:
    body = re.sub(r'<g id="([^"]+)">', lambda m: f'<g id="{m.group(1)}" data-pptx-bounds="{bounds}">', body, count=1)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'lang="zh-CN" font-family="Microsoft YaHei" data-pptx-page-role="content">\n'
        f'  <rect id="page-bg" x="0" y="0" width="{W}" height="{H}" fill="{BG}" data-pptx-role="background"/>\n'
        f"{body}\n</svg>\n"
    )
    (SVG_DIR / name).write_text(svg, encoding="utf-8")


def cover():
    b = [f'  <g id="cover">',
         f'    <rect x="0" y="0" width="14" height="{H}" fill="{ACCENT}"/>',
         f'    <text x="130" y="330" font-size="30" fill="{MUTED}">抗菌肽 × 阿尔茨海默病</text>',
         f'    <text x="130" y="430" font-size="62" fill="{TEXT}" font-weight="bold">八个机制落点与计算方案</text>',
         f'    <rect x="130" y="478" width="180" height="6" fill="{ACCENT}"/>',
         f'    <text x="130" y="560" font-size="26" fill="{MUTED}">肠道宏基因组来源抗菌肽 · 对接与分子动力学 · 暴露路径判别</text>',
         f'    <text x="130" y="770" font-size="22" fill="{MUTED}">姓名：　　　　　　指导教师：</text>',
         f'  </g>']
    page("P01.svg", "\n".join(b), bounds="0 60 1400 760")


def overview():
    cols = [
        ("肠腔与肠上皮", ACCENT2, ["M8a　与细菌功能性淀粉样蛋白 CsgA、FapC 的组装界面",
                            "M8b　菌群重塑与 LPS、短链脂肪酸的变化",
                            "M7　抗菌肽自身形成淀粉样种子"]),
        ("循环与屏障", ACCENT, ["M6　与 Aβ 争夺 IDE、NEP 的催化腔",
                           "外周沉降槽：TTR、白蛋白的结合面重叠",
                           "跨屏障入脑作为条件分支"]),
        ("脑实质", "#C9705B", ["M1　AChE 的 PAS 上的三元复合物",
                           "M2　与 Aβ 的交叉成核及其方向",
                           "M4　FPR2、CLIC1、TLR4、RAGE",
                           "M5　含 GM1 的神经元膜界面",
                           "M3　tau 的 PHF6（可选）"]),
    ]
    b = ['  <g id="overview">',
         f'    <text x="110" y="128" font-size="44" fill="{TEXT}" font-weight="bold">八个落点分布在三个隔室</text>',
         f'    <rect x="110" y="156" width="120" height="5" fill="{ACCENT}"/>']
    x = 110
    for title, color, items in cols:
        b.append(f'    <rect x="{x}" y="220" width="440" height="560" fill="{PANEL}"/>')
        b.append(f'    <rect x="{x}" y="220" width="440" height="8" fill="{color}"/>')
        b.append(f'    <text x="{x+36}" y="300" font-size="30" fill="{color}" font-weight="bold">{title}</text>')
        y = 365
        for it in items:
            t, y2 = text_block(x + 36, y, it, size=21, per_line=18, lh=32, fill=TEXT)
            b.append("    " + t)
            y = y2 + 56
        x += 470
    b.append(f'    <text x="110" y="838" font-size="20" fill="{MUTED}">肠道端与外周端不依赖跨血脑屏障的假设，脑实质一侧按条件分支处理</text>')
    b.append("  </g>")
    page("P02.svg", "\n".join(b))


def mech(idx, no, title, hypo, how, judge, note=None):
    b = ['  <g id="mechanism">',
         f'    <rect x="0" y="0" width="{W}" height="170" fill="{PANEL}"/>',
         f'    <rect x="0" y="162" width="{W}" height="8" fill="{ACCENT}" fill-opacity="0.5"/>',
         f'    <text x="110" y="82" font-size="24" fill="{ACCENT}">机制 {no}</text>',
         f'    <text x="110" y="134" font-size="42" fill="{TEXT}" font-weight="bold">{escape(title)}</text>']
    rows = (("假设", hypo, ACCENT), ("做法", how, ACCENT2), ("判据", judge, "#C9705B"))
    per_line, lh = 46, 40
    heights = [len(wrap(c, per_line)) * lh for _, c, _ in rows]
    gap = max(66, min(132, (700 - sum(heights)) / 2))
    y = 270
    for (label, content, color), h in zip(rows, heights):
        b.append(f'    <rect x="110" y="{y-36:.0f}" width="6" height="48" fill="{color}"/>')
        b.append(f'    <text x="140" y="{y:.0f}" font-size="27" fill="{color}" font-weight="bold">{label}</text>')
        t, _ = text_block(244, round(y), content, size=23, per_line=per_line, lh=lh)
        b.append("    " + t)
        y += h + gap
    if note:
        b.append(f'    <rect x="110" y="776" width="1380" height="2" fill="{MUTED}" fill-opacity="0.5"/>')
        t, _ = text_block(110, 824, note, size=20, per_line=64, lh=32, fill=MUTED)
        b.append("    " + t)
    b.append("  </g>")
    page(f"P{idx:02d}.svg", "\n".join(b), bounds="0 0 1600 870")


def routes():
    b = ['  <g id="routes">',
         f'    <text x="110" y="120" font-size="44" fill="{TEXT}" font-weight="bold">肠道来源要不要过血脑屏障</text>',
         f'    <rect x="110" y="148" width="120" height="5" fill="{ACCENT}"/>']
    items = [
        ("R1　跨屏障入脑", "#C9705B", "吸收入血后经被动扩散或受体介导转胞吞进入脑实质，在脑间质达到可作用的游离浓度。最苛刻的一条。"),
        ("R2　肠道就地起效", ACCENT2, "肠腔浓度可到微摩尔以上，作用于菌群、细菌功能性淀粉样蛋白、肠上皮与肠神经系统，经迷走和免疫把信号送到中枢。"),
        ("R3　入血不入脑", ACCENT, "改变外周对 Aβ 的结合与清除（TTR、白蛋白、单核巨噬），或影响 Aβ 跨屏障的净通量。"),
    ]
    y = 220
    for title, color, body in items:
        b.append(f'    <rect x="110" y="{y}" width="1380" height="150" fill="{PANEL}"/>')
        b.append(f'    <rect x="110" y="{y}" width="8" height="150" fill="{color}"/>')
        b.append(f'    <text x="150" y="{y+54}" font-size="28" fill="{color}" font-weight="bold">{title}</text>')
        t, _ = text_block(150, y + 100, body, size=22, per_line=58, lh=34)
        b.append("    " + t)
        y += 176
    tail, _ = text_block(110, y + 52, "主线放 R2 与 R3。细菌源肽多为十几到几十个残基、净正电荷高，被动过屏障效率低；能过屏障的肽偏小、偏疏水、弱阳离子，和一般穿膜肽不是一回事。", size=23, per_line=57, lh=38)
    b.append("    " + tail)
    b.append("  </g>")
    page("P11.svg", "\n".join(b))


def conditions():
    b = ['  <g id="conditions">',
         f'    <text x="110" y="120" font-size="44" fill="{TEXT}" font-weight="bold">要主张能入脑，四条同时满足</text>',
         f'    <rect x="110" y="148" width="120" height="5" fill="{ACCENT}"/>']
    items = [
        ("序列", "血脑屏障穿透预测为阳性，不只依赖一个模型，报概率而不是只给标签"),
        ("物理", "跨膜自由能垒在可跨越范围，或能指出受体介导转胞吞的结合面"),
        ("药代", "房室模型给出的脑间质游离浓度不低于目标结合常数的十分之一"),
        ("实测", "脑组织里用质谱检出完整肽，而不是降解片段或只看荧光标记"),
    ]
    x, y = 110, 230
    for i, (tag, body) in enumerate(items):
        px = x + (i % 2) * 700
        py = y + (i // 2) * 250
        b.append(f'    <rect x="{px}" y="{py}" width="650" height="210" fill="{PANEL}"/>')
        b.append(f'    <text x="{px+40}" y="{py+70}" font-size="30" fill="{ACCENT}" font-weight="bold">{tag}</text>')
        t, _ = text_block(px + 40, py + 125, body, size=22, per_line=26, lh=36)
        b.append("    " + t)
    b.append(f'    <text x="110" y="800" font-size="23" fill="{TEXT}">四条里缺一条，机制主线就放回肠道端和外周端。脑内 Aβ 稳态本来就受外周清除和系统炎症调控。</text>')
    b.append(f'    <text x="110" y="844" font-size="22" fill="{MUTED}">配套做一件便宜的事：候选肽在模拟肠液与血浆里的稳定性和降解片段谱。片段若变短变疏水，入脑的可能性上升。</text>')
    b.append("  </g>")
    page("P12.svg", "\n".join(b))


def pipeline():
    b = ['  <g id="pipeline">',
         f'    <text x="110" y="120" font-size="44" fill="{TEXT}" font-weight="bold">八条共用一套计算流程</text>',
         f'    <rect x="110" y="148" width="120" height="5" fill="{ACCENT}"/>']
    stages = [
        ("分诊", "净电荷、疏水矩、聚集倾向、屏障穿透预测，先估各隔室的可及浓度"),
        ("结构", "ESMFold 或 AlphaFold3，保留构象系综，准备 pH 7.4 与 6.0 两套"),
        ("对接", "HADDOCK 加盲对接，AlphaFold-Multimer 交叉验证，只用来枚举界面"),
        ("动力学", "每个体系三条 1 μs，膜体系先 Martini 3 再回全原子，自由能用伞形采样"),
        ("对照", "打乱序列、等长等电荷、同源无活性三类肽同流程同时长"),
    ]
    x = 110
    for i, (t, d) in enumerate(stages):
        b.append(f'    <rect x="{x}" y="230" width="258" height="330" fill="{PANEL}"/>')
        b.append(f'    <rect x="{x}" y="230" width="258" height="7" fill="{ACCENT if i%2==0 else ACCENT2}"/>')
        b.append(f'    <text x="{x+30}" y="305" font-size="30" fill="{TEXT}" font-weight="bold">{t}</text>')
        tb, _ = text_block(x + 30, 365, d, size=20, per_line=11, lh=32, fill=MUTED)
        b.append("    " + tb)
        if i < len(stages) - 1:
            b.append(f'    <rect x="{x+262}" y="392" width="16" height="4" fill="{MUTED}"/>')
        x += 278
    b.append(f'    <text x="110" y="650" font-size="26" fill="{ACCENT}" font-weight="bold">判稳与判向</text>')
    b.append(f'    <text x="110" y="700" font-size="23" fill="{TEXT}">最后 500 ns 的界面接触占据率不低于六成，且至少两条副本一致。</text>')
    b.append(f'    <text x="110" y="742" font-size="23" fill="{TEXT}">方向在开跑前写定：伸长自由能的符号加二次成核速率，决定判为加速、改形还是无效应。</text>')
    b.append(f'    <text x="110" y="784" font-size="23" fill="{TEXT}">β 含量对力场敏感，CHARMM36m 与 a99SB-disp 两套都跑，只采信一致的结论。</text>')
    b.append("  </g>")
    page("P13.svg", "\n".join(b))


def plan():
    b = ['  <g id="plan">',
         f'    <text x="110" y="120" font-size="44" fill="{TEXT}" font-weight="bold">先做什么</text>',
         f'    <rect x="110" y="148" width="120" height="5" fill="{ACCENT}"/>']
    rows = [
        ("第一批", ACCENT, "肠道端（M8）和外周清除竞争（M6）。不依赖跨屏障假设，风险最低，也最能说明肠道来源这个出身的意义。"),
        ("第二批", ACCENT2, "AChE 三元体系（M1）和交叉成核的方向判据（M2）。已经动手的部分，补上三元、双力场和 ThT 全局拟合。"),
        ("第三批", "#C9705B", "受体层（M4）需要膜体系和细胞实验配合，周期长；膜界面（M5）、自淀粉样化（M7）、tau（M3）视前两批结果展开。"),
    ]
    y = 230
    for tag, color, body in rows:
        b.append(f'    <rect x="110" y="{y}" width="1380" height="160" fill="{PANEL}"/>')
        b.append(f'    <rect x="110" y="{y}" width="8" height="160" fill="{color}"/>')
        b.append(f'    <text x="150" y="{y+58}" font-size="28" fill="{color}" font-weight="bold">{tag}</text>')
        t, _ = text_block(150, y + 108, body, size=22, per_line=58, lh=34)
        b.append("    " + t)
        y += 186
    b.append(f'    <text x="110" y="828" font-size="22" fill="{MUTED}">跨屏障那条路径，在稳定性和降解片段谱的数据出来之前按条件分支处理，不写进主线结论。</text>')
    b.append("  </g>")
    page("P14.svg", "\n".join(b))


def main():
    for f in SVG_DIR.glob("*.svg"):
        f.unlink()
    cover()
    overview()
    mech(3, 1, "AChE 的 PAS 上的三元复合物",
         "抗菌肽在 344—361 疏水区和 PAS 邻域占位，要么替掉 Aβ 减少模板表面，要么夹成 AChE–抗菌肽–Aβ 三层把 Aβ 拉得更近。",
         "以 Tyr72、Asp74、Tyr124、Trp286、Tyr341 和 344—361 为活性残基做数据驱动对接；二元与三元体系各三条 1 μs，和已有的 AChE–Aβ 体系并排当内参。",
         "界面接触占据率、停留区段与 344—361 的重合比例、Aβ 占据 PAS 的概率变化。",
         "对照：已知只结合催化位点的小分子；湿实验用 AChE 促聚集的 ThT 曲线和 SPR。")
    mech(4, 2, "与 Aβ 的交叉成核，重点是定方向",
         "交叉成核既能加速也能抑制，方向由结合位点、化学计量比和界面电荷互补性决定，不预先定判据就不可证伪。",
         "增强采样看异质接触比例和 β-桶中间体；把肽分别放到纤维生长端和侧表面算结合与伸长自由能；侧表面补伞形采样，因为二次成核发生在那里。",
         "生长端占优且伸长自由能更负判为加速；侧表面占优并封端判为改形、滞留寡聚体；两者都弱就是没有交叉成核。",
         "湿实验用 ThT 全局拟合把总效应拆成一次成核、二次成核和伸长三个常数，与模拟判断一一对应。")
    mech(5, 3, "tau 这一侧（可选）",
         "阳离子肽能否靠芳香堆积参与 tau 的异质 β-折叠。",
         "以 PHF6（306VQIVYK311）和 PHF6*（275VQIINK280）为界面做对接和增强采样。",
         "异质 β-折叠占比与界面氢键数。",
         "阴性结果同样有用：同为阳离子而相斥，说明效应选择性地走 Aβ 和受体两条线。")
    mech(6, 4, "先天免疫受体",
         "抗菌肽占住 Aβ 用的受体口袋，或改变受体对 Aβ 的识别，由此接上神经炎症这一层表型。",
         "FPR2 用 Aβ42 与 humanin 的复合物结构做口袋对接加膜环境 MD；CLIC1 按 LL-37 的路子算结合面并看跨膜段插入倾向；TLR4–MD-2、CD14、RAGE 把候选肽当第二配体，比 pH 7.4 与 6.0。",
         "位点重合率、界面面积能否和 Aβ42 的 1166 Å² 同量级、TM6 外移这类激活构象指标。",
         "细胞端：小胶质炎症因子、NF-κB 报告、钙成像。LL-37 经 CLIC1 做出 AD 样表型，是现成的参照。")
    mech(7, 5, "神经元膜界面",
         "抗菌肽对细菌膜的选择性一旦丧失，就会在含 GM1 的神经元膜上富集，把 Aβ 招到同一界面上促进成核。",
         "建细菌内膜、含 GM1 与胆固醇的神经元膜、内皮膜三套；Martini 3 跑十几微秒看吸附和聚集，关键构象回到全原子。",
         "两类膜的结合自由能差，也就是选择性；插入深度、膜厚与曲率扰动、水柱或孔的寿命。",
         "这条通道不需要抗菌肽直接结合 Aβ，独立于交叉成核。")
    mech(8, 6, "Aβ 清除通路里的竞争",
         "候选肽占住 IDE、NEP 的催化腔，或者占住外周沉降槽的结合面，不进脑也能把脑内 Aβ 负荷抬上去。",
         "候选肽与 Aβ 分别对接进 IDE 封闭催化腔并跑 MD，比停留时间和腔口闭合；用竞争模型换算成降解速率的相对下降；再看与 TTR、白蛋白的结合面是否与 Aβ 的重叠。",
         "占位时间比、相对抑制常数排序、外周 Aβ 结合竞争实验。",
         "胰岛素竞争拖慢 Aβ 降解是现成的先例。")
    mech(9, 7, "抗菌肽自己的淀粉样化",
         "候选肽先在肠腔或循环里形成种子，再以种子而不是单体的形式参与宿主蛋白的异质成核。",
         "聚集倾向预测找热点，枚举 steric zipper，对最优的跑几百纳秒稳定性模拟看剥离功和氢键网络，再把稳定 zipper 当种子面算 Aβ 的结合与伸长自由能。",
         "zipper 剥离功；种子面对 Aβ 的伸长自由能是否显著为负。",
         "uperin 3.5 在无脂时成 cross-β、遇膜脂转 cross-α；LL-37 的 17–29 片段能自组装成功能性纤维。")
    mech(10, 8, "肠道这一端",
         "肠道端本身就能构成完整链条：抗菌肽改变细菌功能性淀粉样蛋白的组装，并重塑菌群结构。",
         "分子面是与 CsgA、FapC 组装界面的对接与 MD；群落面是用 MIC 谱作约束做群落代谢模型，预测短链脂肪酸产生菌与高产 LPS 菌的变化。",
         "配准偏移与可溶寡聚体占比；丁酸丙酸通量与 LPS 负荷；肠屏障跨上皮电阻、血清细胞因子、小胶质表型。",
         "注意方向：把 curli 从胞外纤维变成可溶寡聚体，可能反而提高跨上皮和交叉成核的能力。")
    routes()
    conditions()
    pipeline()
    plan()
    print("pages:", sorted(p.name for p in SVG_DIR.glob("*.svg")))


if __name__ == "__main__":
    main()
