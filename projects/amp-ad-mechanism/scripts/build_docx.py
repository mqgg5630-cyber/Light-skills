#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成期刊投稿格式的中文稿件 DOCX（抗菌肽—AD 机制关联：对接/动力学/多尺度模拟框架）。

运行：PYTHONUTF8=1 python3 build_docx.py
输出：../outputs/抗菌肽-阿尔茨海默病-机制关联框架.docx
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

SONG, HEI, FANG, TNR = "宋体", "黑体", "仿宋", "Times New Roman"


# ----------------------------------------------------------------------------- 排版工具
def set_run(run, *, cn=SONG, en=TNR, size=10.5, bold=False, italic=False, color=None):
    run.font.name = en
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), en)
    rfonts.set(qn("w:hAnsi"), en)
    rfonts.set(qn("w:eastAsia"), cn)


def para(doc, text="", *, cn=SONG, en=TNR, size=10.5, bold=False, italic=False,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent_chars=0.0, space_before=0, space_after=3,
         line=1.5, color=None, keep_with_next=False):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    pf.keep_with_next = keep_with_next
    if indent_chars:
        pf.first_line_indent = Pt(size * indent_chars)
    if text:
        set_run(p.add_run(text), cn=cn, en=en, size=size, bold=bold, italic=italic, color=color)
    return p


def rich(doc, parts, *, size=10.5, indent_chars=2.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         space_after=3, line=1.5):
    """parts: [(text, bold), ...]"""
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    if indent_chars:
        pf.first_line_indent = Pt(size * indent_chars)
    for text, bold in parts:
        set_run(p.add_run(text), size=size, bold=bold, cn=HEI if bold else SONG)
    return p


def h1(doc, text):
    return para(doc, text, cn=HEI, size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT,
                space_before=10, space_after=5, line=1.4, keep_with_next=True)


def h2(doc, text):
    return para(doc, text, cn=HEI, size=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT,
                space_before=7, space_after=4, line=1.4, keep_with_next=True)


def h3(doc, text):
    return para(doc, text, cn=SONG, size=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT,
                space_before=5, space_after=3, line=1.4, keep_with_next=True)


def bullet(doc, text, *, size=10.5, level=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Pt(size * (2 + 2 * level))
    pf.first_line_indent = Pt(-size)
    pf.space_after = Pt(2)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.4
    set_run(p.add_run(text), size=size)
    return p


def table_caption(doc, text):
    return para(doc, text, cn=HEI, size=9, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                space_before=8, space_after=3, line=1.2, keep_with_next=True)


def figure_caption(doc, text):
    return para(doc, text, cn=HEI, size=9, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                space_before=3, space_after=8, line=1.2)


def add_table(doc, header, rows, widths=None, size=8.5):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tbl_pr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    for i, htxt in enumerate(header):
        cell = t.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.15
        set_run(p.add_run(htxt), cn=HEI, size=size, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.15
            set_run(p.add_run(val), size=size)
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    return t


def add_figure(doc, path: Path, width_cm=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    return p


def add_page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run(run, size=9)
    for instr in ("begin", "instrText", "end"):
        el = OxmlElement(f"w:fld{instr}" if instr != "instrText" else "w:instrText")
        if instr == "begin":
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), "begin")
        elif instr == "end":
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), "end")
        else:
            el.set(qn("xml:space"), "preserve"); el.text = " PAGE "
        run._r.append(el)


def reference(doc, idx, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Pt(20)
    pf.first_line_indent = Pt(-20)
    pf.space_after = Pt(2)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.25
    set_run(p.add_run(f"[{idx}] "), size=9)
    set_run(p.add_run(text), size=9)
    return p


# ----------------------------------------------------------------------------- 正文
def build() -> Path:
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = TNR
    st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), SONG)

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    sec.left_margin = sec.right_margin = Cm(2.6)
    add_page_number_footer(sec)

    # ---------------- 题名区
    para(doc, "肠道宏基因组来源抗菌肽与阿尔茨海默病的机制关联：", cn=HEI, size=16, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0, line=1.3)
    para(doc, "基于分子对接、分子动力学与多尺度计算模拟的八模块研究框架", cn=HEI, size=16, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8, line=1.3)
    para(doc, "作者姓名 1，作者姓名 2，通信作者 1*", cn=FANG, size=12,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, line=1.2)
    para(doc, "（1. 单位名称，学院/研究所，城市 邮编；2. 单位名称，城市 邮编）", cn=SONG, size=9,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, line=1.2)

    para(doc, "摘  要：本文针对“肠道宏基因组筛选获得的抗菌肽（antimicrobial peptide, AMP）如何与阿尔茨海默病"
              "（Alzheimer’s disease, AD）发生机制关联”这一问题，回答两个具体诉求：其一，现有仅有的两条机制落点"
              "（AChE–Aβ 复合物分子动力学、AMP 与 Aβ 交叉成核）数量偏少、层级单一，需要参照其他疾病中“用对接/动力学/"
              "计算模拟建立分子—疾病机制关联”的成熟做法加以扩展；其二，肠道来源这一出身是否要求 AMP 穿过血脑屏障"
              "（blood-brain barrier, BBB）才能影响大脑，还是可以经肠道端起效。为此，本文先从五类疾病范式"
              "（淀粉样共聚集/交叉成核、先天免疫受体识别、膜界面与离子通透、酶–底物竞争与清除、屏障转运与系统暴露）"
              "中提炼可移植的证据结构，再据此构建八个机制模块（M1–M8）：AChE 外周阴离子位点三元复合物、Aβ 交叉成核的"
              "热力学与动力学定向、tau PHF6 异质组装、先天免疫受体识别（FPR2/CLIC1/TLR4–MD-2–CD14/RAGE）、"
              "神经元膜界面与钙通透、Aβ 清除通路的底物竞争、AMP 自身淀粉样化与“种子输出”、肠道端细菌功能性淀粉样蛋白"
              "与菌群重塑。每个模块给出结构对象、对接与动力学方案、判据阈值、阴性对照与可证伪读出，并统一到"
              "Stage 0–4 计算工作流与 G1–G5 通过门。关于暴露路径，本文提出以“肠腔/肠上皮局部作用 + 外周信号传导”为主假设、"
              "以“直接跨 BBB 入脑”为次要分支的判别设计，并给出四项必要条件与对应的计算/实验判别指标。"
              "本框架不以“抗菌肽作为抑制剂”为叙事主线，而以“抗菌肽作为可改变 AD 关键分子过程方向的内源/外源因子”为主线，"
              "为后续论文提供可执行、可证伪、可被审稿人检验的机制版图。",
         size=9, indent_chars=0, space_after=4, line=1.35)
    para(doc, "关键词：抗菌肽；阿尔茨海默病；分子对接；分子动力学；交叉成核；肠-脑轴；血脑屏障；多尺度模拟",
         size=9, indent_chars=0, space_after=4, line=1.35)
    para(doc, "中图分类号：R749.16；Q616        文献标志码：A", size=9, indent_chars=0, space_after=10, line=1.35)

    para(doc, "Mechanistic links between gut-metagenome-derived antimicrobial peptides and "
              "Alzheimer’s disease: an eight-module framework built on docking, molecular dynamics "
              "and multiscale simulation", cn=HEI, en=TNR, size=12, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6, line=1.3)
    para(doc, "Abstract: Only two mechanistic anchors are currently available for linking a gut-derived "
              "antimicrobial peptide (AMP) to Alzheimer’s disease (AD): the molecular dynamics of the "
              "acetylcholinesterase (AChE)–amyloid-β (Aβ) complex, and AMP–Aβ cross-nucleation. Both are "
              "single-layer, and neither specifies exposure. Here we distil transferable evidence structures "
              "from five paradigms used in other diseases to establish molecule-to-disease mechanisms by docking "
              "and simulation, and construct eight mechanistic modules (M1–M8) spanning the AChE peripheral "
              "anionic site ternary complex, directionality of Aβ cross-nucleation, tau PHF6 hetero-assembly, "
              "innate-immune receptor recognition (FPR2, CLIC1, TLR4–MD-2–CD14, RAGE), the neuronal membrane "
              "interface, competition within Aβ clearance pathways, AMP self-amyloidogenesis and seed export, "
              "and the gut-side interaction with bacterial functional amyloids plus microbiome remodelling. "
              "Each module is specified with structures, docking and MD protocols, quantitative gates, negative "
              "controls and falsifiable readouts, unified by a Stage 0–4 workflow with five pass/fail gates. "
              "For exposure, we argue for a gut-local-plus-peripheral-signalling primary hypothesis with "
              "BBB permeation as a secondary, testable branch, and give the four conditions that the latter must "
              "satisfy. The framework is deliberately framed around pathogenic mechanism rather than inhibitor design.",
         en=TNR, size=9, indent_chars=0, space_after=4, line=1.3)
    para(doc, "Key words: antimicrobial peptide; Alzheimer’s disease; molecular docking; molecular dynamics; "
              "cross-nucleation; gut-brain axis; blood-brain barrier; multiscale simulation",
         en=TNR, size=9, indent_chars=0, space_after=10, line=1.3)

    # ---------------- 1 引言
    h1(doc, "1  引言")
    h2(doc, "1.1  研究背景")
    rich(doc, [("深度学习驱动的宏基因组小开放阅读框挖掘，已把抗菌肽的发现从“逐条实验筛”变成“先算后验”：从人体肠道宏基因组中预测的 "
                "2 349 条候选抗菌肽里，216 条经化学合成、181 条具抗菌活性，阳性率超过 83%", False),
               ("[1]", False),
               ("；随后覆盖 63 410 份宏基因组的 AMPSphere 又给出 863 498 条非冗余候选肽", False),
               ("[2]", False),
               ("。由此产生的肽序列，其宿主端安全性评估长期只关注溶血与细胞毒，而对“慢性、低剂量暴露是否参与神经退行性疾病过程”几乎没有计算层面的系统评估。"
                "阿尔茨海默病（AD）恰恰是最需要回答这一问题的疾病：Aβ 本身即具备抗菌肽的性质与活性", False),
               ("[18,19]", False),
               ("；人源抗菌肽 LL-37 在 AD 脑内升高，并通过激活 CLIC1 造成小胶质细胞过度活化、神经炎症与兴奋性毒性，在小鼠与猴模型中诱发 AD 样表型", False),
               ("[15]", False),
               ("。也就是说，“抗菌肽—AD”不是一个需要凭空假设的关联，而是一个已经有阳性先例、但缺少系统机制版图的关联。", False)])

    h2(doc, "1.2  现有两条机制落点及其不足")
    rich(doc, [("分子机制（一）：AChE–Aβ 复合物的分子动力学。", True),
               ("Aβ 对接进乙酰胆碱酯酶（AChE）的外周阴离子位点（peripheral anionic site, PAS）后，复合物在 1 μs（1 000 ns）模拟中保持稳定；除 PAS 外另有多处接触；"
                "Aβ 在 AChE 表面的主要停留区段为 AChE 344—361，该区段紧邻 PAS，但不受双位点抑制剂的空间位阻", False),
               ("[6]", False),
               ("。该落点的上游实验基础是清楚的：AChE 通过 PAS 附近的疏水区促进 Aβ 成纤维，并形成毒性高于 Aβ 自身的 AChE–Aβ 复合物", False),
               ("[3-5]", False),
               ("。", False)])
    rich(doc, [("分子机制（二）：抗菌肽与 Aβ 的交叉成核。", True),
               ("抗菌肽与淀粉样肽结构兼容（都倾向形成 β-折叠），可以发生交叉成核，方向由界面与浓度决定：既有“加速”的例子，也有“抑制、改变纤维形态”的例子", False),
               ("[16,17,24]", False),
               ("。", False)])
    para(doc, "这两条落点本身没有错，问题在于它们作为一篇论文的机制骨架时存在三个结构性不足：", indent_chars=2.0)
    bullet(doc, "① 层级单一。两条机制都停留在“肽—蛋白/肽—肽的单一相互作用”层，没有覆盖受体信号、膜界面、清除代谢、屏障转运与菌群系统层，"
                "审稿人容易判定为“一个对接 + 一段 MD”的薄工作。")
    bullet(doc, "② 方向未定。交叉成核既可加速也可抑制，若不预先设定“判定方向的量化判据”，任何结果都能被解释，等于不可证伪。")
    bullet(doc, "③ 暴露缺位。没有回答“肠道来源的肽凭什么出现在 AChE/Aβ 所在的脑实质”，这恰是评审最直接的攻击点，也是本文第 5 节要处理的问题。")

    h2(doc, "1.3  本文贡献")
    bullet(doc, "（i）方法学迁移：系统梳理其他疾病中“靠对接/动力学/计算模拟确立机制关联”的五类范式，抽出可直接复用的证据结构（表 1）。")
    bullet(doc, "（ii）机制版图：把两条落点扩展为八个机制模块 M1–M8，每个模块都给出结构对象、方案、判据阈值、阴性对照与可证伪读出（图 1、表 2）。")
    bullet(doc, "（iii）暴露判别：给出肠道来源肽的三条候选路径 R1–R3 及其判别矩阵与四项必要条件（表 4），把“要不要过血脑屏障”从争论变成可检验命题。")
    bullet(doc, "（iv）执行规范：统一的 Stage 0–4 工作流、G1–G5 通过门、力场/时长/副本/统计口径与常见审稿攻击应答（图 2、表 3、表 5）。")

    # ---------------- 2 方法学范式
    h1(doc, "2  方法学范式：其他疾病如何用计算模拟确立机制关联")
    rich(doc, [("把“某分子与某疾病有关”做成可发表的机制工作，其他领域已有稳定套路。共同点不是“做了对接和 MD”，而是", False),
               ("先指认一个疾病过程中的决速步或关键界面，再证明目标分子能在生理可及的浓度下改变这一步的方向或速率，"
                "最后给出体外/体内可测量的对应量", True),
               ("。本文把它们归纳为五类范式（P1–P5）。", False)])

    table_caption(doc, "表 1  五类“对接/动力学 → 疾病机制”范式及其可迁移要素")
    add_table(
        doc,
        ["范式", "代表疾病体系", "关键计算做法", "核心可证伪读出", "参考"],
        [
            ["P1 淀粉样共聚集 / 交叉成核",
             "AD × 2 型糖尿病：Aβ × hIAPP；PD：α-syn × 细菌 curli(CsgA)",
             "DMD/全原子 MD 采样异质二聚体与寡聚体；分别把单体放到纤维“生长端”与“侧表面”；自由能面（接触数–氢键数）判断结合模式优劣",
             "异质接触是否多于同质接触；β-桶中间体是否出现；生长端结合是否优于侧表面结合；对应 ThT 迟滞期/半时的变化",
             "[7-9,13]"],
            ["P2 先天免疫受体识别",
             "AD 神经炎症：Aβ 原纤维 × TLR2/TLR4/CD14/RAGE；Aβ42 × FPR2（与 humanin 竞争）",
             "MD 产生受体与配体的低能构象后做蛋白–蛋白对接（ZDOCK/HADDOCK），比较不同纤维多态与不同 pH 下的界面；GPCR 用冷冻电镜结构做共位点竞争分析",
             "是否与 Aβ 共用结合口袋、界面面积与盐桥数是否可比；竞争是否改变下游 IP/Ca²⁺ 信号",
             "[14,23]"],
            ["P3 膜界面与离子通透",
             "AD：Aβ–GM1/胆固醇膜；AMP 的成孔与 cross-α/cross-β 转换",
             "CHARMM-GUI 构建含 GM1/胆固醇/PS 的神经元膜与细菌膜；Martini 3 粗粒化长时程 + 全原子验证；插入深度与跨膜 PMF",
             "膜选择性（细菌膜 vs 神经元膜的结合自由能差）；孔径/水柱寿命；Ca²⁺ 通量指标",
             "[20,21,33,35,45]"],
            ["P4 酶–底物竞争与清除",
             "AD：IDE/NEP 对 Aβ 的降解被胰岛素等竞争性底物拖慢",
             "把候选肽与 Aβ 分别对接进催化腔，比较占位、停留时间与出口通道阻塞；用米氏竞争模型把结构量换算成清除速率变化",
             "竞争性抑制常数的相对排序；加入候选肽后 Aβ 降解半衰期是否延长",
             "[46,47]"],
            ["P5 屏障转运与系统暴露",
             "CNS 递送肽/穿膜肽；肠-脑轴代谢物与 LPS",
             "序列级 BBB 穿透预测（B3Pred/B3BPFN）+ 跨膜 PMF + 受体介导转胞吞（RMT）受体对接；PBPK 三室模型估算脑间质游离浓度",
             "预测游离浓度能否达到结合 Kd 的十分之一以上；Transwell/类器官表观渗透系数",
             "[25,26,40]"],
        ],
        widths=[2.4, 3.2, 4.4, 3.6, 1.6],
    )

    h2(doc, "2.1  从“抑制剂视角”改写为“致病机制视角”的三条规则")
    para(doc, "本课题明确不走“抗菌肽作为抗 AD 抑制剂”的叙事。把上述范式改写为机制视角时，遵循三条规则：", indent_chars=2.0)
    bullet(doc, "规则 1（换问题）：不问“能不能降低聚集”，而问“会不会改变聚集路径的分支比例”——即把终点从“纤维量”换成“寡聚体/纤维比、二次成核速率、纤维形态与毒性”。"
                "LL-37 的例子很能说明问题：它抑制长直纤维的形成，却稳定可溶性寡聚体，净效应偏向毒性而非保护[16,17,24]。")
    bullet(doc, "规则 2（换主语）：不把靶点当“待抑制的酶”，而当“疾病过程的催化面”。例如 AChE 的 PAS 在本框架中不是药物结合口袋，而是 Aβ 成核的模板表面，"
                "抗菌肽的作用是改变这个模板表面的可用性与几何[3-6]。")
    bullet(doc, "规则 3（补暴露）：任何机制声明都必须附带“该分子在该位点的可及浓度”估计，否则结论只在试管里成立（见第 5 节与门限 G1）。")

    # ---------------- 3 机制模块
    h1(doc, "3  机制模块设计（M1–M8）")
    para(doc, "图 1 给出三个解剖学隔室下的机制版图：肠腔/肠上皮（隔室 I）、循环与屏障（隔室 II）、脑实质（隔室 III）。"
              "实线箭头代表可由对接/动力学直接检验的分子事件，虚线箭头代表需要经信号或细胞层传递的间接联系。", indent_chars=2.0)
    if (FIG / "fig1_mechanism_map.png").exists():
        add_figure(doc, FIG / "fig1_mechanism_map.png", 15.8)
        figure_caption(doc, "图 1  肠道来源抗菌肽与 AD 的三隔室机制版图（M1–M8）\n"
                            "Fig.1  Three-compartment mechanistic map linking a gut-derived AMP to AD (modules M1–M8)")

    h2(doc, "3.1  M1  AChE 外周阴离子位点上的三元复合物")
    rich(doc, [("假设 H1：", True),
               ("抗菌肽可在 AChE 表面 344—361 疏水区/PAS 邻域形成稳定占位，从而改变 AChE 作为 Aβ 成核模板的几何与可用性，"
                "结果既可能是“替代 Aβ 占位（减少模板）”，也可能是“形成 AChE–AMP–Aβ 三元夹层（增强模板）”。", False)])
    bullet(doc, "结构对象：人 AChE（建议 4EY7 系列）与 Torpedo AChE 对照；Aβ40/Aβ42 无序单体系综；候选抗菌肽 ESMFold/AlphaFold3 构象系综。")
    bullet(doc, "计算方案：HADDOCK2.4 以 344—361 与 PAS 残基（Tyr72/Asp74/Tyr124/Trp286/Tyr341）为活性残基做数据驱动对接，"
                "同时用 HPEPDOCK/ClusPro-PeptiDock 盲对接交叉验证；二元（AChE–AMP）与三元（AChE–AMP–Aβ）体系各 3×1 μs，"
                "与已报道的 AChE–Aβ 1 μs 体系并行作为内参[6]。")
    bullet(doc, "判据：界面接触占据率（末 500 ns ≥60%）、停留区段重合度（与 344—361 的残基重叠比）、Aβ 在 PAS 的占位概率变化 ΔP(PAS)、"
                "MM/PBSA 相对排序[38]；三元体系需额外报告 Aβ–AChE 接触是否被削弱或被“桥接增强”。")
    bullet(doc, "阴性对照：序列打乱肽、等电荷等长的非抗菌肽、已知只结合催化位点的小分子；这些对照必须在 G2–G4 上失败。")
    bullet(doc, "湿实验对应：AChE 促 Aβ 聚集的 ThT 动力学（有/无候选肽）、AChE 活性与促聚集活性解耦实验、表面等离子体共振测 AChE–AMP 亲和力。")

    h2(doc, "3.2  M2  与 Aβ 的交叉成核：把“方向”变成可测量")
    rich(doc, [("假设 H2：", True),
               ("抗菌肽与 Aβ 的相互作用改变的是聚集", False), ("路径分支", True),
               ("而非单纯总量；其方向由结合位点（生长端 vs 侧表面）、化学计量比与界面电荷互补性共同决定。", False)])
    bullet(doc, "计算方案（借鉴 Aβ×hIAPP 的成熟设计[7,8]）：(a) 异质二聚体/三聚体的离散分子动力学或 REST2 增强采样，统计异质接触 vs 同质接触频率与 β-桶中间体占比；"
                "(b) 把抗菌肽单体分别放到 Aβ 纤维（如 2NAO/2MXU 多态）的生长端与侧表面，计算结合自由能与伸长自由能 ΔG(elongation)；"
                "(c) 用伞形采样得到侧表面“二次成核位点”的 PMF。")
    bullet(doc, "方向判据（门限 G4）：ΔG(elongation) 更负且生长端优于侧表面 → 判“加速/共纤维化”；侧表面结合占优且封端 → 判“改形/滞留寡聚体”；"
                "两者皆弱 → 判“无显著交叉成核”。该判据在开跑前写入预注册，避免事后择优解释。")
    bullet(doc, "动力学对应：ThT 曲线用全局动力学模型拟合，分离出一次成核、二次成核与伸长速率常数[42,43]，与模拟判据一一对应；"
                "这是把“加速还是抑制”从定性说法变成三个可比常数的关键一步。")
    bullet(doc, "注意事项：力场对 β 含量有系统性偏好，需并行 CHARMM36m 与 a99SB-disp 两套力场[31,32]，只报告两套一致的结论。")

    h2(doc, "3.3  M3  tau PHF6 异质组装（可选模块）")
    bullet(doc, "以 tau 的 306VQIVYK311（PHF6）与 275VQIINK280（PHF6*）为界面，做抗菌肽–tau 片段的对接与 REST2 采样，"
                "考察阳离子肽能否借芳香堆积与疏水拉链参与异质 β-折叠；阴性预期同样重要——若抗菌肽因同为阳离子而与 tau 相斥，"
                "则可作为“机制选择性”的证据写入论文，说明本课题的效应主要走 Aβ 与受体线。")

    h2(doc, "3.4  M4  先天免疫受体识别：最容易与 AD 表型对齐的一层")
    rich(doc, [("这是把“抗菌肽”与“AD”连起来最有力的一层，因为已有直接先例：LL-37 促进 CLIC1 的膜转位、整合与激活，"
                "引发小胶质细胞过度活化、神经炎症与兴奋性毒性，并在小鼠与猴中造成 Aβ 升高、缠结增多、脑萎缩与认知损害", False),
               ("[15]", False),
               ("；FPR2 则同时是 Aβ42 与 LL-37 的受体，其冷冻电镜结构显示 Aβ42 与 humanin 的结合位点高度重叠，"
                "界面面积分别为 1 166 Å² 与 1 077 Å²", False),
               ("[14]", False),
               ("，这为“外源抗菌肽占据同一口袋并改变 Aβ42 信号”提供了结构学可检验的入口。", False)])
    bullet(doc, "子模块 M4a（FPR2 竞争）：以 FPR2–Aβ42 与 FPR2–humanin 复合物为模板，做候选肽的口袋对接与膜环境 MD（3×500 ns），"
                "读出：位点重合率、界面面积、TM6 外移等激活构象指标；判据是“是否达到 Aβ42 同量级的界面面积且共位点”。")
    bullet(doc, "子模块 M4b（CLIC1 膜转位）：按 LL-37 范式，计算候选肽与 CLIC1 的结合面，并在膜体系中观察 CLIC1 跨膜段的插入倾向变化[15]。")
    bullet(doc, "子模块 M4c（TLR4–MD-2/CD14/RAGE）：参照对 Aβ 原纤维与 CD14/TLR2/TLR4/RAGE 的系统对接研究[23]，"
                "把候选肽作为“第二配体”评估其对纤维–受体识别的竞争或协同，并比较 pH 7.4 与 pH 6.0（炎症微环境）的差异。")
    bullet(doc, "表型对应：小胶质细胞 IL-1β/TNF-α 释放、NF-κB 报告基因、Ca²⁺ 成像、iPSC 源小胶质–神经元共培养。")

    h2(doc, "3.5  M5  神经元膜界面：抗菌肽“选择性”的丧失就是毒性的来源")
    bullet(doc, "构建三类膜：细菌内膜模拟（POPE/POPG 3:1）、神经元质膜（POPC/POPE/POPS/胆固醇/鞘磷脂 + GM1）、内皮膜；"
                "用 Martini 3 做 10–20 μs 粗粒化吸附与聚集[33]，对关键构象回到全原子验证。")
    bullet(doc, "读出：结合自由能差 ΔΔG(细菌膜−神经元膜)（选择性指标）、插入深度、膜曲率与厚度扰动、水柱/孔的寿命、GM1 簇集是否为 Aβ 提供成核平台[45]。")
    bullet(doc, "机制含义：若候选肽在含 GM1 的膜上富集，则它不需要“化学结合 Aβ”也能通过“把 Aβ 招募到同一界面”来促进成核——"
                "这是一条独立于 M2 的、界面介导的交叉成核通道，也是审稿人喜欢的“新机制”落点。")

    h2(doc, "3.6  M6  Aβ 清除通路的底物竞争")
    bullet(doc, "结构对象：胰岛素降解酶（IDE，如 2G47/4IOF 系列）催化腔、脑啡肽酶（NEP）、转甲状腺素蛋白（TTR）、ApoE 与血清白蛋白。")
    bullet(doc, "做法：把候选肽与 Aβ 分别对接进 IDE 的封闭催化腔并做 3×500 ns MD，比较停留时间与腔口闭合度；"
                "用竞争性米氏模型把“占位时间比”换算成 Aβ 降解速率的相对下降幅度[46,47]。")
    bullet(doc, "外周沉降槽（peripheral sink）：若候选肽与 TTR/白蛋白的结合面与 Aβ 结合面重叠，则外周 Aβ 清除能力下降，"
                "可在不入脑的前提下抬高脑内 Aβ 负荷[49,50]——这正是回答“肠道来源是否必须入脑”的关键机制之一。")

    h2(doc, "3.7  M7  抗菌肽自身的淀粉样化与“种子输出”")
    rich(doc, [("抗菌肽与淀粉样蛋白共享结构语法：uperin 3.5 可在无脂环境下形成 cross-β 纤维、在细菌膜脂存在时切换为 cross-α 纤维", False),
               ("[20,21]", False),
               ("；LL-37 的 17–29 片段可自组装为功能性超分子纤维", False),
               ("[22]", False),
               ("。因此候选肽本身可能在肠腔或循环中形成淀粉样种子，再以“种子”而非“单体”的形式参与宿主蛋白的异质成核。", False)])
    bullet(doc, "流程：AmyloGram/WALTZ/TANGO 预测聚集热点 → ZipperDB 枚举 steric zipper 候选 → 对最优 zipper 做 300–500 ns 稳定性 MD（剥离功、氢键网络）→ "
                "把稳定 zipper 作为“种子面”与 Aβ 单体做结合与伸长自由能计算。")
    bullet(doc, "判据：若种子面对 Aβ 的伸长自由能显著为负，则 M7 与 M2 构成“单体通道 + 种子通道”的双通道机制，论文叙事因此升级为“条件依赖的双向调控”。")

    h2(doc, "3.8  M8  肠道端：细菌功能性淀粉样蛋白与菌群重塑")
    rich(doc, [("肠道端本身就能构成完整的致病链条，无需先入脑。curli 的主亚基 CsgA 具有典型 cross-β 结构，其片段种子可促进 Aβ 成纤维", False),
               ("[9]", False),
               ("；在动物模型中，产 curli 细菌暴露可增强肠与脑内 α-syn 聚集、并放大 TLR2/IL-6/TNF 反应", False),
               ("[10-12]", False),
               ("；来自人体菌群的多种 CsgA 同源物同样能以 1∶1 复合物形式加速 α-syn 聚集", False),
               ("[13]", False),
               ("。抗菌肽进入这一系统后有两条可算的作用面。", False)])
    bullet(doc, "M8a（分子面）：候选肽与 CsgA/FapC 组装界面的对接与 MD——是否封端、是否改变 R1–R5 重复单元的配准、是否把可溶 CsgA 稳定为寡聚体。"
                "注意方向性：抑制 curli 组装未必是好事，若把 curli 从“胞外纤维”变成“可溶寡聚体”，反而可能提升其跨上皮与交叉成核能力。")
    bullet(doc, "M8b（群落面）：以候选肽的体外 MIC 谱为约束，用 MICOM/群落 FBA 模拟菌群结构与代谢通量的重塑[39]，"
                "预测短链脂肪酸产生菌与 LPS 高产菌的相对丰度变化，进而预测屏障完整性与外周炎症负荷的方向[40,41]。")
    bullet(doc, "读出链条：MIC 谱 → 群落 FBA 预测的丁酸/丙酸通量与 LPS 负荷 → 体外肠屏障 TEER → 血清 LPS/细胞因子 → 小胶质表型。")

    table_caption(doc, "表 2  八个机制模块的对象、方法与判据一览")
    add_table(
        doc,
        ["模块", "分子/结构对象", "主要计算方法", "关键判据（量化）", "湿实验验证"],
        [
            ["M1 AChE PAS 三元体系", "hAChE 4EY7；Aβ40/42；候选肽",
             "数据驱动对接 + 盲对接；二元/三元 3×1 μs", "接触占据率≥60%；与 344—361 重叠比；ΔP(PAS)",
             "ThT（AChE 促聚集）；SPR；AChE 活性/促聚集解耦"],
            ["M2 Aβ 交叉成核", "Aβ 单体系综、纤维 2NAO/2MXU",
             "REST2/DMD；生长端与侧表面自由能；伞形采样", "ΔG(elongation) 符号与大小；异质/同质接触比；β-桶占比",
             "ThT 全局动力学拟合（k_n, k_2, k_+）；TEM/AFM 形态"],
            ["M3 tau PHF6（可选）", "PHF6/PHF6* 片段、tau 纤维核",
             "对接 + REST2", "异质 β-折叠占比；界面氢键数", "tau 体外聚集；生物素-拉下"],
            ["M4 免疫受体", "FPR2（Aβ42/humanin 复合物）、CLIC1、TLR4–MD-2、CD14、RAGE",
             "膜环境 GPCR 对接 + 3×500 ns MD；多 pH", "位点重合率；界面面积 vs Aβ42 的 1 166 Å²；激活构象指标",
             "IP/Ca²⁺ 信号；NF-κB 报告；小胶质炎症因子"],
            ["M5 膜界面", "细菌膜 / 神经元膜(含 GM1) / 内皮膜",
             "Martini 3 10–20 μs + 全原子验证；插入 PMF", "ΔΔG(选择性)；插入深度；孔寿命；GM1 簇集",
             "钙黄绿素泄漏；LDH；膜电位；钙成像"],
            ["M6 清除竞争", "IDE、NEP、TTR、ApoE、白蛋白",
             "催化腔对接 + 3×500 ns；竞争米氏换算", "占位时间比；腔口闭合度；相对 Ki 排序",
             "IDE/NEP 酶动力学；血浆 Aβ 结合竞争"],
            ["M7 自淀粉样化", "候选肽 steric zipper 模型",
             "AmyloGram/WALTZ/ZipperDB → 300–500 ns MD → 种子伸长自由能", "zipper 剥离功；种子面 ΔG(elongation)",
             "ThT 自聚集；TEM；种子加速实验"],
            ["M8 肠道端", "CsgA/FapC 组装界面；菌群群落模型",
             "界面对接 + MD；MICOM/群落 FBA", "配准偏移；可溶寡聚体占比；SCFA 通量与 LPS 负荷变化",
             "curli 生物膜；类器官/Transwell TEER；粪菌宏基因组"],
        ],
        widths=[2.3, 3.1, 3.5, 3.5, 2.8],
    )

    # ---------------- 4 工作流
    h1(doc, "4  统一计算工作流与参数设定")
    para(doc, "八个模块共用一条工作流（图 2）。之所以强调“统一”，是因为审稿人评估这类工作时，看的不是某一次对接分数，"
              "而是整条链条的自洽性与可复现性：同一套结构来源、同一套力场与时长、同一套判据阈值、同一套阴性对照。", indent_chars=2.0)
    if (FIG / "fig2_workflow.png").exists():
        add_figure(doc, FIG / "fig2_workflow.png", 15.8)
        figure_caption(doc, "图 2  Stage 0–4 计算工作流与 G1–G5 通过门\n"
                            "Fig.2  The Stage 0–4 computational workflow and its five pass/fail gates")

    table_caption(doc, "表 3  各阶段的工具、参数与通过门")
    add_table(
        doc,
        ["阶段", "内容", "建议工具与参数", "输出与通过门"],
        [
            ["Stage 0 序列分诊", "候选肽性质与风险分层",
             "净电荷、疏水矩、两亲性；AmyloGram/WALTZ/TANGO 聚集倾向；B3Pred/B3BPFN 的 BBB 穿透概率[25,26]；溶血/细胞毒预测",
             "分诊表；G1 暴露门：目标位点预测游离浓度 ≥ 0.1×Kd"],
            ["Stage 1 结构建模", "肽与复合体初始构象",
             "ESMFold/ColabFold/AlphaFold3[27]；每条肽保留 5 个模型；pH 7.4 与 pH 6.0 两套质子化状态；无序肽用系综而非单构象",
             "构象系综 + pLDDT/PAE 报告"],
            ["Stage 2 对接", "界面枚举与共识",
             "HADDOCK2.4 数据驱动[28]；ClusPro-PeptiDock[29]、HPEPDOCK 盲对接[30]；AlphaFold-Multimer 交叉验证 ipTM[44]",
             "G2 位姿门：≥2/3 引擎一致、首簇占比≥30%、ipTM≥0.6"],
            ["Stage 3 动力学", "稳定性、自由能与路径",
             "GROMACS[34]；CHARMM36m[31] 与 a99SB-disp[32] 双力场；310 K、0.15 mol/L NaCl；全原子 3×1 μs；"
             "膜体系 CHARMM-GUI[35] + Martini 3[33]；REST2[37]、metadynamics[36]、伞形采样；MM/PBSA 仅用于排序[38]",
             "G3 稳定门：末 500 ns 接触占据率≥60% 且 ≥2/3 副本一致；G4 方向门：ΔG(elongation) 与二次成核速率符号一致"],
            ["Stage 4 系统与验证", "暴露、群落与湿实验",
             "PBPK 三室（肠腔–血浆–脑间质）；MICOM 群落 FBA[39]；ThT 全局动力学拟合[42,43]；TEM/AFM、CD、SPR；"
             "Transwell BBB 与脑类器官；灌胃给药 + 标记示踪",
             "G5 证伪门：打乱序列与等电荷对照肽必须在 G2–G4 上失败"],
        ],
        widths=[2.2, 2.6, 6.2, 4.2],
    )

    h2(doc, "4.1  统计与复现口径")
    bullet(doc, "副本：每个体系至少 3 个独立副本（不同初速度种子），结论必须在 ≥2 个副本中重复；报告块平均误差而非单轨迹标准差。")
    bullet(doc, "收敛：RMSD 平台 + 接触数时间序列 + 自由能面块收敛检验；对增强采样报告交换率（REST2 建议 20%–30%）与收敛曲线。")
    bullet(doc, "报告：MM/PBSA 只给相对排序，不与实验 Kd 直接比较；所有输入结构、mdp/参数文件、分析脚本随文归档（建议 Zenodo）。")
    bullet(doc, "阴性对照必须与正样本同流程、同时长，不得只跑一半。")

    # ---------------- 5 暴露路径
    h1(doc, "5  肠道来源意味着什么：三条暴露路径的判别")
    rich(doc, [("这是本课题最容易被问倒、也最容易做出亮点的一节。结论先行：", False),
               ("对肠道宏基因组来源的抗菌肽而言，“必须穿过血脑屏障才能影响大脑”不是默认前提，而是三条并列假设中最苛刻的一条；"
                "本文建议以肠道局部与外周信号为主假设、以跨 BBB 为次要分支", True),
               ("。理由是：多数细菌源候选肽为 10–50 残基、高净正电荷、两亲性强，这类分子的被动跨 BBB 效率极低，"
                "而 BBB 穿透肽在序列特征上自成一类（偏小、偏疏水、弱阳离子），并不等同于一般穿膜肽", False),
               ("[25,26]", False),
               ("；与此同时，肠道端与外周端已经有完整且被验证过的致病链条可用", False),
               ("[10-13,40,41,49,50]", False),
               ("。", False)])

    h2(doc, "5.1  三条候选路径")
    bullet(doc, "R1 直接入脑：肽经肠上皮吸收入血、逃过蛋白酶与肾清除、再经被动扩散或受体介导转胞吞（RMT，如 TfR/LRP1/GLUT1）跨过 BBB，"
                "在脑间质达到可与 AChE/Aβ/受体作用的游离浓度。对应 M1、M2、M4、M5 在脑内的版本。")
    bullet(doc, "R2 肠道局部 + 神经/免疫传导：肽在肠腔（浓度可达 μmol/L 甚至更高）作用于菌群、细菌功能性淀粉样蛋白、肠上皮与肠神经系统，"
                "经迷走传入、肠源免疫细胞迁移与细胞因子传导影响中枢。对应 M8a、M8b 与 M7 的肠腔版本。")
    bullet(doc, "R3 入血后外周作用：不入脑，但改变外周 Aβ 沉降槽（TTR/白蛋白/ApoE 结合与外周单核-巨噬清除）、"
                "改变 IDE/NEP 介导的外周降解、或经内皮与 RAGE/LRP1 影响 Aβ 的跨屏障净通量。对应 M6 与 M4 的外周版本。")

    table_caption(doc, "表 4  三条暴露路径的判别矩阵（计算指标 / 实验指标 / 证伪条件）")
    add_table(
        doc,
        ["判别维度", "R1 跨 BBB 入脑", "R2 肠道局部 + 神经免疫", "R3 外周作用"],
        [
            ["可及浓度量级", "脑间质游离 pmol/L–nmol/L 级，需 PBPK 支撑", "肠腔 μmol/L–mmol/L 级，最宽松", "血浆 nmol/L–μmol/L 级，受蛋白结合与清除限制"],
            ["核心计算指标", "B3Pred/B3BPFN 概率；跨膜 PMF 能垒；RMT 受体对接；PBPK 脑/血分配比 Kp,uu", "MIC 谱 + 群落 FBA 通量；CsgA 界面对接；肠上皮膜 CGMD", "血浆蛋白结合对接（白蛋白/TTR）；IDE/NEP 竞争；内皮受体对接"],
            ["关键实验", "体外 Transwell BBB/脑类器官表观渗透系数；标记肽脑内定量（LC-MS/MS 而非仅荧光）", "无菌/抗生素小鼠定植；粪菌宏基因组与代谢组；TEER；迷走切断对照", "血浆 Aβ 结合竞争；外周清除动力学；肝/脾巨噬吞噬"],
            ["阳性判据", "Kp,uu ≥ 0.05 且脑内浓度 ≥ 0.1×Kd", "菌群/屏障/炎症三项中至少两项方向一致且剂量依赖", "外周 Aβ 清除速率显著下降且脑内负荷相应升高"],
            ["证伪条件", "脑内检测不到完整肽（仅见降解片段）→ R1 不成立", "无菌小鼠中效应消失 → R2 依赖菌群的部分不成立", "迷走切断或外周清除阻断后效应不变 → R3 贡献有限"],
        ],
        widths=[2.6, 4.2, 4.2, 4.2],
    )

    h2(doc, "5.2  若要主张 R1 成立，必须同时满足的四个条件")
    bullet(doc, "① 序列级可行性：BBB 穿透预测为阳性且不只依赖单一模型（建议 B3Pred 与 B3BPFN 双阳性，并报告概率值而非仅标签）[25,26]。")
    bullet(doc, "② 物理可行性：全原子/CG 跨膜 PMF 的自由能垒处于可跨越范围，或能给出明确的 RMT 受体结合面。")
    bullet(doc, "③ 药代可行性：PBPK 模型给出的脑间质游离浓度不低于目标结合 Kd 的十分之一（门限 G1）；蛋白水解半衰期需一并纳入。")
    bullet(doc, "④ 实测可行性：脑组织中检出的是完整肽（LC-MS/MS 定量），而非降解片段或标记基团。")
    para(doc, "四条中任一条不成立，就应把论文的机制主线迁回 R2/R3，并在讨论中明确写出——这不是退让，反而是当前 AD 领域更受重视的"
              "“系统性视角”：脑内 Aβ 稳态本就受外周清除与系统炎症调控[49,50]，肠源因子无需入脑也能改变中枢病理负荷。",
         indent_chars=2.0)

    h2(doc, "5.3  给本课题的具体建议")
    bullet(doc, "把 M8（肠道端）与 M6/R3（外周端）作为论文的机制主干，把 M1/M2/M4/M5 的脑内版本作为“若肽或其片段可及脑实质”的条件性分支，"
                "并用 G1 暴露门在图 2 的流程里显式标注这一分叉。")
    bullet(doc, "在摘要与引言中使用条件化措辞：“在可及浓度下”“若跨屏障条件满足”，避免出现“抗菌肽进入大脑导致 AD”这类当前证据不支持的强声明。")
    bullet(doc, "补一个低成本的关键实验：候选肽在模拟肠液/血浆中的稳定性与降解片段谱。若主要活性片段变短、变疏水，R1 的可能性反而上升，"
                "此时应把片段而非全长肽作为脑内模块的建模对象。")

    # ---------------- 6 可证伪性与审稿应答
    h1(doc, "6  可证伪性、阴性对照与常见审稿攻击")
    table_caption(doc, "表 5  常见审稿攻击点与本框架的应答设计")
    add_table(
        doc,
        ["审稿攻击", "问题实质", "本框架的应答与证据设计"],
        [
            ["“对接分数不能说明机制”", "刚性对接的打分函数与自由能无定量对应",
             "对接只用于枚举界面假设，机制结论由 3×1 μs MD 的占据率、增强采样的自由能与湿实验三者共同支撑；对接分数不进入结论句"],
            ["“1 μs 不够长”", "采样不足可能错过解离或重排",
             "报告收敛诊断与副本一致性；对关键界面补 REST2/metadynamics 与伞形采样 PMF；明确写出“未观察到”不等于“不会发生”"],
            ["“力场偏好 β-折叠”", "结论可能是力场伪影",
             "CHARMM36m 与 a99SB-disp 双力场并行，只报告一致结论；对无序体系使用 TIP4P-D 类水模型"],
            ["“浓度不生理”", "模拟与体外常用浓度远高于体内",
             "G1 暴露门强制给出各隔室可及浓度估计；肠腔与脑实质分别评估；讨论中标注浓度外推的不确定性"],
            ["“加速还是抑制，你怎么都能解释”", "缺少预先设定的方向判据",
             "G4 方向门在开跑前预注册；ThT 全局拟合把总效应拆成 k_n/k_2/k_+ 三个常数，与模拟判据一一对应"],
            ["“为什么是这条肽，不是任何阳离子肽”", "缺少特异性证据",
             "G5 证伪门：打乱序列、等电荷等长肽、同源但无抗菌活性的肽三类对照同流程运行，必须失败"],
            ["“相关不等于因果”", "体内表型与分子机制之间跳步",
             "用无菌/抗生素小鼠、迷走切断、受体敲除（如 Clic1、Fpr2）做机制必需性检验，形成“分子—通路—表型”的三点闭合"],
        ],
        widths=[3.1, 3.5, 8.6],
    )

    # ---------------- 7 论文化建议
    h1(doc, "7  论文化建议：叙事线与图表计划")
    bullet(doc, "叙事线（四段式引言）：肠道宏基因组 AMP 正在被大规模发现并推向应用 → 但宿主端慢性暴露的神经安全性没有机制评估 → "
                "AD 领域已有 Aβ 即 AMP、LL-37 促 AD 的先例，说明“抗菌肽—AD”是真问题 → 本文给出可执行、可证伪的八模块计算框架与暴露判别。")
    bullet(doc, "图 1 机制版图（本文图 1）；图 2 工作流与门限（本文图 2）；图 3 对接共识与界面残基热图；"
                "图 4 关键体系的接触占据率与自由能面；图 5 跨膜/伸长自由能 PMF；图 6 暴露路径判别决策树；图 7 ThT 全局拟合的三常数对比。")
    bullet(doc, "表格：表 1 范式迁移；表 2 模块清单；表 3 参数与门限；表 4 路径判别矩阵；表 5 审稿应答（可放补充材料）。")
    bullet(doc, "投稿口径：若以计算为主、湿实验为辅，可考虑计算生物学/生物物理类期刊；若能补齐 M8 的菌群与屏障实验，则可向微生物组–神经退行交叉类期刊投递。"
                "具体刊物选择建议在数据完成度确定后再定。")

    # ---------------- 8 结论
    h1(doc, "8  结论")
    rich(doc, [("（1）现有两条机制落点应被视为", False), ("入口", True),
               ("而非全部：AChE–PAS 体系提供了“模板表面”这一可复用的机制隐喻，交叉成核提供了“方向由界面决定”的可检验命题。", False)],
         indent_chars=2.0)
    rich(doc, [("（2）参照其他疾病的五类范式，可以把机制版图扩展到受体识别、膜界面、清除竞争、自淀粉样化与肠道端共五层，"
                "形成八个彼此独立又可交叉验证的模块，且每个模块都有明确的量化判据与阴性对照。", False)], indent_chars=2.0)
    rich(doc, [("（3）关于肠道来源：", False),
               ("不必先假定跨血脑屏障", True),
               ("。建议以肠道局部与外周信号为机制主干，把跨屏障作为需满足四项必要条件的条件性分支；"
                "这一安排既符合现有证据分布，也更容易通过审稿。", False)], indent_chars=2.0)
    rich(doc, [("（4）本框架的价值不在于预言某个结果，而在于把“抗菌肽是否、以何种方向、在何处影响 AD 过程”写成一组"
                "可以被数据推翻的命题——这正是导师所说“机制不够”的真正解法。", False)], indent_chars=2.0)

    # ---------------- 参考文献
    h1(doc, "参考文献")
    refs = [
        "Ma Y, Guo Z, Xia B, et al. Identification of antimicrobial peptides from the human gut microbiome using deep learning[J]. Nature Biotechnology, 2022, 40(6): 921–931. doi:10.1038/s41587-022-01226-0",
        "Santos-Júnior C D, Torres M D T, Duan Y, et al. Discovery of antimicrobial peptides in the global microbiome with machine learning[J]. Cell, 2024, 187(14): 3761–3778.e16. doi:10.1016/j.cell.2024.05.013",
        "Inestrosa N C, Alvarez A, Pérez C A, et al. Acetylcholinesterase accelerates assembly of amyloid-β-peptides into Alzheimer’s fibrils[J]. Neuron, 1996, 16(4): 881–891. ▲",
        "De Ferrari G V, Canales M A, Shin I, et al. A structural motif of acetylcholinesterase that promotes amyloid β-peptide fibril formation[J]. Biochemistry, 2001, 40(35): 10447–10457. doi:10.1021/bi0101392",
        "Inestrosa N C, Dinamarca M C, Alvarez A. Amyloid–cholinesterase interactions[J]. The FEBS Journal, 2008, 275(4): 625–632. doi:10.1111/j.1742-4658.2007.06238.x",
        "【待补全】用户稿件中编号 [31] 的文献：AChE–Aβ 复合物 1 μs 分子动力学研究（PAS 之外的多点接触、Aβ 主要停留区段 AChE 344—361）。请按目标期刊格式补全著录信息与 DOI。",
        "Fan X, Zhang X, Yan J, et al. Computational investigation of co-aggregation and cross-seeding between Aβ and hIAPP underpinning the crosstalk in Alzheimer’s disease and type-2 diabetes[J]. Journal of Chemical Information and Modeling, 2024, 64(13): 5303–5316. doi:10.1021/acs.jcim.4c00859",
        "Identification of hybrid amyloid strains assembled from amyloid-β and human islet amyloid polypeptide[J]. Nanotechnology, 2023. doi:10.1088/1361-6528/acf3ee ▲",
        "Perov S, Lidor O, Salinas N, et al. Structural insights into curli CsgA cross-β fibril architecture inspire repurposing of anti-amyloid compounds as anti-biofilm agents[J]. PLoS Pathogens, 2019, 15(8): e1007978. doi:10.1371/journal.ppat.1007978",
        "Sampson T R, Challis C, Jain N, et al. A gut bacterial amyloid promotes α-synuclein aggregation and motor impairment in mice[J]. eLife, 2020, 9: e53111. doi:10.7554/eLife.53111 ▲",
        "Wang C, Lau C Y, Ma F, et al. Genome-wide screen identifies curli amyloid fibril as a bacterial component promoting host neurodegeneration[J]. PNAS, 2021, 118(34): e2106504118. doi:10.1073/pnas.2106504118",
        "Chen S G, Stribinskis V, Rane M J, et al. Exposure to the functional bacterial amyloid protein curli enhances alpha-synuclein aggregation in aged Fischer 344 rats and Caenorhabditis elegans[J]. Scientific Reports, 2016, 6: 34477. doi:10.1038/srep34477",
        "Bhoite S S, Han Y, Ruotolo B T, et al. Mechanistic insights into accelerated α-synuclein aggregation mediated by human microbiome-associated functional amyloids[J]. Journal of Biological Chemistry, 2022, 298(8): 102088. doi:10.1016/j.jbc.2022.102088 ▲",
        "Zhu Y, Lin X, Zong X, et al. Structural basis of FPR2 in recognition of Aβ42 and neuroprotection by humanin[J]. Nature Communications, 2022, 13: 1775. doi:10.1038/s41467-022-29361-x",
        "Wang C, et al. Human antimicrobial peptide LL-37 contributes to Alzheimer’s disease progression[J]. Molecular Psychiatry, 2022. doi:10.1038/s41380-022-01790-6 ▲",
        "De Lorenzi E, Chiari M, Colombo R, et al. Evidence that the human innate immune peptide LL-37 may be a binding partner of amyloid-β and inhibitor of fibril assembly[J]. Journal of Alzheimer’s Disease, 2017, 59(4): 1213–1226. doi:10.3233/JAD-170223 ▲",
        "LL-37 and its truncated fragments modulate amyloid-β dynamics, aggregation and toxicity through hetero-oligomer and cluster formation[J]. 2025. PMID: 40916348 ▲",
        "Soscia S J, Kirby J E, Washicosky K J, et al. The Alzheimer’s disease-associated amyloid β-protein is an antimicrobial peptide[J]. PLoS ONE, 2010, 5(3): e9505. doi:10.1371/journal.pone.0009505",
        "Kumar D K V, Choi S H, Washicosky K J, et al. Amyloid-β peptide protects against microbial infection in mouse and worm models of Alzheimer’s disease[J]. Science Translational Medicine, 2016, 8(340): 340ra72. doi:10.1126/scitranslmed.aaf1059 ▲",
        "Salinas N, Tayeb-Fligelman E, Sammito M D, et al. The amphibian antimicrobial peptide uperin 3.5 is a cross-α/cross-β chameleon functional amyloid[J]. PNAS, 2021, 118(3): e2014442118. doi:10.1073/pnas.2014442118",
        "Bücker R, Seuring C, Cazey C, et al. The cryo-EM structures of two amphibian antimicrobial cross-β amyloid fibrils[J]. Nature Communications, 2022, 13: 4356. doi:10.1038/s41467-022-32039-z",
        "Engelberg Y, Landau M. The human LL-37(17-29) antimicrobial peptide reveals a functional supramolecular structure[J]. Nature Communications, 2020, 11: 3894. doi:10.1038/s41467-020-17736-x",
        "Factors driving amyloid beta fibril recognition by cell surface receptors: a computational study[J]. 2025. PMCID: PMC12566521 ▲",
        "Antimicrobial peptides as cross-seeding modulators at the neurodegenerative–infectious interface[J]. 2026. PMCID: PMC12930082 ▲",
        "Kumar V, Patiyal S, Dhall A, et al. B3Pred: a random-forest-based method for predicting and designing blood–brain barrier penetrating peptides[J]. Pharmaceutics, 2021, 13(8): 1237. doi:10.3390/pharmaceutics13081237 ▲",
        "Prediction of blood-brain barrier-penetrating peptides using B3BPFN[J]. Frontiers in Molecular Biosciences, 2026. doi:10.3389/fmolb.2026.1858506 ▲",
        "Abramson J, Adler J, Dunger J, et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3[J]. Nature, 2024, 630: 493–500. doi:10.1038/s41586-024-07487-9",
        "Honorato R V, Koukos P I, Jiménez-García B, et al. Structural biology in the clouds: the WeNMR-EOSC ecosystem (HADDOCK2.4)[J]. Frontiers in Molecular Biosciences, 2021, 8: 729513. doi:10.3389/fmolb.2021.729513 ▲",
        "Kozakov D, Hall D R, Xia B, et al. The ClusPro web server for protein–protein docking[J]. Nature Protocols, 2017, 12(2): 255–278. doi:10.1038/nprot.2016.169",
        "Zhou P, Jin B, Li H, et al. HPEPDOCK: a web server for blind peptide–protein docking based on a hierarchical algorithm[J]. Nucleic Acids Research, 2018, 46(W1): W443–W450. doi:10.1093/nar/gky357",
        "Huang J, Rauscher S, Nawrocki G, et al. CHARMM36m: an improved force field for folded and intrinsically disordered proteins[J]. Nature Methods, 2017, 14(1): 71–73. doi:10.1038/nmeth.4067",
        "Robustelli P, Piana S, Shaw D E. Developing a molecular dynamics force field for both folded and disordered protein states[J]. PNAS, 2018, 115(21): E4758–E4766. doi:10.1073/pnas.1800690115",
        "Souza P C T, Alessandri R, Barnoud J, et al. Martini 3: a general purpose force field for coarse-grained molecular dynamics[J]. Nature Methods, 2021, 18(4): 382–388. doi:10.1038/s41592-021-01098-3",
        "Abraham M J, Murtola T, Schulz R, et al. GROMACS: high performance molecular simulations through multi-level parallelism from laptops to supercomputers[J]. SoftwareX, 2015, 1–2: 19–25. doi:10.1016/j.softx.2015.06.001",
        "Jo S, Kim T, Iyer V G, et al. CHARMM-GUI: a web-based graphical user interface for CHARMM[J]. Journal of Computational Chemistry, 2008, 29(11): 1859–1865. doi:10.1002/jcc.20945",
        "Laio A, Parrinello M. Escaping free-energy minima[J]. PNAS, 2002, 99(20): 12562–12566. doi:10.1073/pnas.202427399",
        "Wang L, Friesner R A, Berne B J. Replica exchange with solute scaling: a more efficient version of REST (REST2)[J]. The Journal of Physical Chemistry B, 2011, 115(30): 9431–9438. doi:10.1021/jp204407d",
        "Kumari R, Kumar R, Open Source Drug Discovery Consortium, et al. g_mmpbsa—a GROMACS tool for high-throughput MM-PBSA calculations[J]. Journal of Chemical Information and Modeling, 2014, 54(7): 1951–1962. doi:10.1021/ci500020m",
        "Diener C, Gibbons S M, Resendis-Antonio O. MICOM: metagenome-scale modeling to infer metabolic interactions in the gut microbiota[J]. mSystems, 2020, 5(1): e00606-19. doi:10.1128/mSystems.00606-19",
        "Yang J, Liang J, Hu N, et al. The gut microbiota modulates neuroinflammation in Alzheimer’s disease: elucidating crucial factors and mechanistic underpinnings[J]. CNS Neuroscience & Therapeutics, 2024, 30(10): e70091. doi:10.1111/cns.70091",
        "Wasén C, Beauchamp L C, Vincentini J, et al. Bacteroidota inhibit microglia clearance of amyloid-beta and promote plaque deposition in Alzheimer’s disease mouse models[J]. Nature Communications, 2024, 15: 3872. ▲",
        "Meisl G, Kirkegaard J B, Arosio P, et al. Molecular mechanisms of protein aggregation from global fitting of kinetic models[J]. Nature Protocols, 2016, 11(2): 252–272. doi:10.1038/nprot.2016.010",
        "Cohen S I A, Linse S, Luheshi L M, et al. Proliferation of amyloid-β42 aggregates occurs through a secondary nucleation mechanism[J]. PNAS, 2013, 110(24): 9758–9763. doi:10.1073/pnas.1218402110",
        "Evans R, O’Neill M, Pritzel A, et al. Protein complex prediction with AlphaFold-Multimer[EB/OL]. bioRxiv, 2022. doi:10.1101/2021.10.04.463034",
        "Matsuzaki K. Aβ–ganglioside interactions in the pathogenesis of Alzheimer’s disease[J]. Biochimica et Biophysica Acta – Biomembranes, 2020, 1862(8): 183233. doi:10.1016/j.bbamem.2020.183233 ▲",
        "Farris W, Mansourian S, Chang Y, et al. Insulin-degrading enzyme regulates the levels of insulin, amyloid β-protein, and the β-amyloid precursor protein intracellular domain in vivo[J]. PNAS, 2003, 100(7): 4162–4167. doi:10.1073/pnas.0230450100",
        "Iwata N, Tsubuki S, Takaki Y, et al. Metabolic regulation of brain Aβ by neprilysin[J]. Science, 2001, 292(5521): 1550–1552. doi:10.1126/science.1059946",
        "Li X, Masliah E, Reixach N, et al. Neuronal production of transthyretin in human and murine Alzheimer’s disease: is it protective?[J]. Journal of Neuroscience, 2011, 31(35): 12483–12490. ▲",
        "Wang J, Gu B J, Masters C L, et al. A systemic view of Alzheimer disease—insights from amyloid-β metabolism beyond the brain[J]. Nature Reviews Neurology, 2017, 13(10): 612–623. doi:10.1038/nrneurol.2017.111",
        "Xiang Y, Bu X L, Liu Y H, et al. Physiological amyloid-beta clearance in the periphery and its therapeutic potential for Alzheimer’s disease[J]. Acta Neuropathologica, 2015, 130(4): 487–499. ▲",
    ]
    for i, r in enumerate(refs, 1):
        reference(doc, i, r)
    para(doc, "注：标注 ▲ 的条目为本文在检索环境下未能逐字核对卷期页码的文献，投稿前请用 DOI/PMID 复核；标注【待补全】的条目需由作者提供原稿信息。",
         size=8.5, indent_chars=0, space_before=4, line=1.25)

    # ---------------- 附录
    doc.add_page_break()
    h1(doc, "附录 A  本文写作过程中使用的 Agent Skills（find-skills 检索结果）")
    para(doc, "按 vercel-labs 的 find-skills 工作流执行：理解意图 → 检索技能注册表 → 核验来源 → 呈现候选 → 安装。"
              "受当前网络环境限制，skills.sh 注册表与 npx skills find 不可达（返回空结果），因此改为对已安装的本地技能目录"
              "（Light Skills 23 个 + K-Dense scientific-agent-skills 若干）执行离线检索，脚本见 "
              "projects/amp-ad-mechanism/scripts/skill_finder.py。下表为与本任务相关度最高的技能及其在本文中的实际用途。",
         indent_chars=2.0, size=9.5)
    add_table(
        doc,
        ["技能", "来源", "在本文中的用途"],
        [
            ["find-skills", "vercel-labs/skills", "技能路由与发现；本文按其六步流程执行（注册表不可达时降级为本地检索）"],
            ["molecular-dynamics", "K-Dense scientific-agent-skills", "M1–M7 的 MD 方案设计：体系搭建、力场选择、轨迹分析（RMSD/RMSF/接触图/自由能面）"],
            ["diffdock", "K-Dense scientific-agent-skills", "对接环节的工具对照（DiffDock 适用于小分子；肽–蛋白改用 HADDOCK/HPEPDOCK/AF-Multimer）"],
            ["esm", "K-Dense scientific-agent-skills", "Stage 0–1：ESM 嵌入与 ESMFold 结构生成，用于序列分诊与构象系综"],
            ["pkpd-modeling", "K-Dense scientific-agent-skills", "第 5 节 PBPK 三室暴露模型与 Kp,uu 估计"],
            ["literature-review / paper-lookup", "K-Dense scientific-agent-skills", "范式检索与文献元数据核验"],
            ["scientific-writing / docx", "K-Dense、Anthropic", "稿件结构、证据溯源与 Word 期刊格式排版"],
            ["light-literature-search", "Light Skills", "三层检索（前沿/奠基/跨领域方法移植），产出第 2 节的范式地图"],
            ["light-idea-critique", "Light Skills", "第 6 节审稿攻击点与一票否决式自审"],
            ["light-research-plan", "Light Skills", "第 3–4 节的实验矩阵、判据阈值与预注册口径"],
            ["light-citation", "Light Skills", "参考文献核验与 ▲ 标注规则（查不到就标待核查，不臆造）"],
            ["light-paper-writing / light-consistency", "Light Skills", "论文叙事线、措辞强度与跨材料一致性检查"],
        ],
        widths=[3.6, 4.0, 7.6],
        size=8.5,
    )

    h1(doc, "附录 B  缩略语")
    add_table(
        doc,
        ["缩写", "全称", "中文"],
        [
            ["AMP", "antimicrobial peptide", "抗菌肽"],
            ["AD", "Alzheimer’s disease", "阿尔茨海默病"],
            ["AChE / PAS", "acetylcholinesterase / peripheral anionic site", "乙酰胆碱酯酶 / 外周阴离子位点"],
            ["Aβ", "amyloid-β", "β-淀粉样蛋白"],
            ["BBB / RMT", "blood-brain barrier / receptor-mediated transcytosis", "血脑屏障 / 受体介导转胞吞"],
            ["MD / CG-MD", "molecular dynamics / coarse-grained MD", "分子动力学 / 粗粒化分子动力学"],
            ["REST2 / PMF", "replica exchange with solute scaling / potential of mean force", "溶质缩放副本交换 / 平均力势"],
            ["MM/PBSA", "molecular mechanics Poisson-Boltzmann surface area", "分子力学泊松-玻尔兹曼表面积法"],
            ["FBA", "flux balance analysis", "通量平衡分析"],
            ["SCFA / LPS", "short-chain fatty acid / lipopolysaccharide", "短链脂肪酸 / 脂多糖"],
            ["ThT / TEER", "thioflavin T / transepithelial electrical resistance", "硫黄素 T / 跨上皮电阻"],
        ],
        widths=[2.6, 7.0, 5.6],
        size=8.5,
    )

    out = OUT / "抗菌肽-阿尔茨海默病-机制关联框架.docx"
    doc.save(out)
    return out


if __name__ == "__main__":
    p = build()
    print("wrote", p)
