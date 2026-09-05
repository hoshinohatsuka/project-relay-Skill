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
