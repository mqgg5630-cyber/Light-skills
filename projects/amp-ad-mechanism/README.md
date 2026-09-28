# 抗菌肽 × 阿尔茨海默病：机制关联研究框架（对接 / 动力学 / 多尺度模拟）

本目录是一次真实任务的交付留存：为“肠道宏基因组来源抗菌肽（AMP）与 AD 的机制关联”补齐机制版图，
并产出一份期刊投稿格式的中文 DOCX 稿件。

## 交付物

| 文件 | 说明 |
|---|---|
| `outputs/抗菌肽-阿尔茨海默病-机制关联框架.docx` | 主交付：期刊格式稿件（题名/中英文摘要/关键词/正文 8 节/5 张表/2 张图/50 条参考文献/2 个附录） |
| `figures/fig1_mechanism_map.png` | 图 1：三隔室机制版图（M1–M8），程序化生成 |
| `figures/fig2_workflow.png` | 图 2：Stage 0–4 工作流与 G1–G5 通过门，程序化生成 |
| `outputs/skill-search-raw.txt` | find-skills 流程的本地检索原始输出 |
| `scripts/build_docx.py` | 稿件生成脚本（python-docx，宋体/黑体 + Times New Roman，A4，页码） |
| `scripts/make_figures.py` | 示意图生成脚本（matplotlib；沙箱无中文字体，图内用英文标注，中文在图题） |
| `scripts/skill_finder.py` | find-skills 的离线回退实现（对本地 SKILL.md 清单做关键词检索），含 `--selftest` |

## 复现

```powershell
$env:PYTHONUTF8="1"
python scripts\make_figures.py
python scripts\build_docx.py
python scripts\skill_finder.py --selftest
```

依赖：`python-docx`、`matplotlib`。

## 内容要点

- **不走“抑制剂”叙事**：全文以“抗菌肽作为可改变 AD 关键分子过程方向的因子”为主线，第 2.1 节给出从抑制剂视角
  改写为致病机制视角的三条规则。
- **机制从 2 条扩到 8 个模块**：M1 AChE–PAS 三元复合物（承接原机制一）、M2 Aβ 交叉成核的方向判据（承接原机制二）、
  M3 tau PHF6（可选）、M4 先天免疫受体（FPR2 / CLIC1 / TLR4–MD-2–CD14 / RAGE）、M5 神经元膜界面与钙通透、
  M6 Aβ 清除通路底物竞争（IDE/NEP/TTR）、M7 AMP 自身淀粉样化与种子输出、M8 肠道端（CsgA/FapC + 菌群群落 FBA）。
- **每个模块都带量化判据与阴性对照**，统一到 G1 暴露门、G2 位姿门、G3 稳定门、G4 方向门、G5 证伪门。
- **肠道来源的暴露问题**：给出 R1 跨 BBB / R2 肠道局部+神经免疫 / R3 外周作用 三条路径的判别矩阵，
  建议以 R2+R3 为主假设、R1 为需满足四项必要条件的次要分支。

## find-skills 说明（诚实记录）

- `find-skills` 已安装到 `.claude/skills/find-skills`（来源 vercel-labs/skills，仓库 `.gitignore` 忽略该目录）。
- 其依赖的 skills.sh 注册表与 `npx skills find` 在本环境不可达（`curl https://skills.sh/` 返回 000，
  `npx skills find <query>` 一律返回 "No skills found"），因此按 find-skills 的六步流程降级为**本地技能检索**：
  索引 Light Skills（23 个）与 K-Dense `scientific-agent-skills` 中安装的技能，按任务关键词打分排序。
- 命中并实际用于本文的技能见稿件附录 A。

## 待核查

- 参考文献中标 ▲ 的条目未能在本环境逐字核对卷期页码，投稿前请用 DOI/PMID 复核。
- 参考文献 [6] 为用户原稿中的文献 [31]（AChE–Aβ 1 μs MD），需作者补全著录信息。
