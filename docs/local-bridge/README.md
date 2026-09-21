# 本机打通（Windows ↔ Arena 沙箱）

把沙箱里的 agent 和你自己的 Windows 机器接起来：agent 推分支 → 本机值守自动拉取、
跑检查、把判定和产物推回 → agent 读到判定再决定收尾还是修一轮。中间**只有 git**，
每一步都有提交可审计。

这份能力来自外部技能包 **git-sync**（不是 Light 自研），本文只讲「在本仓库怎么装、
怎么用、怎么停」。技能内部细节见 `skills/git-sync/SKILL.md`（上游文档，原样保留）。

---

## 1. 来源与版本（可核对）

| 项 | 值 |
|---|---|
| 上游仓库 | <https://github.com/shaohuawen03-cyber/BrowserSkill> |
| 上游分支 | `arena/01a0b237-browserskill` |
| 上游 commit | `db7ae89c0e9b471c34fdade12280328b8c5d0556`（2026-09-18） |
| `skills/git-sync` | **v2.9.2**（沙箱 ↔ 本机双向桥，本次打通用的就是它） |
| `skills/arena-local-bridge` | **v2.0**（arena 会话编排 + 实测铁律；选装，依赖本机 `bsk` CLI） |
| 本仓库工作分支 | `arena/01a0c342-light-skills`（`skills/git-sync/sync.config.json` 的 `branch`） |

两个技能都登记在 `skills/.external-skills`：`scripts/bootstrap_agent_skills.py`
按 **external** 处理，原样镜像到 `.agents/.claude/.opencode`，不按 light-* 的
命名规则判 invalid（上游 `git-sync` 的 frontmatter `name` 是 `git-local-arena-sync`，
`arena-local-bridge` 干脆没有 frontmatter）。

## 2. 装了什么（文件清单）

```
skills/git-sync/            上游技能整份（SKILL.md / VERSION / scripts/ / templates/ / sync.config.json）
skills/arena-local-bridge/  上游技能整份
skills/gen_skills_index.sh  索引生成器（刷新根目录 SKILLS.md 的 AUTO-INDEX 表）
skills/.external-skills     外部技能清单（bootstrap 的豁免依据）
SKILLS.md                   本仓库技能总目录（索引自动生成）

sync.ps1 push.ps1 upload.ps1 download.ps1 pack.ps1 doctor.ps1
bootstrap.ps1 pr.ps1 hardware.ps1 watch.ps1 auth.ps1 install.ps1
where.ps1 where.cmd         仓库根目录的本机侧脚本，是 skills/git-sync/scripts/ 的逐字节镜像
                            （code/check_all.sh 第 3 节会卡这件事）

code/check_all.sh           提交前闸门（.ps1 全 ASCII / 配置分支==HEAD / 根目录镜像一致 / $var: 陷阱）
code/local_check.ps1        本机值守每轮实际执行的检查（闸门 + 你自己加的仓库专属检查）
code/scan_ps_var_colon.py   闸门辅助：扫 "$var:" 盘符变量陷阱
code/check_loop_summary.ps1 / .py   值守收尾行覆盖检查

results/sync/               同步回执（last_sync.md + history/）
results/status/             握手与判定（handshake.json / check_rN_*.txt / success_criteria.json）
results/hardware/           本机硬件与环境报告（hardware.ps1 写入）
```

`sync.config.json` 关键项：`branch=arena/01a0c342-light-skills`、`remote=origin`、
`gate=bash code/check_all.sh`、`check_cmd=powershell ... code/local_check.ps1`、
`hands_free/auto_pull/auto_push=true`、`download_sets={final:[deliverable], all:[deliverable,code,skills]}`。

## 3. 本机打通：一段粘贴（Windows PowerShell）

目录按你的要求放 `E:\0zhongqi`，**并且不覆盖任何已有目录**：同名目录已存在时
自动改用 `-2` / `-3` 后缀（`git clone` 本身也拒绝写进非空目录，这里只是让它不报错）。

```powershell
New-Item -ItemType Directory -Force E:\0zhongqi | Out-Null
cd E:\0zhongqi
$base = 'Light-skills-01a0c342'; $dir = $base; $i = 1
while (Test-Path -LiteralPath $dir) { $i++; $dir = "$base-$i" }
git clone -b arena/01a0c342-light-skills https://github.com/mqgg5630-cyber/Light-skills.git $dir
cd $dir
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\bootstrap.ps1 -Auto                        # 身份 + 切分支 + 免点击推送 + 注册值守
.\auth.ps1 -Account mqgg5630-cyber           # 账号策略：谁仓库的会话就用谁账号（只钉本克隆）
.\auth.ps1 -Verify                           # 证明静默推送可用（ls-remote + push --dry-run）
.\doctor.ps1                                 # 体检
.\watch.ps1 -Status                          # 值守活着吗
```

对应关系（由 `bash skills/git-sync/scripts/agent-handoff.sh` 生成，别手打）：

| 项 | 值 |
|---|---|
| repo | `Light-skills`（`https://github.com/mqgg5630-cyber/Light-skills.git`） |
| branch | `arena/01a0c342-light-skills` |
| folder | `Light-skills-01a0c342`（新目录，不覆盖已有克隆） |
| watcher | 计划任务 `git-sync-watch-Light-skills-01a0c342` |
| account | `mqgg5630-cyber`（仓库主；机器默认账号不受影响） |

前置只有一个：本机装好 Git（`git --version` 出版本号；没有就到
<https://git-scm.com/download/win>）。`auth.ps1 -Account` 需要本机有 `gh`
并且该账号已登录（`gh auth status`）；没有 `gh` 时跳过这两行，用机器默认凭据也能推。

### 验收：`.\doctor.ps1` 应该看到

- `branch` = `arena/01a0c342-light-skills`，`ahead/behind = 0/0`
- 末尾三行 `watcher` / `heartbeat` / `auth` 都正常，`hands-free: master=True`
- `auth account` 行显示本克隆钉到 `mqgg5630-cyber`

`.\watch.ps1 -Status` 应该看到 `loop process: pid ... (running)`（只有一个）、
`heartbeat age ... fresh`、`other loops` 不出现。计划任务结果码
`0 / 267009 / 267011 / 267014 / 2147946720(0x800710E0)` 都是正常值。

## 4. 日常用法

```powershell
.\sync.ps1                       # 拉最新（agent 每轮推完就看得到）
.\where.cmd -Want 01a0c342       # 我这台机器上该用哪个文件夹（[USE] 标记）
.\download.ps1 -Set final        # 交付物落地（打印来源仓库/分支/提交/目标目录）
.\download.ps1 -Set all          # deliverable + code + skills
.\upload.ps1 -Src "E:\附件"       # 附件按扩展名归位 sources/ code/ results/ 并推回
.\push.ps1 -Gate "本机改动说明"    # 手动推（拒绝 main/master；默认静默、不弹窗）
.\hardware.ps1 -Deep             # 上报本机硬件/conda 环境（每台机器一次）
.\doctor.ps1 -Fix                # 任何不对劲先跑这个
```

`download_dir` 留空 → 产物落在克隆**上一级**的 `Light-skills-01a0c342_out`
（即 `E:\0zhongqi\Light-skills-01a0c342_out`），不会写进你别的目录。

### 自循环（agent 干活 → 本机自动验收 → 结果回传）

本机值守注册好之后，沙箱侧一条命令闭环：

```bash
bash skills/git-sync/scripts/agent-handsfree.sh \
  --sync "feat: <本轮改动>" --request "verify: <验收什么>" --timeout auto
```

`exit 0` = 本机判定通过且已收尾；`exit 2` = 看 `results/status/check_rN_*.txt` 修一轮；
`exit 3` = 本机值守没起来（重跑第 3 节那段粘贴）。

## 5. 与 light-* 技能共存

```powershell
$env:PYTHONUTF8 = "1"
python scripts\bootstrap_agent_skills.py --mode auto --force   # 25 个技能 -> 项目级发现路径
python scripts\bootstrap_agent_skills.py --check-only          # 期望 exit 0，external=2 invalid=0
```

想装到**全局**（所有项目可用）又**不覆盖已有目录**：

```powershell
foreach ($t in @("$HOME\.claude\skills", "$HOME\.agents\skills")) {
  New-Item -ItemType Directory -Force $t | Out-Null
  Get-ChildItem .\skills -Directory | ForEach-Object {
    $d = Join-Path $t $_.Name
    if (-not (Test-Path -LiteralPath $d)) { Copy-Item -Recurse $_.FullName $d }
    else { Write-Host "skip (exists): $d" }
  }
}
```

## 6. 停用与卸载

```powershell
.\watch.ps1 -Unregister      # 摘掉本会话值守（计划任务删除，克隆保留）
.\watch.ps1 -RestoreParked   # 把被 -Register/-Focus 暂停的其他会话值守全部拉回来
```

- **零后台政策**：只有你点名要用某个会话时才 `-Register`，任务结束就 `-Unregister`；
  注册新值守会**暂停**（不删除）机器上其他 `git-sync-watch-*` 任务。
- 卸载技能本身：删掉根目录 14 个 `.ps1/.cmd`、`code/`、`skills/git-sync/`、
  `skills/arena-local-bridge/`、`skills/gen_skills_index.sh`、`skills/.external-skills`、
  `results/`，并从 `skills/.external-skills` 相关的文档段落里移除引用即可；
  light-* 技能与 `scripts/bootstrap_agent_skills.py` 不依赖它们。

## 7. 重装 / 升级（换分支或换仓库时）

```bash
# 沙箱侧：把上游技能装进任意仓库的工作分支（只建不覆盖本地检查脚本与已有配置）
git clone --quiet --depth 1 -b arena/01a0b237-browserskill \
  https://github.com/shaohuawen03-cyber/BrowserSkill.git /tmp/bs \
  && bash /tmp/bs/skills/git-sync/scripts/agent-install.sh \
       --repo <目标仓库> --branch <工作分支> --source /tmp/bs
```

```powershell
# 本机侧：已装过的克隆升级三步
.\sync.ps1
.\watch.ps1 -Unregister ; .\watch.ps1 -Register
.\watch.ps1 -Status
```

安装器**拒绝降级**（比对 `skills/git-sync/VERSION`），已有 `sync.config.json`
只更新 `branch/remote` 与补缺失键，`code/local_check.ps1` 只建不覆盖。

## 8. 已知边界（别踩）

- `.ps1` **只能 ASCII**：Windows PowerShell 5.1 按 GBK 解码无 BOM 的 `.ps1`，
  中文注释会吃掉引号。中文写进 `.md` / `.json`。闸门每次提交前扫全部 `.ps1`。
- 只在工作分支上动：`push.ps1` / `pr.ps1` 直接拒绝 `main` / `master`。
- 同一分支不要 Windows + WSL 双值守（会抢答/重复判定），只留一侧 live。
- 大文件不进 git（`pack.ps1` 外发，或放被 ignore 的目录）。
- `arena-local-bridge` 需要本机装 `bsk` CLI + 浏览器扩展才能真正驱动浏览器；
  本次打通**没有**装它（只用 git-sync 那条链路）。要装见上游
  `AGENT_INSTALL.md`：`irm https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.ps1 | iex`。
