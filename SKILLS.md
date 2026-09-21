# Light Skills 技能总目录（SKILLS.md）

> 本文件是**本仓库全部技能的总目录**。第 2 节的索引表由
> `skills/gen_skills_index.sh` 自动生成（`agent-sync.sh` 每次推送前刷新），
> 手写内容在标记区之外，机器只改 `AUTO-INDEX` 标记之间。
> 面向用户的入口仍是 `README.md`；`skills/README.md` 是 light-* 技能的开发说明。

## 1. 两类技能，一份目录

| 类别 | 目录 | 说明 |
|---|---|---|
| **Light 自研技能**（23 个） | `skills/light-*` | 科研/竞赛/创新全流程：选题、文献、实验、图表、论文、排版、专利软著 |
| **外部桥技能**（2 个） | `skills/git-sync`、`skills/arena-local-bridge` | 沙箱 agent ↔ 本机 Windows 的打通与编排，来源见 `skills/.external-skills` |

外部桥技能**不是** Light 自研，整份来自
<https://github.com/shaohuawen03-cyber/BrowserSkill> 分支 `arena/01a0b237-browserskill`
（commit `db7ae89`，git-sync v2.9.2 / arena-local-bridge v2.0）。它们的上游
`SKILL.md` 原样保留（`name` 可以与目录名不同、甚至没有 frontmatter），因此
`scripts/bootstrap_agent_skills.py` 按 `skills/.external-skills` 清单把它们当
**external** 镜像，不再按 light-* 命名规则判 invalid。

## 2. 技能索引（自动生成，勿手改）

<!-- BEGIN:AUTO-INDEX -->
| 技能 | 版本 | 说明 |
|---|---|---|
| **arena-local-bridge** | 2.0 | arena-local-bridge — 最终版 skill（BrowserSkill 全家桶汇总） — 版本 v2.0（2026-09-18）。汇总：`git-sync`（git 打通+值守+自循环）、 |
| **git-sync** | 2.9.2 | git-local-arena-sync — TRIGGER: user says 安装https://arena.ai/agent/01a0a821 的skills 与本地打通 (or 安装 arena/01a0a821-git-pull-arena skills). Do NOT open arena.ai (login wall). Immediately:… |
| **light-citation** | - | light-citation — Verify scholarly references and claim-citation support for Light stage 10. Use when auditing a manuscript, claim map, bibliography, DOI/arXiv/PMID/ISBN/URL, Bib… |
| **light-consistency** | - | light-consistency — Light 跨材料一致性常驻机读门:在所有产出材料后台核查术语 / 指标(名+值)/ 创新点表述 / 方法名 在论文·PPT·软著·代码·项目文档之间是否统一,定义一改回扫所有已产出材料,把"各处说法对齐"从口头 建议落成**可机检、可阻断、可被总控 run_checkpoint 聚合的机读门**(产 light.fi… |
| **light-data-engineering** | - | light-data-engineering — Light 科研主线第 2 步·数据工程：**找得到且用得起的数据**（来源/许可/版本/大小/split）+ **提 idea 前先判数据可行性** （数据够不够支撑研究/统计功效）+ **防数据泄漏**（顶会拒稿高频雷）。何时用：用户要找/选/下载公开数据集，或给了数据问 "能不能做研究/够不够/质量行不行" / … |
| **light-experiment-coding** | - | light-experiment-coding — Light 科研主线 stage 6：把冻结的 question/estimand、experiment matrix、pre-registration 与 data lineage 落成最小可运行、测试先行、无泄漏、可复现且能交给 result-analysis 的实验代码。用于实现或复现训练/预处理/评测， 设计 … |
| **light-figure** | - | light-figure — Light 科研主线第 9 步·图表：图服务论点（每图支撑哪条 claim、删了缺什么）+ 出版级规格（栏宽/字号/色盲安全/ 误差棒+n+显著性）+ 视觉诚实（不偷偷截 y 轴/不双 y 轴伪相关/不 jet-rainbow）+ 渲染后多模态「真看一眼」+ 论文数据图程序化生成绝不 AI 生图。何时用：结果分析做完要… |
| **light-file-reading** | - | light-file-reading — Light 多格式文件深度理解常驻技能：强大地读 Word / PDF / PPTX / Excel / CSV / 图片 / 视频 / 代码 / 压缩包，**不只提取文字，而是理解结构 / 图表 / 数据 / 格式要求 / 隐含意图**，产结构化"理解笔记"五面 （结构逻辑·关键内容·格式约束·视觉风格·可复用）并映… |
| **light-frontend-design** | - | light-frontend-design — Light 按需工程技能·前端设计：把模糊的「做个好看的界面」落成**能跑的 React/Tailwind/shadcn 代码 + 设计决策说明**—— 有**视觉记忆点**(signature element)、**风格自洽**(design tokens 一致)、**适配场景**(学术海报/数据大屏/管理后台/移动… |
| **light-idea-critique** | - | light-idea-critique — Light 科研主线第 4 步·审 idea：以**顶会审稿人标准严审** idea，**撞车/无创新 fatal flaw 一票否决**(critical 门)， 逼出真能发表的 idea。何时用：用户问"这 idea 行不行/够不够新/能不能发""帮我严审/挑刺/找致命问题" / idea 定稿前把关 / 收到 i… |
| **light-idea-generation** | - | light-idea-generation — Light 科研主线第 3 步·提 idea:从模糊方向/数据/文献**结构化发散**(激发算子系统生成,不是泛泛头脑风暴) → 产**值得做且做得成的分层候选 idea**(moonshot 冲刺/solid 稳妥/safe 保底),每个必答**为什么值得做·创新点· 比现有强在哪·解决什么具体问题·能投什么层次**… |
| **light-literature-search** | - | light-literature-search — Light 科研主线第 1 步·文献调研:在线多源检索(OpenAlex/arXiv/Crossref/Europe PMC/DOAJ,全程免 key)→ 产出**不是论文列表,是可直接喂 idea 的"领域地图"**:近三年前沿 + 经典奠基 + 跨领域方法移植**三层分别 检索分别排序**,合成研究脉络 + 方法谱… |
| **light-memory-pm** | - | light-memory-pm — Light 项目运行时记忆与项目管理常驻技能:把"项目做到哪/定了啥/出到哪版/术语怎么统一/上次断哪" 落到每个项目自己的 .light/ 目录(项目卡 + 决策日志 + 版本史 + 受控术语表 + 跨会话交接卡), 复用 passport.py 引擎管 DAG 台账(不重造)。它是 consistency 事实源的… |
| **light-orchestrator** | - | light-orchestrator — Coordinate and recover multi-stage Light research projects through the canonical .light/passport.yaml state, stages 1-13, resident overlays, checkpoints, findin… |
| **light-paper-writing** | - | light-paper-writing — Light 科研主线第 8 步·论文写作：围绕「如何让审稿人相信值得发表」组织，初稿→审稿人视角循环打磨； 每个 claim 都有证据、措辞强度匹配证据强度、绝不过度宣称。何时用：实验+分析做完要写论文 / 写/改摘要·引言· 贡献句·结论 / 担心「claim 无证据 或 措辞夸大」/ 要让贡献三处(摘要·引言·结论… |
| **light-patent-disclosure** | - | light-patent-disclosure — Prepare evidence-backed patent invention disclosure materials for attorney or patent-agent review. Use when the user asks for 专利点挖掘, 技术交底书, 现有技术/查新记录, claim/pat… |
| **light-project-structure** | - | light-project-structure — Audit, plan, scaffold, and safely migrate research project structures across greenfield, existing Git/non-Git repositories, and monorepo subroots. Use for proje… |
| **light-research-ethics** | - | light-research-ethics — Light 科研诚信与伦理全生命周期常驻红线门:在研究分诊、审批、采集、变更、分析、投稿、发布与出版后检查 学术不端/数据造假/统计自洽/结论夸大/幻觉与撤稿 引用/自我抄袭/隐私/版权/署名与 AI 披露/软著专利权属/论文工厂洗稿等风险,把"别造假别夸大"从口头建议 落成**可机检、可阻断、可被总控 run_che… |
| **light-research-plan** | - | light-research-plan — Light 科研主线第 5 步·研究方案与实验设计：把 idea-critique 放行的 idea 与 data feasibility 拆成**能真执行、能写进论文、 能复现**的 question/estimand、实验矩阵与预注册包。何时用：idea 已通过审查要落地 / 要设计实验·消融·对比·敏感性· 泛化… |
| **light-result-analysis** | - | light-result-analysis — Light 科研主线第 7 步·结果分析：不描述好坏、解释「为什么」，把每条结论**绑死到 claim + 证据强度**，并防 p-hacking。 何时用：实验跑完要解读结果 / 问「这些数说明什么」/ 要做显著性检验 + 效应量 + 置信区间 + 多重比较校正 / 担心 p-hacking (多重比较不校正、选择性… |
| **light-review-rebuttal** | - | light-review-rebuttal — Build auditable peer-review revision and author-response packages for Light stage 13. Use after receiving reviewer comments, a decision or meta-review; when dra… |
| **light-software-copyright** | - | light-software-copyright — Prepare China software copyright registration material drafts from a real software project: application-field worksheet, source-code deposit material, user/oper… |
| **light-system-design** | - | light-system-design — Design or modernize a software system from an evidence-backed current-state inventory through quality attributes, architecture options, API and schema contracts… |
| **light-typesetting** | - | light-typesetting — Build and preflight submission-ready LaTeX/PDF artifacts for Light stage 11. Use when receiving a paper-writing manuscript, figure delivery, citation delivery.j… |
| **light-venue-matching** | - | light-venue-matching — Build evidence-bound journal or conference shortlists for Light stage 12. Use after typesetting delivers venue-handoff.json/PDF/compliance facts; when an author… |
<!-- END:AUTO-INDEX -->

## 3. 安装（含本机打通）

```powershell
git clone -b <工作分支> https://github.com/mqgg5630-cyber/Light-skills.git
cd Light-skills
$env:PYTHONUTF8="1"
python scripts\bootstrap_agent_skills.py --mode auto --force   # 25 个技能 -> .agents/.claude/.opencode
python scripts\bootstrap_agent_skills.py --check-only          # 期望 exit 0
```

Windows 本机打通（git-sync 值守 + 产物回传）见
[`docs/local-bridge/README.md`](docs/local-bridge/README.md)：一次粘贴即可在
`E:\0zhongqi\<新目录>` 建克隆、注册值守，**不覆盖任何已有目录**。

## 4. 自检闸门

| 命令 | 作用 |
|---|---|
| `python scripts\bootstrap_agent_skills.py --selftest` | 技能镜像器自测（含 external 分支） |
| `bash code/check_all.sh` | 桥技能闸门：`.ps1` 全 ASCII、配置分支==HEAD、根目录脚本与 `skills/git-sync/scripts` 逐字节一致、`$var:` 陷阱扫描、值守收尾行覆盖 |
| `.\doctor.ps1`（本机） | 分支/落后领先/未提交/技能版本/值守/心跳/凭据 体检，`-Fix` 一键修复 |
