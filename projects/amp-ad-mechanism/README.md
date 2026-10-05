# 抗菌肽 × 阿尔茨海默病：机制落点与计算方案

| 文件 | 说明 |
|---|---|
| `outputs/抗菌肽-阿尔茨海默病-机制关联框架.docx` | 正文文档：两条原有机制的问题、其他疾病的五类做法、可补的八个机制落点、肠道来源的暴露路径、计算方案与判据、下一步安排、参考文献 |
| `figures/fig1_mechanism_map.png` | 文中图 1，按肠腔 / 循环与屏障 / 脑实质三隔室排列的机制落点 |
| `scripts/build_docx.py` | 文档生成脚本（python-docx，宋体 + Times New Roman，A4） |
| `scripts/make_figures.py` | 示意图生成脚本（matplotlib） |
| `scripts/skill_finder.py` | 本地技能检索脚本（按关键词检索已安装的 SKILL.md），含 `--selftest` |

复现：

```powershell
$env:PYTHONUTF8="1"
python scripts\make_figures.py
python scripts\build_docx.py
```

依赖 `python-docx` 与 `matplotlib`。

参考文献 [3] 对应原稿编号 [31] 的 AChE–Aβ 1 μs 分子动力学文献，著录信息需补；
其余条目在检索环境下未能逐字核对卷期页码的，投稿前用 DOI / PMID 复核一次。
