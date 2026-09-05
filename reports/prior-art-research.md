# Prior-Art Research — project-relay v2.0.0

调研日期：2026-09-05（v1.0.0 首轮）与 2026-09-05（v2.0.0 增补，针对接手/黑板协议方向）。
方法与诚实声明：来源为联网检索摘要与页面抓取；**未运行 `npx skills find` 与 SkillsMP 目录脚本，未取到 skills.sh 安装量与 SkillsMP 星标（missing evidence）**。本文不使用"热门/高热度"等不可复核表述，只记录可复核的机制与链接；检索摘要仅作线索，机制描述以标注的来源页为准。

## 1. 查询记录

| # | 查询 | 日期 | 主要产出 |
|---|---|---|---|
| Q1 | agent skill "SKILL.md" analyze github repository deep dive codebase analysis | 2026-09-05 | repo-analyzer、repomix-explorer、repository-analyzer、codebase-summarizer、docs-seeker |
| Q2 | npx skills find "repository analysis" claude skill | 2026-09-05 | 同上集合 |
| Q3 | claude agent skill research twitter X huggingface "stack overflow" community insights | 2026-09-05 | x-research-skill、huggingface/skills、Stack Overflow for Agents、awesome-agent-skills |
| Q4 | AI coding agent project handoff "HANDOFF.md" OR "memory bank" session continuity skill | 2026-09-05 | Session Handover、Claude Code Handoff、AI Hero /handoff、Cline Memory Bank、roo-code-memory-bank、claude-code#11455 |
| Q5 | "AGENTS.md" standard spec memory bank cline schema persistent project state | 2026-09-05 | agents.md（60k+ 项目采用、最近文件优先）、cline/prompts memory-bank 规则、混合协议 |
| Q6 | skill "strong model" plan "cheap model" execute relay handoff pipeline | 2026-09-05 | Together AI plan-divide-conquer、模型路由文章、CodeRescue (arXiv)、PEAR 基准、agent-relay (PRPM) |

## 2. 直接上游（血统）

- **Guan-Yep/open-source-llm-analyzer**（MIT）：五阶段提示词分析；四方法检索与翻译文档化模板的直接来源。
- **comeonzhj/howPrompt**：四方法检索模式源头。

## 3. 拆解/分析类技能

- **yzddmr6/repo-analyzer**（MIT）：8 阶段架构拆解、Quick/Standard/Deep 覆盖率（30/60/90）、并行子代理、外部调研、交叉验证、Mermaid。→ **adapt**：档位、并行、交叉验证；**reject**：动态报告结构与交互式问答（非交互场景会卡）。
- **repomix-explorer / docs-seeker**：repomix 打包后分析。→ **reject**：外部 CLI 依赖，内置 Grep/Glob 足够。
- **jackspace/repository-analyzer、codebase-summarizer**：通用总结。→ **reject**：无需求映射/选型分级/社区维度。

## 4. 会话交接与记忆库

- **Cline Memory Bank**（docs.cline.bot；方法论而非固定功能）：结构化 markdown 常驻上下文（projectbrief/activeContext/progress）。→ **adapt**：常驻记忆 vs 在途状态二分。
- **AI Hero /handoff**：明确"standing context vs in-flight handoff；工作落地后 handoff 死亡"。→ **keep**：成为 `.ai/` 交接包维护规则。
- **Session Handover / Claude Code Handoff / Superpowers handoff / roo-code-memory-bank / rumotion 滚动 handoff.md**：均为单 Agent 会话续传（同一 Agent 换会话），rumotion 支持"任意模型可续"。→ **differentiate**：本技能做跨模型接力（强规划→弱执行）+ 真相层级仲裁 + 禁区/检查点执行纪律。
- **agents.md**（agents.md，60k+ 项目）：静态指令标准、最近文件优先。→ **interop**：`.ai/` 动态状态与之共存，不覆盖。

## 5. 强规划/弱执行与多 Agent

- **Together AI "Plan, divide, and conquer"**：强模型 Orchestrator 出计划，弱 Worker 并行执行。→ **adapt**：档位化 Worker 数与互斥分区。
- **模型路由实践与反方观点**（getunblocked、dev.to "AI Bill Grows in the Agent Loop"）：便宜模型优先只在"失败可检测且重试便宜"时省钱。→ 已写入 relay-principles 已知边界。
- **CodeRescue (arXiv 2607.19338)**：预算校准的恢复路由。**PEAR (arXiv 2510.07505)**：planner-executor 的安全弱点基准。→ 纳入对抗审查：弱执行者是接力的隐藏弱点 → 检查点 + 验证门禁为反制。
- **agent-relay (PRPM)**：多 worker 中继编排。→ 参考，不依赖。

## 6. 缺口综合（invent 空间）

现有技能/协议均未同时具备：①需求→模块计数与口径声明；②选型理由四级证据分级；③跨九平台结构化社区证据（查询/URL/日期/来源类型/可访问状态）；④跨模型接力中的真相层级仲裁与假设登记；⑤变更禁区 + 用户门禁 + git 检查点的执行纪律；⑥与拆解学习共享同一理解引擎（拆解产物直接喂接手流程）。

## 7. missing evidence 清单

- skills.sh 安装量、SkillsMP 星标、各来源页全文逐字核对。
- 深度档 3–5 Worker 在大仓库上的实测收益（待用户本地真实测试）。
- 登录墙平台（知乎/小红书/Facebook/LinkedIn）无登录态召回率。

## 8. v2.1.0 增补查询（2026-09-06，交棒文档方向）

| # | 查询 | 主要产出 |
|---|---|---|
| Q7 | handoff document template "next agent"/"next session" coding AI best practices | AI Hero /handoff（"next agent 把文档当合约"）、agent-toolkit/session-handoff（Important Context/Decisions Made/Immediate Next Steps 三段式）、HandoffKit（按工具粘贴指引）、JD Hodges HANDOVER.md（单文件滚动）、r/ClaudeAI"handoff 成为一等模式" |

结论：公共模板普遍缺三样——红线置顶、防重探架构事实、测试基线数字；这三样来自用户的 Reverie 范例，构成模式C 模板的差异化。另：v2.1.0 的"模式C 交棒冻结"（离场 AI 在额度濒尽时主动冻结会话为合约文档）在检索范围内未见同类技能实现，属 invent。
