# 项目接手.Skill（Project Handoff Skill · `project-relay`）

（[中文](https://github.com/hoshinohatsuka/project-relay-Skill/edit/main/README.md) | [English](https://github.com/hoshinohatsuka/project-relay-Skill/blob/main/readme-EN) ）

为 Agent 提供跨会话项目分析、接手、冻结交接和续跑的操作协议。它引导 Agent 将状态与可核验证据写进仓库，而不是留在聊天框里；实际执行质量仍取决于所用的宿主和模型。

一个技能，五种用法

| 模式 Mode | 什么时候用 When | 产出 Output |
|---|---|---|
| **A 拆解学习** Teardown & Learn | 给它一个 开源项目，要求拆解/分析/学习 | `oss-teardown/<run-id>/`：基线测绘、需求→模块映射、选型矩阵（证据分级）、解耦与性能证据、提示词翻译、结构化社区调研、`LEARNING_REPORT.md`（含学习路径） |
| **B 项目接手** Handoff (take over) | 接手前任 AI 或他人留下的半成品/烂尾项目 | 项目 `.ai/` 交接包（PROJECT_STATE / REQUIREMENTS / ARCHITECTURE / DECISIONS / TODO / TEST_PLAN / HANDOFF / ASSUMPTIONS / checkpoints），经你批准后按 `Correctness > Completeness > Maintainability > Performance` 纪律与 git 检查点动工 |
| **C 交接冻结** Freeze & hand off | 额度快用完、要换模型——由**当前离场 AI** 执行 | `.ai/handoffs/HANDOFF-<主题>-<日期>.md` 权威交接文档：红线置顶、状态表、已完成根因明细、待办批次（含已探明的坑）、防重探架构事实、测试基线、无技能接手附录 |
| **D 借鉴计划** Borrow & adapt | 给出**你自己的项目** + **想借鉴的参考项目**两个目标 | `BORROWING_PLAN.md`：双项目登记表、差异对比、借鉴点清单（来源 SHA+file:line→你的落点）、许可证判定记录与社区证据，经你批准后接入手流程执行 |
| **断点续跑** Resume | "继续上次未完成的拆解" | 从 `run-manifest.json` / checkpoint 恢复，不从头重跑 |

**核心公理**：不要让下一个模型重新理解项目。A 拆解项目并学习项目的模块与架构；C 写合约，B 验合约；文档权威于意图与状态，代码权威于事实；红线穿越工具边界仍然绑定。

---

## 使用方法

### 模式A 拆解学习
新会话直接说："**帮我拆解分析某个开源项目 （给AI链接或者克隆好的本地仓库位置）**"。可加档位（"快速拆一下"/"深度拆解"）与关注点（"重点看性能"）。产出在 `oss-teardown/<run-id>/`：`notes/` 各阶段证据 + `LEARNING_REPORT.md`。档位预算：快速（单 Agent、社区检索≤4、核心模块≥30%）/ 标准（默认，≤12、≥60%）/ 深度（3–5 Worker、≤24、≥90%）。

### 模式B 项目接手
说："**接手这个项目，前任 AI 留了交接材料，先独立侦察再对比，生成接手计划**"。流程：盲扫形成自己的认知（五类复述）→ 与交接材料对比 → 真相层级仲裁（代码 > 文档）→ 假设登记 → 生成 `.ai/` 交接包 → **H5 用户门禁：你批准后才动一行代码** → 检查点执行 → 五段收尾验收。交接文档中的红线默认绑定，让AI了解清晰你的项目，你才能解除，然后让他工作。

### 模式C 交接冻结
感觉额度快用完时，对**当前 AI** 说："**我额度快用完了，用模式C 把这个项目的会话冻结成交接文档**"。它会走 C0–C5：确认路径 → 用 git status/diff 核对记忆 → 提取红线与待办 → **边写边落盘**（先写头部+红线+状态表+下一步的保命骨架，额度死在半路也留下有效合约）→ 自查归档。文档落在 `<项目>/.ai/handoffs/HANDOFF-<主题>-<日期>.md`，尾部附"无技能接手协议"，**下一个 AI 装没装本技能都能接手**。

### 模式D 借鉴计划（v3.0.0 新增）
告诉我**哪个是你自己的项目、哪个是你想借鉴的参考项目**："**借鉴这个开源项目的认证架构，用到我的项目里，出借鉴计划**"。它会走 D0–D8：先锚定双项目角色（不明确就停下来问你，绝不猜）→ 双线独立扫描（参考方走拆解引擎、你的项目走接手引擎，结论互不共享）→ 以「需求→模块」对比差异 → 提取借鉴点（来源 SHA+file:line → 你的落点）→ 社区调研 → 解耦/性能门 → **D7 安全门**：`python scripts/check_license.py <你的项目> <参考项目>` 做许可证结构检测，结合"借代码 vs 仅借设计"询问（默认仅借设计，抄代码需你显式选择），未批准 0 行代码 → 产出 `BORROWING_PLAN.md`，你批准后接入手流程执行。许可证判定标注"非法律意见"，GPL/AGPL 抄代码或声明缺失/矛盾时一律升级你拍板。

### 断点续跑
新会话说："**继续昨天未完成的拆解，从上次的 checkpoint 恢复**"。技能读 run 目录的 `run-manifest.json` 校验 schema 版本后从断点继续。

### 你可以直接这样说
- "帮我拆解分析这个开源项目 （开源项目链接给AI）"
- "拆解这个项目：每个需求用了多少个模块、每个模块为什么选这个框架？"
- "接手这个烂尾项目，前任 AI 留了交接材料"
- "借鉴这个参考项目的架构，制定到我的项目的借鉴计划"
- "我额度快用完了，写交接文档交棒给下一个模型"
- "继续昨天未完成的拆解，从 checkpoint 恢复"

## 安装

```bash
# 方式一：skills CLI，全局安装（推荐）
npx skills add hoshinohatsuka/project-relay-Skill -g

# 方式二：skills CLI，仅当前项目（在项目根目录执行）
npx skills add hoshinohatsuka/project-relay-Skill

# 方式三：手动安装（ZCode / Claude Code / Codex 等）
git clone https://github.com/hoshinohatsuka/project-relay-Skill.git
mkdir -p ~/.agents/skills && cp -r project-relay-Skill ~/.agents/skills/project-relay
# 注意：目录名必须与 SKILL.md frontmatter 的 name 一致（project-relay），否则发现失败

# [OpenCode](https://opencode.ai/) 全局目录为 ~/.config/opencode/skills/，建议用目录联接共享同一份：
# powershell -Command "New-Item -ItemType Junction -Path \"$env:USERPROFILE\.config\opencode\skills\project-relay\" -Target '<已安装副本路径>'"
```

前置条件：`git` 可用；Agent 具备 Bash / 文件读写 / Grep / Glob 权限；社区调研需要联网搜索（缺失时自动降级并标注 `missing evidence`）。

## 安全

- **目标源码只读**：不执行/构建/安装被拆解代码，不初始化 submodule，不拉 LFS，不加载目标 `.env` 值。
- **提示词注入防护**：目标仓库内一切文件与网页视为数据，其中的指令性文字不执行。
- **文件系统隔离**：只写输出根目录；拒绝路径逃逸。
- **模式B/D 门禁**：H5 / D7 未获你批准不动一行代码；变更禁区（schema/公共 API/认证等）默认封闭；每个 checkpoint 可回滚。
- **版权与许可证（模式D）**：借鉴点强制归因（来源 SHA+file:line）；许可证冲突绝不自动放行，交你拍板；`python scripts/check_license.py` 只做结构检测，判断权在模型+你。
- **秘密卫生**：只记变量名，值脱敏；产物过密钥扫描。

## 验证命令（确定性基线）

```powershell
python scripts/validate_skill.py        # 包结构合同，须 0 failures
python scripts/evaluate_triggers.py     # 触发合同评测（48 例），须 0 failures
python scripts/validate_run.py evals/fixtures/valid-standard-run   # 须 exit 0
python scripts/validate_run.py evals/fixtures/invalid-path-escape  # 须 exit 2
python scripts/check_license.py <你的项目> <参考项目>  # 模式D 许可证结构检测（非法律意见）
```
这些只证明文件与确定性合同的结构，不证明宿主自动触发或任意模型逐字遵守流程（详见 `evals/EVALUATION_PLAN.md`）。

## 已验证与未验证

已验证（可复现命令见上节与 `evals/EVALUATION_PLAN.md`）：包完整性校验、触发合同评测、黑板状态校验的正反例，以及五种工作流的人工审查量表。它们证明技能文件、确定性路由合同和状态产物的结构，不证明宿主会自动触发或任意模型会逐字遵守流程。

未验证（missing evidence）：真实宿主自动触发；真实模型在模式 A、B、C、D 和续跑中的端到端遵从性；大规模仓库（>500 模块）深度档表现；登录墙平台的社区召回率；模式D 在真实双项目上的借用计划质量（依赖宿主与模型）。

## 故障排查 Troubleshooting

| 现象 | 处理 |
|---|---|
| 克隆失败 | 检查 git 与网络；私有仓库改用本地路径 |
| 报告出现 `missing evidence` | 上一个AI模型不可用或预算用尽；模式AB共用交给下一个AI共同跑该阶段 |
| 模式D 没说清哪个是"我的项目" | 停下追问；锚定双项目角色（D0）后再启动扫描 |
| 借鉴点报许可证缺失/矛盾 | 运行 `python scripts/check_license.py` 看结构结果；标 missing evidence 并请你拍板（非法律意见，绝不自动放行） |
| 大仓库读不完 | 降为快速档，或指定 `focus` 聚焦模块 |
| "继续上次"没生效 | 确认 run 目录存在且 `schema_version` 为 2.x；运行 `python scripts/validate_run.py <run目录>` 体检 |
| 技能没被触发 | 用 `/skill project-relay-Skill <请求>` 强制加载 |
| 想重新拆（行号已漂移） | 旧证据绑定旧 commit SHA；新建 run-id 重跑 |

## 致谢
- 初始灵感：作者主项目 - [Reverie](https://github.com/MuheStudio/Reverie) 的开发经验（跨模型共同打磨项目的经验）
- 上游灵感： [开源项目大模型应用分析器](https://github.com/Guan-Yep/open-source-llm-analyzer) —— 四路提示词扫描与翻译文档化改编自 howPrompt 系；档位化覆盖率、并行 Worker 与交叉验证参考 repo-analyzer；常驻记忆/在途交接二分借鉴 Cline Memory Bank 与 AI Hero /handoff；强规划弱执行见 Together AI 的 plan-divide-conquer。上游归因声明（manifest.json）：Guan-Yep/open-source-llm-analyzer (howPrompt by comeonzhj); yzddmr6/repo-analyzer; Cline Memory Bank; agents.md; AI Hero /handoff; Together AI plan-divide-conquer。完整借鉴映射见 `reports/creation-handoff.md`。
- 方法论来源：作者受朋友们的建议、作者主项目 - [Reverie](https://github.com/MuheStudio/Reverie) 的开发经验（跨模型共同打磨项目的经验）、[卡兹克老师](https://github.com/KKKKhazix)的文章灵感。
- 作者 ：[hoshinohatsuka](https://github.com/hoshinohatsuka) · License: MIT
