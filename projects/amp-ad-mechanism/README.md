# 抗菌肽 × 阿尔茨海默病：机制落点与计算方案

| 文件 | 说明 |
|---|---|
| `outputs/抗菌肽-阿尔茨海默病-机制关联框架.docx` | 正文文档：八个机制落点、肠道来源的暴露路径、计算方案与判据、下一步安排、参考文献 |
| `outputs/抗菌肽-阿尔茨海默病-八个机制.pptx` | 14 页组会用 PPT，原生可编辑形状与文本框（ppt-master 导出） |
| `ppt/svg_output/P01–P14.svg` | PPT 的页面源文件，改这里再重新导出即可 |
| `figures/fig1_mechanism_map.png` | 文中图 1，按肠腔 / 循环与屏障 / 脑实质三隔室排列的机制落点 |
| `scripts/build_docx.py` | 文档生成脚本（python-docx，宋体 + Times New Roman，A4） |
| `scripts/make_slides.py` | PPT 页面 SVG 生成脚本（1600×900，zh-CN） |
| `scripts/make_figures.py` | 示意图生成脚本（matplotlib） |
| `scripts/skill_finder.py` | 本地技能检索脚本（按关键词检索已安装的 SKILL.md），含 `--selftest` |

复现：

```bash
export PYTHONUTF8=1
python3 scripts/make_figures.py
python3 scripts/build_docx.py

python3 scripts/make_slides.py
SKILL=../../.claude/skills/ppt-master
python3 $SKILL/scripts/svg_quality_checker.py ppt --quick-generate --canonical-authoring --stage final --json
python3 $SKILL/scripts/svg_to_pptx.py ppt --quick-generate --primary-language zh-CN \
  -o outputs/抗菌肽-阿尔茨海默病-八个机制.pptx
```

依赖：`python-docx`、`matplotlib`、`python-pptx`、`XlsxWriter`。
技能：`.claude/skills/ppt-master`（SVG → 原生 PPTX）、`.claude/skills/humanizer`（行文去 AI 腔）、`.claude/skills/find-skills`。

待补：AChE–Aβ 1 μs 分子动力学那篇（原稿编号 [31]）的著录信息，补到参考文献第 2 条之后并顺延编号；
其余条目在检索环境下未能逐字核对卷期页码的，投稿前用 DOI / PMID 复核一次。
