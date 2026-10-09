# Manuscript version history / 稿件版本记录

> Purpose: maintain one authoritative index of every material manuscript revision, its Git checkpoint, evidence status, deliverables, and recovery method.  
> 用途：以单一权威文件记录每次实质性稿件版本、Git检查点、证据状态、交付物和恢复方法。

## 1. Versioning convention / 版本规则

Tag pattern / 标签格式：

```text
porphyromonas-ad-manuscript-vMAJOR.MINOR.PATCH
```

- **MAJOR / 主版本：** evidence architecture, research question, or manuscript structure changes materially. / 证据架构、研究问题或全文结构发生实质改变。
- **MINOR / 次版本：** new analyses, figures, references, submission documents, or evidence-controlled external integration. / 新增分析、图件、文献、投稿材料或受控外部整合。
- **PATCH / 修订版本：** wording, translation, formatting, metadata, or non-substantive corrections. / 措辞、翻译、格式、元数据或非实质性修正。

Rules / 规则：

1. Update this file before creating a release tag. / 创建标签前先更新本文件。
2. Use annotated tags and push them explicitly. / 使用带说明的annotated tag并显式推送。
3. Never move, overwrite, or reuse an existing release tag. / 不移动、不覆盖、不复用既有版本标签。
4. A tag freezes a recoverable project snapshot; later edits require a new version. / 标签冻结可恢复快照，后续修改必须使用新版本。
5. Manuscript version numbers are independent of the external repository’s “v0.4” label. / 本稿版本号与外部仓库“v0.4”标签相互独立。

## 2. Version ledger / 版本台账

| Manuscript version | Date | Git checkpoint | Release tag | Status | Main content |
| --- | --- | --- | --- | --- | --- |
| **v0.1.0 — source intake** | 2026-08-12 | `f6a020a5c98b243b13963a8de83cd859f52e132d` | Untagged historical checkpoint | Superseded | Initial project materials entered Git management. / 初始研究材料纳入Git管理。 |
| **v0.2.0 — source parsing** | 2026-08-12 | `956210917503cfd2f521c80feeb4eb9aecbf8028` | Untagged historical checkpoint | Superseded | Principal documents parsed and source provenance registered. / 解析主要文档并登记来源。 |
| **v1.0.0 — first bilingual draft** | 2026-08-12 | `1fd8ab3bdf616fd1ab7b0e70d7c71046fb43da58` | Untagged historical checkpoint | Superseded | First English–Chinese SCI draft and initial quality review. / 首版中英文SCI稿与质量检查。 |
| **v2.0.0 — nine-stage aggregate rebuild** | 2026-08-12 | `a31d29466dc8d376d6012abd916152eb82e017f1` | Untagged historical checkpoint | Superseded | Nine-stage reconstruction, 25-reference corpus, aggregate-only evidence boundary, figures, DOCX and submission package. / 九阶段重建、25条文献、汇总证据边界、图件、DOCX及投稿包。 |
| **v3.0.0 — external-v0.4 evidence integration** | 2026-08-12 | Manuscript content commit `2a7573604b6e12bd1d51b897d52c58f0d9ead077`; release-management commit `012d0cbcd3c45a26aed0adf9ba9bce2f70e4844b` | `porphyromonas-ad-manuscript-v3.0.0` | **Frozen prior full release** | Expanded 53-reference parallel manuscript; twelve externally reported sequences; independently recomputed composition; source-reported AChE docking summary; three figures; six supplementary tables; revision-v3 workflow, provenance controls and deterministic audits. / 扩展至53条文献；整合12条外部报告序列、组成审计、来源报告AChE对接汇总、三幅主图、六个补充表、revision-v3工作流及确定性审计。 |
| **v3.1.0 — initial concise package** | 2026-08-14 | `ef8493c8d26f31fefef6ad6e79ca31a412d4af0a` | `porphyromonas-ad-manuscript-v3.1.0` | **Frozen prior concise release** | Added separate short English and Chinese SCI-style DOCX files with two tables, one figure and 20 selected references. / 新增英文、中文独立DOCX精简稿，保留两表、一图和20条精选文献。 |
| **v3.2.0 — provenance-verified clean concise package** | 2026-08-14 | `273e352a5b92620df66e482b30fbd759472fad8b` | `porphyromonas-ad-manuscript-v3.2.0` | **Frozen prior concise release** | Renamed deliverables to `English.docx` and `Chinese.docx`; removed headers, footers, page-number fields and workflow metadata; rebuilt the AD–*P. gingivalis* Introduction; documented predictor algorithms; and corrected the PRJNA678453/PRJEB65451 provenance to 11 healthy plus 11 periodontitis participants and 66 specimens. / 采用中性文件名，删除页眉页脚页码及流程元数据，重构AD—*P. gingivalis*引言，补充预测算法，并核正来源队列为11名健康对照、11名牙周炎患者及66份标本。 |
| **v3.3.0 — SCI-style Introduction and deep-learning-guided Methods** | 2026-08-14 | `e8c16c630d658424e8656ea89aa1c9c52cc33966` | `porphyromonas-ad-manuscript-v3.3.0` | **Frozen prior concise release** | Rewrote the Introduction with individually bracketed references [1]–[10]; reorganized Methods into conventional SCI subsections; and emphasized the relevant deep-learning peptide modes—ESM-2/CNN, fine-tuned ESM2-t30 and multi-task 1D CNN—while retaining the neural-network and evidence boundaries. / 引言采用[1]–[10]逐篇独立引用；方法按SCI结构重组；突出ESM-2/CNN、微调ESM2-t30和多任务一维CNN等肽分析深度学习模式，同时保留神经网络及证据边界。 |
| **v3.4.0 — separate provenance-corrected full manuscripts** | 2026-08-17 | `918f7f9abf531c467b83a409ba5ccd4e86cd4c76` | `porphyromonas-ad-manuscript-v3.4.0` | **Frozen prior full release** | Added separate neutral `English.docx` and `Chinese.docx` full manuscripts with abstract, AD-first Introduction, complete Methods/Results/Discussion/Conclusions, declarations, four tables, three figures, and 53 verified references; carried forward the corrected PRJNA678453/PRJEB65451 provenance and model-specific architecture descriptions; removed headers, footers, page fields, draft notes, purpose-facing text, and the unsupported cohort/assembly summary. / 新增中性命名的独立英文、中文完整稿，含摘要、AD起始引言、完整方法/结果/讨论/结论、声明、四表、三图和53条核验文献；继承来源与模型架构修正，并删除页眉、页脚、页码域、草稿说明、用途性文字及无依据的队列/组装汇总。 |
| **v3.5.0 — review-grade Introduction and prospective MD methods** | 2026-08-17 | The annotated tag resolves the final v3.5.0 release commit | `porphyromonas-ad-manuscript-v3.5.0` | **Frozen prior full release** | Replaced the abstract with a concise high-impact-SCI narrative; expanded the Introduction through evidence-class synthesis; omitted participant, specimen, assembly-analysis and MAG totals from the article bodies; registered the user-derived 296-MAG value as pending audit; added a versioned prospective 100-ns GROMACS protocol without MD results; hid the visible article title; retained no headers, footers, page fields or comments; and audited editable-text SVG sources. / 采用高水平SCI叙事摘要和证据综合型扩展引言；正文省略参与者、标本、组装分析和MAG总数；将用户原始映射所得296个MAG登记为待审计；新增版本化100 ns GROMACS前瞻性方案但不加入MD结果；隐藏正文标题并保持无页眉、页脚、页码和批注；审计可编辑文字SVG。 |
| **v3.6.0 — clean full and concise submission variants** | 2026-08-17 | The annotated tag resolves the final v3.6.0 release commit | `porphyromonas-ad-manuscript-v3.6.0` | **Frozen prior release** | Rebuilt complete and concise English/Chinese manuscripts; converted every table to a three-line structure; removed figures from all four DOCX files; ended each article at Conclusion followed directly by References; removed evidence-tier, hash, commit, archive, acceptance and workflow-governance prose from article bodies; and converted source citations to Pandoc/BibTeX keys with an explicit Better BibTeX/Word acceptance gate. / 重建完整与精简中英文稿；全部表格改为三线表；四份DOCX移除所有图像；结论后直接进入参考文献；正文删除证据分层、哈希、提交、归档、接纳和工作流治理表述；正文引文改为Pandoc/BibTeX键，并设置明确的Better BibTeX/Word验收门。 |
| **v3.7.0 — journal-aligned manuscripts and expanded concise variants** | 2026-08-17 | The annotated tag resolves the final v3.7.0 release commit | `porphyromonas-ad-manuscript-v3.7.0` | **Frozen prior release** | Reframed the ongoing MD work as a pending analysis extension whose trajectory measurements will be integrated after completion; removed “no MD result” wording; expanded the concise English body by approximately 74% with synchronized Chinese content; adopted structured abstracts, unnumbered IMRaD headings, 12-point Times New Roman, double spacing and one-inch margins; retained figure-free DOCX files, three-line tables and Conclusion-to-References order. / 将MD表述修正为正在进行、完成后补充轨迹指标的分析扩展，删除“不报告MD结果”措辞；精简英文正文扩展约74%并同步中文；采用结构式摘要、无编号IMRaD标题、12磅Times New Roman、双倍行距和1英寸页边距；继续保持DOCX无图、三线表及结论后直接进入参考文献。 |
| **v3.8.0 — single-paragraph abstracts and simplified article ending** | 2026-08-17 | The annotated tag resolves the final v3.8.0 release commit | `porphyromonas-ad-manuscript-v3.8.0` | **Frozen prior release** | Converted all four abstracts to one unlabelled paragraph and removed their Conclusions components; removed the Statistical analysis subsection and standalone Conclusion section; made Discussion proceed directly to References; added a 480-twip first-line indent to ordinary main-text paragraphs while retaining unindented abstracts and non-body elements; preserved synchronized science, ongoing-MD language, figure-free DOCX files and three-line tables. / 四稿摘要改为单段无标签形式并删除摘要结论内容；删除“统计分析”小节和独立“结论”章节，使讨论后直接进入参考文献；正文普通段落增加480 twip首行缩进，摘要及非正文元素保持顶格；继续保持中英文科学同步、MD正在分析、DOCX无图和三线表。 |
| **v3.9.0 — restored multidimensional long/short results and attrition limitation** | 2026-08-17 | The annotated tag resolves the final v3.9.0 release commit | `porphyromonas-ad-manuscript-v3.9.0` | **Frozen prior screening release** | Restored all 22 principal-source UniDL4BioPep functional outputs for both long and short branches in all four manuscripts; retained exact counts and percentages in separate full-version tables and a compact concise table; documented that all 72 metaproteome-supported, dereplicated long BBB-high candidates were absent from the all-≤30-aa NTxPred2-positive set, so downstream metal/CHEL/FRS screening and the final aggregate 12 retained only short peptides; treated this as a serial-pipeline limitation rather than biological inactivity. / 四稿恢复主源长肽与短肽各22项UniDL4BioPep功能输出，完整稿分别列表、精简稿合并列表并保留精确计数与比例；明确72条经宏蛋白质组支持、去重且BBB高分的长肽均未进入全部≤30 aa的NTxPred2阳性集合，故后续金属/CHEL/FRS筛选及最终12条仅保留短肽；将其界定为串行流程局限，而非长肽无生物活性。 |
| **v3.10.0 — standalone ALLLHRC–AChE MD package** | 2026-08-23 | The annotated tag resolves the final v3.10.0 release commit | `porphyromonas-ad-manuscript-v3.10.0` | **Frozen prior project release** | Preserved the four v3.9.0 screening DOCX files byte-for-byte and added separate full/concise English/Chinese manuscripts for the user-designated 100-ns ALLLHRC–AChE trajectory; interpreted RMSD, RMSF, center-of-mass RDF, SASA, secondary-structure fractions and hydrogen bonds using Atanasova et al. as a framework; disclosed that the RMSD diagnostic is digitized, the plot retains an inherited Aβ title, and raw/replicate data are incomplete; kept every new DOCX titleless and figure-free. / 原v3.9.0四份筛选DOCX逐字节保持不变；新增用户指定ALLLHRC–AChE 100 ns轨迹的完整/简洁中英文独立稿；以Atanasova等为框架解释RMSD、RMSF、质心RDF、SASA、二级结构比例和氢键；披露RMSD诊断来自数字化曲线、图标题继承Aβ文字且原始/重复数据不完整；新增DOCX继续无标题、无图。 |
| **v3.11.0 — intermediate submission manuscripts** | 2026-08-23 | The annotated tag resolves the final v3.11.0 release commit | `porphyromonas-ad-manuscript-v3.11.0` | **Frozen prior project release** | Added separate English/Chinese intermediate screening manuscripts positioned between the full and concise variants, with approximately 4,600 English main-text words, 40 references and four three-line tables; retained all 22 paired long/short multidimensional outputs, funnel counts, the twelve-sequence composition/docking summary and the long-peptide attrition limitation; excluded the new standalone MD result and created no intermediate MD variant; preserved all pre-existing full, concise and MD DOCX hashes. / 在筛选论文完整稿与简洁稿之间新增独立中英文中间版，含约4,600个英文正文词、40条参考文献和4个三线表；保留全部22项长/短肽配对多维结果、漏斗计数、12条序列组成/对接汇总和长肽流失局限；不纳入新的独立MD结果，也不创建MD中间版；既有完整、简洁和MD DOCX哈希保持不变。 |
| **v3.12.0 — full-only methods/results/discussion MD reports** | 2026-08-23 | The annotated tag resolves the final v3.12.0 release commit | `porphyromonas-ad-manuscript-v3.12.0` | **Frozen prior project release** | Reduced the standalone ALLLHRC–AChE package to separate full English and Chinese reports; deleted the concise MD variant; removed the title, abstract, keywords, Introduction, citation apparatus and References; retained only detailed Analysis methods, Results and Discussion with two three-line tables and explicit evidence limits; preserved all six full/intermediate/concise screening DOCX files byte-for-byte and did not import MD findings into them. / 独立ALLLHRC–AChE包仅保留完整英文、中文报告并删除MD简洁版；删除显示标题、摘要、关键词、引言、引文体系和参考文献；仅保留详细分析方法、结果、讨论、两个三线表及明确证据边界；六份完整/中间/简洁筛选DOCX逐字节不变，且不导入MD结果。 |
| **v3.13.0 — expanded molecular docking and multi-system MD reports** | 2026-08-27 | The annotated tag resolves the final v3.13.0 release commit | `porphyromonas-ad-manuscript-v3.13.0` | **Frozen prior project release** | Expanded the standalone docking and MD report package to begin from molecular docking of all 12 candidate micropeptides against human AChE (PDB 4EY6) with detailed PAS engagement analysis, and integrated 100-ns GROMACS MD comparisons across unliganded apo AChE and three pathogenic complexes (ALLLHRC, FLLHTTR, YLSLLQR); in-text cited docking and MD comparison figures (Figures 1–4 / 图1–4); Methods and Results contain no citation markup; Discussion cites high-impact SCI literature explaining the oral–brain axis, BBB breach, PAS blockade (cholinergic deficit), and AChE pathological chaperone amyloid co-nucleation in AD; retained 3 three-line tables; preserved all six screening DOCX files byte-for-byte. / 扩展独立对接与MD报告包：从12条微肽针对人AChE的分子对接及PAS结合分析开始，整合apo AChE与三种致病复合物（ALLLHRC、FLLHTTR、YLSLLQR）的100 ns全原子MD多系统对比分析；正文引用对接与MD对比图件（图1–4）；方法与结果不含引文，讨论系统引用高分SCI文献深入阐明BBB跨越、PAS阻断、胆碱能失能及AChE病理性伴侣共成核的AD致病机制；保留3个三线表；六份筛选DOCX逐字节不变。 |
| **v3.14.0 — local three-run Vina scores and pose composites** | 2026-08-27 | Content commit on `arena/01a04122-light-skills` | Untagged session checkpoint | **Current project release** | Rebuilt the standalone full English/Chinese docking and MD reports from the user-uploaded local three-run AutoDock Vina summary and best-pose composites; reports best-run affinity and mean±SD (n=3) separately; cites score chart, pose panels A–F/G–L, combined overview, and three MD comparisons (Figures 1–6, Figure S1 / 图1–6、图S1); discloses FLLHTTR run-to-run dispersion (1.41 kcal/mol) and that PDBQT/config logs are not archived; preserved all six screening DOCX files byte-for-byte. / 以用户上传的本地三次Vina汇总表与最优构象复合图重建独立完整中英文对接与MD报告；分别报告最优单次打分与三次运行均值±SD；正文引用打分图、A–F/G–L构象图、12肽总览及三套MD对比图（图1–6、图S1）；披露FLLHTTR三次运行离散度（1.41 kcal/mol）及PDBQT/配置日志未归档；六份筛选DOCX逐字节不变。 |

## 3. Scientific status and package relationship / 科学状态与版本关系

**v3.0.0–v3.13.0 screening manuscripts support / 筛选稿可支持：**

- principal-source aggregate funnel and recomputed descriptive percentages;
- twelve externally reported 7–9-aa sequence strings and independently recomputed composition;
- externally reported Vina mean±SD ordering against human AChE PDB 4EY6;
- a versioned 100-ns GROMACS extension whose comparative trajectory analysis and integration remain pending;
- a provenance-aware, hypothesis-generating validation roadmap.

**The separate v3.14.0 molecular docking and MD package supports / 独立对接与MD报告支持：**

- local three-run AutoDock Vina summary of all 12 candidate micropeptides against human recombinant AChE (PDB 4EY6), reporting best-run affinities (-8.25 to -9.60 kcal/mol) and mean±SD across three successful runs (-8.07 ± 0.16 to -9.44 ± 0.09 kcal/mol), plus best-pose hydrogen bonds (3–10) and residue-specific PAS engagement;
- explicit identification of micropeptides that dock into the canonical PAS (FLLHTTR, YLSLLQR, FCLHLQLR, HVLLLRQCA, HLLTLKKHV, LLHPLRL) versus catalytic/gorge neck binders (ALLLHRC, YHHLLCRR);
- dual-site spanning architecture of LLHPLRL (bridging PAS Trp286/Tyr341 to catalytic His447 with 10 hydrogen bonds);
- multi-system 100-ns all-atom GROMACS MD comparison of unliganded apo AChE vs three pathogenic complexes (ALLLHRC, FLLHTTR, YLSLLQR), confirming receptor globular stability (RMSD < 0.22 nm, Rg 2.29–2.32 nm, conserved α-helix ~33–34% and β-sheet ~17%), localized PAS loop flexibility (RMSF), persistent intermolecular hydrogen bonds (2.2–4.2 bonds), 7 persistent contact pairs, and strong center-of-mass spatial localization (g(r) 43–213);
- in-text citations of the local score chart, best-pose composites (A–F, G–L, combined overview), and multi-panel MD trajectory comparison figures (Figures 1–6, Figure S1 / 图1–6、图S1);
- Discussion-level integration of high-impact SCI literature explaining how pathogenic peptides cause AD via oral–brain axis translocation, BBB penetration, PAS active gorge obstruction (inducing cholinergic failure), and AChE-mediated pathological chaperone amyloid co-nucleation.

**v3.0.0–v3.14.0 do not support / 不支持：**

- row-level linkage between the twelve strings and the principal screening funnel or stricter eight;
- in vitro measured binding affinity (Kd), inhibition constant (Ki), or biophysical aggregation kinetics without wet-lab validation;
- measured in vivo BBB transport, tissue expression, or proven AD causality prior to prospective animal/cellular assays.

**v3.1.0–v3.3.0 relationship / 精简稿关系：** v3.1.0 and v3.2.0 are frozen prior concise packages. v3.3.0 superseded them after SCI-structure revision and is now itself frozen after v3.6.0; none of these versions strengthens the underlying evidence. / v3.1.0和v3.2.0为冻结的既往精简稿；v3.3.0曾在SCI结构修订后取代它们，现也已被v3.6.0冻结；这些版本均不提高底层证据强度。

**v3.5.0 full-package relationship / 完整稿关系：** v3.5.0 superseded v3.4.0 as the prior full release. Its historical deliverables remain frozen. / v3.5.0曾取代v3.4.0成为上一版完整稿，其历史交付物保持冻结。

**v3.15.0 package relationship / 当前版本关系：** v3.15.0 preserves the six full, intermediate, and concise screening DOCX files byte-for-byte. Screening manuscripts continue to carry the frozen external v0.4 transcribed docking summaries. The standalone docking/MD package now ships full, intermediate, and concise English/Chinese reports, all illustrated with the same seven figures. No docking or MD result is imported into the screening manuscripts. / v3.15.0逐字节保留六份筛选完整稿、中间稿和简洁稿DOCX；筛选稿继续使用冻结的外部v0.4转录对接汇总；独立对接与MD包现含完整/中间/简洁中英文报告，三版均嵌入同一套7幅图；任何对接与MD结果均未导入筛选稿。

**v3.2.0 provenance correction / v3.2.0来源修正：** PRJNA678453 is reported as a 22-participant cohort (11 orally healthy and 11 with periodontitis) producing 66 oral specimens; PRJEB65451 is reported as the derived EBI-EMG/MGnify TPA assembly project. / PRJNA678453按22名参与者（11名口腔健康、11名牙周炎）和66份口腔标本报告；PRJEB65451按衍生TPA组装项目报告。

**v3.3.0 scientific-writing correction / v3.3.0科学写作修正：** Introduction references [1]–[10] are cited one paper per bracket. Methods emphasize the relevant deep-learning peptide modes and retain the absence of row-level model, lineage and docking inputs as a reproducibility limitation. / 引言文献[1]–[10]采用每个括号一篇文献；方法突出与肽分析相关的深度学习模式，并继续把逐行模型输出、来源链和对接输入缺失列为可重复性局限。

**v3.4.0 historical carry-forward / v3.4.0历史修正：** The frozen v3.4.0 English and Chinese manuscripts report the then-adopted public-cohort counts and distinguish UniDL4BioPep, NTxPred2 peptide mode, mebipred, and AnOxPePred by their documented architectures. Introduction citation brackets contain one reference each. / 冻结的v3.4.0中英文稿保留当时采用的公共队列数量，按文献架构区分四类预测工具，且引言每个引文括号仅含一篇文献。

**v3.5.0 historical reporting and MD boundary / v3.5.0历史数量与MD边界：** The v3.5.0 article bodies omitted participant, specimen, assembly-analysis and MAG totals. The user-derived 296-MAG value remained in the evidence ledger pending a recountable manifest. That release described only a prospective GROMACS protocol and did not report an MD result. v3.10.0 does not alter this frozen history; it adds a separate, explicitly limited ALLLHRC result package. / v3.5.0正文省略参与者、标本、组装分析和MAG总数；用户原始映射所得296个MAG在证据台账中暂存，等待可重计清单；该冻结版本只描述前瞻性GROMACS方案而未报告MD结果。v3.10.0不修改其历史内容，仅新增一个边界明确的独立ALLLHRC结果包。

## 4. Create and push the current tag / 创建并推送本次标签

The repository includes a guarded cross-platform helper: / 仓库提供带保护检查的跨平台脚本：

```bash
python3 scripts/manage_version_tag.py create \
  --version 3.13.0 \
  --message "v3.13.0: expand standalone package to full docking and multi-system MD reports" \
  --push
```

Equivalent native Git commands / 等价Git命令：

```bash
git status --short
git tag -a porphyromonas-ad-manuscript-v3.13.0 \
  -m "v3.13.0: expand standalone package to full docking and multi-system MD reports"
git push origin refs/tags/porphyromonas-ad-manuscript-v3.13.0
```

The helper refuses to tag a dirty working tree, the wrong branch, or an existing tag. / 脚本会拒绝脏工作区、错误分支或重复标签。

## 5. Verify a tag / 核验标签

```bash
python3 scripts/manage_version_tag.py verify --version 3.13.0
git show --no-patch --decorate porphyromonas-ad-manuscript-v3.13.0
git rev-list -n 1 porphyromonas-ad-manuscript-v3.13.0

# Earlier immutable baselines remain independently verifiable:
python3 scripts/manage_version_tag.py verify --version 3.12.0
python3 scripts/manage_version_tag.py verify --version 3.11.0
python3 scripts/manage_version_tag.py verify --version 3.10.0
python3 scripts/manage_version_tag.py verify --version 3.9.0
python3 scripts/manage_version_tag.py verify --version 3.8.0
python3 scripts/manage_version_tag.py verify --version 3.7.0
python3 scripts/manage_version_tag.py verify --version 3.6.0
python3 scripts/manage_version_tag.py verify --version 3.5.0
python3 scripts/manage_version_tag.py verify --version 3.2.0
python3 scripts/manage_version_tag.py verify --version 3.1.0
python3 scripts/manage_version_tag.py verify --version 3.0.0
```

## 6. Safe recovery / 安全恢复

### 6.1 Inspect the tagged release without changing the active checkout

Recommended: create a separate worktree. / 推荐创建独立worktree，不改变当前工作目录：

```powershell
Set-Location 'E:\0writing\Light-skills'
git fetch origin --tags
git worktree add 'E:\0writing\Light-skills-restore-v3.13.0' porphyromonas-ad-manuscript-v3.13.0

# To inspect an earlier immutable baseline instead:
git worktree add 'E:\0writing\Light-skills-restore-v3.12.0' porphyromonas-ad-manuscript-v3.12.0
git worktree add 'E:\0writing\Light-skills-restore-v3.11.0' porphyromonas-ad-manuscript-v3.11.0
git worktree add 'E:\0writing\Light-skills-restore-v3.4.0' porphyromonas-ad-manuscript-v3.4.0
git worktree add 'E:\0writing\Light-skills-restore-v3.3.0' porphyromonas-ad-manuscript-v3.3.0
git worktree add 'E:\0writing\Light-skills-restore-v3.2.0' porphyromonas-ad-manuscript-v3.2.0
git worktree add 'E:\0writing\Light-skills-restore-v3.1.0' porphyromonas-ad-manuscript-v3.1.0
git worktree add 'E:\0writing\Light-skills-restore-v3.0.0' porphyromonas-ad-manuscript-v3.0.0
```

Remove it after inspection / 检查后移除：

```powershell
git worktree remove 'E:\0writing\Light-skills-restore-v3.12.0'
# Or remove an earlier baseline worktree if one was created:
git worktree remove 'E:\0writing\Light-skills-restore-v3.11.0'
git worktree remove 'E:\0writing\Light-skills-restore-v3.4.0'
git worktree remove 'E:\0writing\Light-skills-restore-v3.3.0'
git worktree remove 'E:\0writing\Light-skills-restore-v3.2.0'
git worktree remove 'E:\0writing\Light-skills-restore-v3.1.0'
git worktree remove 'E:\0writing\Light-skills-restore-v3.0.0'
```

### 6.2 Restore one file from the tag

```bash
git restore --source=porphyromonas-ad-manuscript-v3.13.0 -- \
  projects/porphyromonas-ad-mechanism-manuscript/manuscript/md_alllhrc/full/English.docx
```

Review the diff before committing the restored file. / 提交恢复文件前先检查差异。

### 6.3 Compare the current branch with v3.0.0

```bash
git fetch origin --tags
git diff --stat porphyromonas-ad-manuscript-v3.0.0..arena/019ff377-light-skills
git diff porphyromonas-ad-manuscript-v3.0.0..arena/019ff377-light-skills -- \
  projects/porphyromonas-ad-mechanism-manuscript/
```

### 6.4 Recover an older untagged historical version

Use a separate worktree with the exact checkpoint, for example v2.0.0: / 使用精确提交在独立worktree中恢复，例如v2.0.0：

```powershell
git worktree add 'E:\0writing\Light-skills-restore-v2.0.0' a31d29466dc8d376d6012abd916152eb82e017f1
```

Do not use `git reset --hard` for routine recovery; it can discard uncommitted work. / 常规恢复不要使用`git reset --hard`，以免丢失未提交内容。

## 7. Template for the next version / 下一版本记录模板

Copy one row into the ledger and complete: / 在台账中复制一行并补齐：

```text
Version:
Date:
Scientific change:
Evidence added or removed:
Files changed:
Audits and verdicts:
Known limitations:
Content commit:
Release tag:
Push verification:
```
  projects/porphyromonas-ad-mechanism-manuscript/
```

### 6.4 Recover an older untagged historical version

Use a separate worktree with the exact checkpoint, for example v2.0.0: / 使用精确提交在独立worktree中恢复，例如v2.0.0：

```powershell
git worktree add 'E:\0writing\Light-skills-restore-v2.0.0' a31d29466dc8d376d6012abd916152eb82e017f1
```

Do not use `git reset --hard` for routine recovery; it can discard uncommitted work. / 常规恢复不要使用`git reset --hard`，以免丢失未提交内容。

## 7. Template for the next version / 下一版本记录模板

Copy one row into the ledger and complete: / 在台账中复制一行并补齐：

```text
Version:
Date:
Scientific change:
Evidence added or removed:
Files changed:
Audits and verdicts:
Known limitations:
Content commit:
Release tag:
Push verification:
```
