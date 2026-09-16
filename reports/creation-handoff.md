# Creation Handoff — project-relay v2.0.0

创建：2026-09-05（v1.0.0）· 融合升级：2026-09-05（v2.0.0）· 作者：hoshinohatsuka（https://github.com/hoshinohatsuka）· 模式：Production

## 研究过的参照技能与协议

1. **Guan-Yep/open-source-llm-analyzer**（直接上游，MIT）——四路提示词扫描与翻译文档化。
2. **comeonzhj/howPrompt**（血统上游）——检索模式源头。
3. **yzddmr6/repo-analyzer**——档位化覆盖率、并行 Worker、外部调研、交叉验证。
4. **Cline Memory Bank / agents.md / AI Hero /handoff / rumotion 滚动交接**——常驻记忆 vs 在途交接二分、`.ai/` 状态目录与 AGENTS.md 互操作。
5. **Together AI plan-divide-conquer / 模型路由实践 / CodeRescue / PEAR**——强规划弱执行模式及其已知弱点。
6. **用户侧方法论**：作者与 @钰 的跨模型接力实战、GPT 对话 22 节协议化综合、卡兹克审查常用语。
7. **第二思考**（另一 AI 的 v2 评审）——黑板协议、确定性校验、证据分级、安全硬化。

## keep / adapt / reject / invent 映射（v2.0.0 累计）

| 判定 | 机制 | 来源 | 去向 |
|---|---|---|---|
| keep | 渐进披露结构、常驻/在途二分、四路扫描 | 通用规范 / AI Hero / howPrompt 系 | SKILL.md / workflow-detail |
| adapt | 三档覆盖率、并行 Worker、交叉验证 | repo-analyzer | P0/P4 + multi-agent-handoff |
| adapt | 强规划弱执行、互斥分区、单写者合并 | Together AI / 第二思考 | 模式B + 黑板协议 |
| adapt | 八不变量、确定性状态校验、四级证据分级、安全硬化 | 第二思考 | SKILL.md 不变量段 + validate_run.py + teardown-guide + 安全边界 |
| reject | 动态报告结构/交互式问答（repo-analyzer）、repomix 依赖、全量输出评测 fixture（暂缓）、保留旧名（与用户决定冲突） | 各来源 | —— 理由见 iteration report §2 |
| invent | 需求→模块计数与口径、选型理由四级分级、九平台结构化社区证据、真相层级仲裁、假设登记、变更禁区+用户门禁+检查点、拆解学习与接手共享理解引擎 | 本技能原创 | teardown-guide / handoff-guide / SKILL.md |

## 设计优势标注

- **validated**：触发评测 33/33（含接手/续跑/混合意图/错别字）；包校验 0 failures；SKILL.md 11532 字节（<14KB 生产档）；validate_run.py 对正常/损坏 run 目录判定正确（见冒烟记录）。
- **validated**：接手模式 H0–H4 在合成烂尾项目上抓住前任交接材料的错误声明（JWT vs session）并按真相层级仲裁。
- **hypothesis**：深度档 3–5 Worker 在大仓库的实际收益；黑板协议对跨日续跑的真实体验——待用户本地真实测试。
- **hypothesis**：H5 用户门禁在长会话中的遵守率。

## 安全与治理

- 目标源码只读 + 注入防护 + 文件系统隔离 + 秘密卫生（详见 SKILL.md 安全边界）。
- 模式B 三重防线：H5 用户门禁、变更禁区、每 checkpoint 可回滚。
- 发布边界：本地发布候选，未 push 未 Release。

## missing evidence 清单

宿主自动触发（需真实会话）、深度档大仓库表现、登录墙平台召回率、H5 门禁长会话遵守率。

---

## v2.1.0 增补（2026-09-06）

新增**模式C 交棒冻结**（C0–C5，离场 AI 在额度濒尽时把会话冻结成权威交接文档）与**模式B 跨 AI 加强**（H0 交接文档标准搜索位、红线绑定规则、文档基线重跑复核、无技能接手协议附录、并行副本交叉验证）。来源：用户与 DarkiIne 的多模型接力实践、Reverie 交接文档范例（八节结构成为模板骨架）、2026-09-06 交接文档模板调研（AI Hero /handoff 等）。keep/adapt/invent 详情与对抗审查见 `reports/iteration-2026-09-06-v2.1.0.md`。关键新公理：11（文档权威于意图与状态，代码权威于事实）、12（红线穿越工具边界）。设计优势标注：C→B round-trip 冒烟为 **validated**；真实濒尽额度场景体验为 **hypothesis**（待用户本地测试）。

## v2.1.1（发布前定稿，2026-09-06）

中文定名「项目接手.Skill」（标识与安装目录保持 `project-relay`，ZCode 规范要求 kebab-case ASCII）；README 重写为中英双语（各模式用法 + `npx skills add` 安装 + 安全模型 + 诚实边界）；作者已本地实测确认功能完善，README 诚实边界同步更新。无行为变更。

## v3.0.0 增补（2026-09-15，模式D 借鉴计划）

新增**模式D 借鉴计划**（D0–D8，双目标：用户自己的项目 + 想借鉴的参考项目）。来源：用户"借鉴计划"新想法（第一性原理：先区分用户项目/借鉴项目，不明确立即停下问；模式A/B 各自独立扫描；对比差异出借鉴点；最后做许可证与"借代码 vs 仅借设计"门禁）。用户拍板 5 项决策（见 `reports/iteration-2026-09-15-v3.0.0.md` §1）。invent 判定：**双项目映射对齐 + 来源→落点借鉴点映射 + 许可证三级判定** 在既有先例（prior-art Q1–Q8 + 本次检索）中无同类实现；D0 角色锚定硬门禁与"默认仅理念、抄代码需显式选择"为本次原创。设计优势标注：结构/触发/脚本三用例自测为 **validated**；真实双项目上的借鉴计划质量、D7 门禁长会话遵守率为 **hypothesis**（待用户本地测试）。顺带修复 2.2.0 遗留（skill-ir 2.1.1→3.0.0、README 门禁警告、安装命令仓库名、.gitignore 重建）。

## v3.1.0 增补（2026-09-16，模式E 教学模式）

新增**模式E 教学模式**（E0–E7，单目标 + 学习意图，面向小白）。来源：用户"学习计划"新想法（模式A 产分析报告对小白不友好→把同一分析引擎重排成课程：分阶段学习地图、鲜活例子走读、举一反三练习、第一性原理/对抗式/墨菲三清单教学化）。用户拍板 5 项决策（命名"教学模式"、版本 v3.1.0、练习档位沿用先例 8–12/3–5、三清单每清单 5–8 条、默认小白画像由 E0 询问调整）。先例 keep/adapt/reject/invent 与对抗审查见 `reports/iteration-2026-09-16-v3.1.0.md`。设计优势标注：结构/触发（58 例全过）为 **validated**；模式E 面向真实小白的端到端学习效果为 **hypothesis**（待用户本地测试）。同期决策：SKILL.md 预算 25,000 字节可略超（1M 上下文时代以精确性优先）。

## v3.2.0 增补（2026-09-16，aif-handoff 理念借鉴：收敛评审门/结构化契约/版本号/状态机/审计快照/运行时画像）

用户用模式D 对 [lee-to/aif-handoff](https://github.com/lee-to/aif-handoff)（290★/39fork/MIT，Autonomous Kanban 应用）做双项目拆解后批准高价值 6 条（B1–B6）**仅理念借鉴**（迭代报告：`reports/iteration-2026-09-16-v3.2.0.md`）。B1 收敛感知自动评审门与 B2 结构化评审契约（Blocking/Advisories/Previous Findings 三小节 + finding id 去重 + 前次回喂）**invent 判定为理念翻译**：参考方是数据库/状态机实现，本研究把机制转成协议规则（handoff-guide H7、learning-plan E3、templates 模板 7/19）+ 回归 fixtures，不抄参考方代码。B3 交接所有权版本号、B4 显式状态机（validate_run.py 转移表）、B5 审计可选字段、B6 运行时画像均完成落地。**validated**：结构性门禁全过（validate 0 failures、触发 58/58、validate_run 全套新旧 fixture、SKILL.md 24,906B）。**hypothesis**：收敛门真实复核效果、版本号遵守率、审计字段实际使用率（依赖宿主与模型，待用户真实测试）。新增公理 13–15。参考方归因与拆解证据保留在 `参考资料/项目接手Skill与handoff的借鉴计划/`（gitignore 隔离）。

## v3.3.0 增补（2026-09-16，aif-handoff 理念借鉴：预算冻结/租约心跳/报告自查清单）

用户继续批准模式D 中价值 3 条（B7/B8/B10）**仅理念借鉴**（迭代报告：`reports/iteration-2026-09-16-v3.3.0.md`）；B9（MCP 双向同步）落点为主项目 Reverie，非 Skill 本体，仅记录不实施。B7 预算耗尽→自动冻结+恢复（blocked_external+retry_after，三模式预算段统一引用 multi-agent-handoff §6）；B8 租约细化（claimed_until/heartbeat_at，心跳续租/过期释放/优雅释放，validate_run.py 校验 ISO 格式）；B10 每包 CHECKLIST 强制（templates 模板 8/13/14/17 自查清单节 + 模板 20 通则，不适用项写明原因）。**validated**：结构性门禁全过（validate 0 failures、触发 58/58、validate_run 全套新旧 fixture、SKILL.md 25,827B）。**hypothesis**：预算冻结跨会话续跑恢复效果、租约释放真实遵守率、自查清单对报告质量的提升（依赖宿主与模型）。新增 release_gates `budget_freeze_gate` 与 interface safety `budget_freeze`/`lease_heartbeat`。B9 状态：借鉴计划记录待 Reverie 侧拍板。
