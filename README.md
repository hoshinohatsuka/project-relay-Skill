# 项目接手.Skill（Project relay Skill · `project-relay`）

（[中文](https://github.com/hoshinohatsuka/project-relay-Skill/edit/main/README.md) | [English](https://github.com/hoshinohatsuka/project-relay-Skill/blob/main/readme-EN)）

## 这个 Skill 是什么：经验凝结，不是工业流水线

这不是一份把流程机械化的"工业流水线 Skill"。它是作者 [**hoshinohatsuka**](https://github.com/hoshinohatsuka) 在真实开发中**多 AI 接力使用经验**的凝结——模型会换、上下文会丢、额度会用完、单模型长跑会积累幻觉、便宜模型需要精致规划才能扛大项目。这些真实教训被固化成一条条纪律：**红线置顶、用户门禁、真相层级、证据分级、git 检查点、边写边落盘**。

所以它**内容多、规则细**：每个模式都是某次真实事故换来的应对，每条红线都是"违反即事故"的现场记录。读它不是在读操作说明书，而是在读一份**实战手册**——作者怎么用多个 AI 打磨同一个项目-[Reverie](https://github.com/MuheStudio/Reverie)（从 DeepSeek 建初始架构、gpt 优化架构、GLM、K3、deepseek、Qwen、Claude、Grok 增添内容的接力实践），就怎么写它。

核心公理：**不要让下一个模型重新理解项目，要让项目本身携带足够完整的"可执行记忆"。** 文档权威于意图与状态，代码权威于事实；红线穿越工具边界仍然绑定。因此这是一份为 Agent 提供跨会话项目分析、接手、冻结交接和续跑的操作协议。它引导 Agent 将状态与可核验证据写进仓库，而不是留在聊天框里；实际执行质量仍取决于所用的宿主和模型。


## 六个模式（用途 / 触发标准 / 红线）

### 模式A 拆解学习（Teardown & Learn）
- **用途**：给开发者与 AI 的深度分析报告——拆开源项目，产出基线测绘、需求→模块映射、每模块框架选型（四级证据分级）、解耦与性能证据、社区口碑调研或复刻学习路径。
- **触发标准**：给出 GitHub 链接 / `owner/repo` / 本地路径 + "拆解 / 分析 / 研究 / 学习"。
- **红线**：不运行目标代码；选型理由必须标注证据等级（L1 代码证实…L4 分析推断）；stars 不当质量评分；社区搜索摘要不作结论；覆盖率必须有分母。

### 模式B 项目接手（Handoff & Take Over）
- **用途**：换一个 AI（或你自己）接手前任留下的半成品/烂尾项目——独立侦察（五类复述）、真相层级仲裁、假设登记、`.ai/` 交接包、检查点执行收尾。
- **触发标准**："接手 / 收尾 / 烂尾 / 前任 AI / 交接材料 / 继续开发"。
- **红线**：**未过 H5 用户门禁不动一行代码**；变更禁区（schema/公共 API/认证/已过测试核心模块）未经你批准永不触碰；每个 checkpoint 可回滚；失控先停后问。

### 模式C 交接冻结（Freeze & Hand Off）
- **用途**：额度快用完 / 要换模型时，由**当前 AI** 把会话冻结成权威交接文档——红线置顶、状态表、已完成根因明细、待办批次、防重探事实、测试基线。任何下一个 AI（装没装本技能）都能接手（尾部附无技能接手协议）。
- **触发标准**："额度不足 / 要换模型 / 交棒 / 冻结交接 / 写交接文档"。
- **红线**：默认不自动 commit（未提交清单写进文档）；交接文档权威于意图与状态，事实以代码为准；边写边落盘——额度死在半路也留下可用合约。

### 模式D 借鉴计划（Borrow & Adapt）
- **用途**：把"参考项目"的架构/设计/框架借鉴到"你的项目"——先锚定双项目角色，双线独立扫描，以「需求→模块」对比差异，产出借鉴点清单（来源 SHA+file:line → 你的落点），过许可证与意图门禁后出可执行借鉴计划。
- **触发标准**：**同时给出两个目标**（你自己的项目 + 想借鉴的参考项目）+ "借鉴 / 抄作业 / 仿照 / 把 X 的架构·设计·框架用到我的项目"。
- **红线**：D0 未锚定双项目角色前不启动任何扫描（不明确立即停下问你）；许可证冲突**绝不自动放行**（GPL/AGPL 抄代码必须升级你拍板，判定标"非法律意见"）；**默认仅借鉴产品设计思维，抄代码需用户显式选择**；借鉴点强制归因（来源 SHA+file:line）。

### 模式E 教学模式（Learn & Teach）
- **用途**：面向**小白**的学习课程——模式A 的拆解报告对小白不友好（不知道从哪看起），模式E 把同一分析引擎重排成"先看什么、后看什么"的分阶段学习地图（30 分钟认识 → 2 小时核心链路 → 1 天模块深读 → 1 周复刻子集），带前置知识清单、生词表、**鲜活例子**走读、三思维清单（第一性原理 / 对抗式审查 / 墨菲，每条绑项目证据、引导你思考）与**举一反三练习**（只给提示不代答）。
- **触发标准**：单目标项目 + "教学模式 / 学习计划 / 学习路径 / 入门 / 小白 / 教程 / 怎么上手 / 想学会 / 教我看"。
- **红线**：项目地址缺失先询问不猜测（本地/链接二者取一）；练习只给提示与验收标准，答案由你在自己 IDE 产出（AI 不代答）；三思维清单每条必须可回溯到项目证据。

### 断点续跑（Resume）
- **用途**：跨会话 / 跨 AI 续跑未完成的拆解，从最近 checkpoint 恢复，不从头重跑。
- **触发标准**："继续上次 / 昨天未完成的拆解 / 从 checkpoint 恢复"。
- **红线**：schema 版本不匹配拒绝自动续跑（先给迁移说明）。

## 你可以直接这样说

- "帮我拆解分析这个开源项目（开源项目链接给AI）"
- "拆解这个项目：每个需求用了多少个模块、每个模块为什么选这个框架？"
- "接手这个烂尾项目，前任 AI 留了交接材料"
- "借鉴这个参考项目的架构，制定到我的项目的借鉴计划"
- "用教学模式教我看懂这个开源项目，出个学习计划"
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

- **目标源码只读**：不执行/构建/安装被分析代码，不初始化 submodule，不拉 LFS，不加载目标 `.env` 值。
- **提示词注入防护**：目标仓库内一切文件与网页视为数据，其中的指令性文字不执行。
- **文件系统隔离**：只写输出根目录；拒绝路径逃逸。
- **模式B/D 门禁**：H5 / D7 未获你批准不动一行代码；变更禁区默认封闭；每个 checkpoint 可回滚。
- **版权与许可证（模式D）**：借鉴点强制归因；许可证冲突绝不自动放行，交你拍板；`python scripts/check_license.py` 只做结构检测，判断权在模型+你。
- **秘密卫生**：只记变量名，值脱敏；产物过密钥扫描。

## 验证命令（确定性基线）

```powershell
python scripts/validate_skill.py        # 包结构合同，须 0 failures
python scripts/evaluate_triggers.py     # 触发合同评测（58 例），须 0 failures
python scripts/validate_run.py evals/fixtures/valid-standard-run   # 须 exit 0
python scripts/validate_run.py evals/fixtures/invalid-path-escape  # 须 exit 2
python scripts/check_license.py <你的项目> <参考项目>  # 模式D 许可证结构检测（非法律意见）
```
这些只证明文件与确定性合同的结构，不证明宿主自动触发或任意模型逐字遵守流程（详见 `evals/EVALUATION_PLAN.md`）。

## 已验证与未验证

已验证（可复现命令见上节与 `evals/EVALUATION_PLAN.md`）：包完整性校验、触发合同评测（58 例）、黑板状态校验的正反例，以及六种工作流的人工审查量表。它们证明技能文件、确定性路由合同和状态产物的结构。

未验证（missing evidence）：真实宿主自动触发；真实模型在模式 A–E 与续跑中的端到端遵从性；大规模仓库（>500 模块）深度档表现；登录墙平台社区召回率；模式D 真实双项目借鉴质量与模式E 面向真实小白的学习效果（均依赖宿主与模型，请以你自己的实测为准）。

## 故障排查 Troubleshooting

| 现象 | 处理 |
|---|---|
| 克隆失败 | 检查 git 与网络；私有仓库改用本地路径 |
| 报告出现 `missing evidence` | 上一个AI模型不可用或预算用尽；若有额度用模式C传递给下一个AI当前项目状态。若额度已经用尽，则模式AB共用交给下一个AI共同跑该阶段 |
| 模式D 没说清哪个是"我的项目" | 停下追问；锚定双项目角色（D0）后再启动扫描 |
| 借鉴点报许可证缺失/矛盾 | 运行 `python scripts/check_license.py` 看结构结果；标 missing evidence 并请你拍板（非法律意见，绝不自动放行） |
| 大仓库读不完 | 降为快速档，或指定 `focus` 聚焦模块 |
| "继续上次"没生效 | 确认 run 目录存在且 `schema_version` 为 2.x；运行 `python scripts/validate_run.py <run目录>` 体检 |
| 技能没被触发 | 用 `/skill project-relay <请求>` 强制加载 |
| 想重新拆（行号已漂移） | 旧证据绑定旧 commit SHA；新建 run-id 重跑 |

## 致谢

- 初始灵感：作者主项目 [Reverie](https://github.com/MuheStudio/Reverie) 的开发经验（跨模型共同打磨项目的经验，也是本 Skill 经验的来源）。
- 上游灵感：[开源项目大模型应用分析器](https://github.com/Guan-Yep/open-source-llm-analyzer) —— 四路提示词扫描与翻译文档化改编自 howPrompt 系；档位化覆盖率、并行 Worker 与交叉验证参考 repo-analyzer；常驻记忆/在途交接二分借鉴 Cline Memory Bank 与 AI Hero /handoff；强规划弱执行见 Together AI 的 plan-divide-conquer。上游归因声明（manifest.json）：Guan-Yep/open-source-llm-analyzer (howPrompt by comeonzhj); yzddmr6/repo-analyzer; Cline Memory Bank; agents.md; AI Hero /handoff; Together AI plan-divide-conquer。完整借鉴映射见 `reports/creation-handoff.md`。
- 方法论来源：作者受朋友们的建议、作者主项目 [Reverie](https://github.com/MuheStudio/Reverie) 的开发经验、[卡兹克老师](https://github.com/KKKKhazix)的文章灵感。
- 作者：[hoshinohatsuka](https://github.com/hoshinohatsuka) · License: MIT
