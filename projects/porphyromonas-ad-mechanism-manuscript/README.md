# 口腔微肽与牙周炎—阿尔茨海默病机制研究稿件包

## 当前版本

v3.15.0在核对图件与本地三次Vina/100 ns对比CSV数字一致的前提下，为独立分子对接与分子动力学报告新增简洁版和中间版。三版（简洁/中间/完整）中英各一份，**全部嵌入同一套7幅PNG**（图1打分、图2/图3构象、图S1总览、图4–6三套apo–复合物100 ns对比图），核心数值不改写。对接打分同时报告最优单次亲和力（-8.25 至 -9.60 kcal/mol）与三次成功运行均值±标准差（-8.07 ± 0.16 至 -9.44 ± 0.09 kcal/mol，n = 3）；最优构象排序仍以FLLHTTR为最强（-9.60 kcal/mol），均值排序则以YLSLLQR为最强（-9.44 ± 0.09 kcal/mol），并明示FLLHTTR三次运行离散度最大（-8.77 ± 1.41 kcal/mol）。各报告均从“分析方法/Analysis methods”起始，无显示标题、摘要、关键词或引言；分析方法与结果章节不含引文标记，讨论章节引用高分SCI经典文献。版本对照与图文核对见 `manuscript/md_alllhrc/VERSIONS.md`。六份口腔smORF筛选DOCX逐字节保持不变，且不导入任何对接或动力学结果。

当前交付物均提供彼此分离的英文、中文DOCX及Markdown源文件：

- 筛选完整稿：`manuscript/full/{English,Chinese}.{docx,md}`
- 筛选中间稿：`manuscript/intermediate/{English,Chinese}.{docx,md}`
- 筛选简洁稿：`manuscript/concise/{English,Chinese}.{docx,md}`
- 独立对接与MD完整/中间/简洁报告：`manuscript/md_alllhrc/{full,intermediate,concise}/{English,Chinese}.{docx,md}`（三版均带图；对照见 `manuscript/md_alllhrc/VERSIONS.md`）

筛选稿完整、中间和简洁三个版本均采用无标题、单段非结构式摘要起始；包含Introduction、Materials and methods、Results、Discussion和References，不设独立“统计分析”小节或“结论”章节。完整稿含6个三线表、约6,900个英文正文词和55条参考文献；中间稿含4个三线表、约4,600个英文正文词和40条参考文献；简洁稿含3个三线表、约3,700个英文正文词和22条参考文献。

独立MD报告是明确例外：DOCX直接从`Analysis methods`或`分析方法`开始，仅含分析方法、结果和讨论三个一级章节；无显示标题、摘要、关键词、引言、统计分析章节或独立结论。分析方法与结果章节不含引文标记，讨论部分引用高分SCI文献解释致病肽导致AD的分子机制。每份报告保留3个三线表（表1：12条微肽本地三次Vina最优打分、均值±SD、氢键与PAS结合；表2：apo AChE与三种复合物100 ns动力学指标，与图4–6面板对齐；表3：证据边界）。完整版表2为13行，中间版8行，简洁版6行；三版核心数字相同。

六份筛选DOCX不含页眉、页脚、页码、批注或嵌入图像。六份独立对接与MD报告同样不含页眉、页脚、页码或批注，但在正文中嵌入同一套7幅PNG图（图1打分图、图2/图3最优构象、图S1总览、图4–6三套100 ns动力学对比图）；高分辨率原图仍保存在`manuscript/figures/`。全部DOCX使用12磅正文、双倍行距和1英寸页边距。正文普通段落采用480 twip首行缩进，摘要、章节标题、图题、表题、表格和参考文献等非普通正文元素不缩进。所有表格仅保留顶线、表头下横线和底线，不使用竖线、内部正文横线或表头底色。

## 科学定位

项目以`source_materials/材料与方法及结果_机制研究版.docx`为主要筛选科学材料，报告纯计算、汇总层面的口腔smORF候选优选。候选级联包括UniDL4BioPep的ESM-2/CNN、NTxPred2肽模式的ESM2-t30微调模型、mebipred两级人工神经网络和AnOxPePred多任务一维CNN。

筛选稿三个版本均支持描述性漏斗、12条独立序列的组成核对及现有AChE Vina评分排序，但不支持牙周炎特异性、*Porphyromonas gingivalis*来源、当前队列表达、BBB通过、神经毒性、金属化学、AChE结合/功能、AD机制或因果关系。中间版保留完整的22项长/短肽多维结果、级联计数、12条序列与评分及长肽流失局限，但压缩文献综合和验证细节。

主源中的长肽和短肽多维功能输出均已恢复。流程局限明确披露：牙周炎标记分支中72条经宏蛋白质组支持、去重且BBB高分的31–50 aa长肽均未进入NTxPred2阳性集合；923条NTxPred2阳性序列全部≤30 aa，因而后续金属结合与CHEL/FRS网页预测及最终12条汇总候选只保留短肽。这不能证明长肽没有神经毒性或金属相关活性，而可能反映串行阈值、模型适用性/校准和网页预测器实现方式。

独立对接与MD包系统性揭示：
1. 本地三次Vina运行显示12条候选微肽均具有有利预测亲和力。最优单次打分介于 -8.25 至 -9.60 kcal/mol；三次运行均值介于 -8.07 ± 0.16 至 -9.44 ± 0.09 kcal/mol。最优构象呈现明确的PAS位点对接特征：FLLHTTR、YLSLLQR、LLHPLRL、FCLHLQLR、HVLLLRQCA、HLLTLKKHV直接对接至PAS位点（Tyr72、Asp74、Thr75、Trp286、His287、Tyr341等）。FLLHTTR最优构象打分最高（-9.60 kcal/mol）且密集结合PAS核心，但其三次运行SD最大（1.41 kcal/mol）；YLSLLQR三次运行均值最强（-9.44 ± 0.09 kcal/mol）并双重锚定PAS与催化入口；LLHPLRL形成多达10个氢键的双位点跨越式结合（纵贯PAS与催化三联体His447），三次运行SD最小（0.05 kcal/mol）；ALLLHRC结合于催化中心Ser203及峡部颈部，均值仍居前列（-9.18 ± 0.11 kcal/mol）。
2. 100 ns全原子GROMACS模拟（apo AChE vs ALLLHRC、FLLHTTR、YLSLLQR）证实：AChE受体骨架保持紧致稳定（RMSD < 0.22 nm，Rg保持在2.29–2.32 nm，α-螺旋与β-折叠片层比例基本恒定），微肽结合主要引发PAS周围表面环区的局部动态柔性重构（RMSF微增）；复合物在产物阶段全程维持持续性界面氢键（后20 ns平均2.2–4.2个）与7对特征接触，RDF呈现强局域质心聚集（g(r)高达43–213），证实肽段稳定吸附于受体表面。
3. 讨论部分结合Atanasova et al. (2020)、Dominy et al. (2019, Sci. Adv.)、Silman & Sussman (2005)、Inestrosa et al. (1996, 2008)、Hampel et al. (2018)、Bartus et al. (1982)及Selkoe & Hardy (2016)等高分SCI文献，深入阐释致病肽穿越破损血脑屏障、占位阻断AChE PAS活性峡部（引发胆碱能突触失能）并作为异源病理性伴侣“种子”加速Aβ聚集与神经毒性级联放大的整合AD分子病理机制。

筛选正文不报告具体参与者、标本、组装分析或MAG总数。用户说明的296个MAG在`evidence/mag_count_audit.md`中保留为待核查信息，未进入稿件。

## 图、表与引文

`manuscript/figures/`保留完整的图件集合：
- `fig5_docking_scores.{png,svg}`：本地三次Vina运行均值±SD与最优单次打分图（正文引用为图1 / Figure 1）；
- `fig_docking_poses_A_F.png`：ALLLHRC至HVLLLRQCA最优构象（图2 / Figure 2，A–F）；
- `fig_docking_poses_G_L.png`：LLHLPKRTT至YLSLLQR最优构象（图3 / Figure 3，G–L）；
- `fig_docking_poses_12_combined.png`：12条微肽最优构象总览（图S1 / Figure S1）；
- `fig_compare_ache_vs_alllhrc.{png,svg,pdf}`：apo AChE单体与AChE–ALLLHRC复合物100 ns对比图（正文引用为图4 / Figure 4）；
- `fig_compare_ache_vs_fllhttr.{png,svg,pdf}`：apo AChE单体与AChE–FLLHTTR复合物100 ns对比图（正文引用为图5 / Figure 5）；
- `fig_compare_ache_vs_ylsllqr.{png,svg,pdf}`：apo AChE单体与AChE–YLSLLQR复合物100 ns对比图（正文引用为图6 / Figure 6）；
- `prioritization_funnel.{png,svg}`、`evidence_ladder.{png,svg}`：筛选流程与证据阶梯图。

筛选稿DOCX不嵌入图像。独立对接与MD报告在图题前嵌入对应PNG，便于直接阅读；高分辨率原图同时作为独立文件存放。

六份筛选Markdown使用Pandoc格式的BibTeX键并链接`references/references.bib`；标准库DOCX构建器生成连续编号的Vancouver式缓存文字。六份独立对接与MD报告在方法与结果部分不含引文标记，在讨论部分引用高分SCI经典文献并附参考文献列表。

相关Zotero验收工具与说明位于：

- `scripts/test_better_bibtex.py`
- `scripts/build_zotero_live_docx.py`
- `references/ZOTERO_WORD_ACCEPTANCE.md`
- `quality_reports/zotero_live_status.json`

## 可重复构建

从项目根目录运行：

```bash
for language in English Chinese; do
  python3 scripts/build_docx_stdlib.py --clean-manuscript --timestamp 2026-08-17T00:00:00Z --bibliography references/references.bib --input "manuscript/full/${language}.md" --output "manuscript/full/${language}.docx" --title "${language}"
  python3 scripts/build_docx_stdlib.py --clean-manuscript --timestamp 2026-08-23T00:00:00Z --bibliography references/references.bib --input "manuscript/intermediate/${language}.md" --output "manuscript/intermediate/${language}.docx" --title "${language}"
  python3 scripts/build_docx_stdlib.py --clean-manuscript --timestamp 2026-08-17T00:00:00Z --bibliography references/references.bib --input "manuscript/concise/${language}.md" --output "manuscript/concise/${language}.docx" --title "${language}"
  for version in full intermediate concise; do
    python3 scripts/build_docx_stdlib.py --clean-manuscript --allow-images --timestamp 2026-08-23T00:00:00Z --input "manuscript/md_alllhrc/${version}/${language}.md" --output "manuscript/md_alllhrc/${version}/${language}.docx" --title "${language}"
  done
done
```

## 当前审计

```bash
python3 scripts/verify_source_checksums.py
python3 scripts/audit_excluded_source_scope.py
python3 scripts/stage5_statistics_audit.py
python3 scripts/audit_external_docking_summary.py
python3 scripts/audit_submission_manuscripts.py
python3 scripts/audit_full_manuscripts.py
python3 scripts/audit_intermediate_package.py
python3 scripts/audit_concise_package.py
python3 scripts/audit_docx_packages.py
python3 scripts/audit_full_docx_reproducibility.py
python3 scripts/audit_citation_inventory.py
python3 scripts/audit_language_structure.py
python3 scripts/audit_manuscript_consistency.py
python3 scripts/audit_manuscript_word_counts.py
python3 scripts/audit_text_quality.py
python3 scripts/audit_md_alllhrc_package.py
```
