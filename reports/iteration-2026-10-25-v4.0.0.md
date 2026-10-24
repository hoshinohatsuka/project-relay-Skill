# Iteration Report — project-relay v4.0.0（2026-10-25）

主题：**模式A 瘦身——"拆解学习"改为"项目拆解"，学习流程迁移模式E**。基线 commit `0411cb3`（v3.3.0），安全锚点 tag `pre-v4-mode-a-refactor`。

## 1. 用户拍板（4 项）

1. 模式A 更名"项目拆解"（Teardown），仅保留对任意开源项目的深度拆解；混入的"学习流程"（学习路径/复刻练习/可迁移清单）迁至模式E。
2. 出口报告 `LEARNING_REPORT.md` 改名 `TEARDOWN_REPORT.md`（与 E 的 `LEARNING_PATH.md` 对仗；无代码依赖——validate_run.py 等脚本零引用报告文件名，已核实）。
3. 版本 v4.0.0（既有模式语义重划分，非新增模式；报告结构与触发词变化对外可感知）。
4. 顺带修复 v3.3.0 拆解报告（`分析结果/LEARNING_REPORT.md`）发现的 A-01/A-02 两个 L1 级文档缺陷；发布后同步重装 ZCode / OpenCode / DeepSeek Harness 三处安装副本。

## 2. 职责划分（改后）

- **模式A 项目拆解**：产出"拆解报告"（给开发者）——基线测绘、需求→模块映射、选型矩阵、解耦与性能证据、四路扫描、社区口碑。**不再产出**学习路径/复刻练习。
- **模式E 教学模式**：所有学习/学会类意图的唯一归属（E0 已支持小白/入门/进阶三档）——在原学习地图、三思维清单、举一反三练习之上，**新增"可迁移清单"**（自模式A §9 学习路径迁入：值得复用的设计/模式/工具，标注来源 file:line）。
- P7 复核项"学习路径是否真的可执行"随迁至 E3 引导逻辑（teardown-guide.md 与 SKILL.md 均留指向说明）。

## 3. 变更清单（file:line 对照，改前 → 改后）

| 文件 | 位置 | 变更 |
|---|---|---|
| SKILL.md | frontmatter L3/L6 | description A 段改名去"学习"词、E 段补"所有学习/学会类意图统一归此模式"+可迁移清单；version 4.0.0 |
| SKILL.md | L17 模式表 | `A 拆解学习…LEARNING_REPORT.md（学会它）` → `A 项目拆解…TEARDOWN_REPORT.md（拆透它）` |
| SKILL.md | L32 不变量8 | `学习复刻` → `拆透项目（模式A）与学会复刻（模式E）` |
| SKILL.md | L36/L40 路由 | A 行去"学习"触发词（留指向 E）；E 行补统一归属 |
| SKILL.md | L46 标题 | `模式A：拆解学习（P0–P8）` → `模式A：项目拆解（P0–P8）` |
| SKILL.md | L55/L56 P7/P8 | P7 删"学习路径可执行"复核项（留迁移说明）；P8 改 TEARDOWN_REPORT.md、删"复刻练习" |
| SKILL.md | L104/L113 | E 导语补 v4.0.0 迁移声明；E7 结构补"可迁移清单" |
| SKILL.md | L128/L131 黑板 | 目录树与单写者规则改 TEARDOWN_REPORT.md |
| references/templates.md | 模板7 L82 | 删 `□学习路径可执行` |
| references/templates.md | 模板8 L85–L102 | 改名 TEARDOWN_REPORT.md / `# <项目名> 项目拆解报告`；**删 §9 学习路径节**；节号 10→9、11→10 |
| references/templates.md | 模板17 L325 | 四阶段后新增 `## 可迁移清单` 节 |
| references/templates.md | 模板20 L373 | `A 的 LEARNING_REPORT` → `A 的 TEARDOWN_REPORT` |
| references/templates.md | L173/L236、L357 后、L375 | **A-01 修复**：模板13 外层 fence 改四反引号；模板18 补闭合 fence；删文件尾孤立 fence（CommonMark 校验全部配对 ✓） |
| references/teardown-guide.md | L62/L70 | 学习者措辞中性化；P7 清单删学习路径项 |
| references/workflow-detail.md | L3 | `"拆解学习 + 可审计"` → `"项目拆解 + 可审计"` |
| references/learning-plan.md | L3/L67–76 | 第一性原理句补迁移声明；E7 结构新增第 7 项"可迁移清单"（原 7–9 顺延为 8–10） |
| references/relay-principles.md | L25 | 不变量8 复述同步 |
| references/multi-agent-handoff.md | L45 | 单写者文件名改 TEARDOWN_REPORT.md |
| agents/interface.yaml | L3/L4/L7/L9/L24–25 | short_description/default_prompt（学习报告→拆解报告）/label/output；模式E 补统一归属与可迁移清单 |
| README.md | L15–17/L36 | 模式A 节改名、用途删"可复刻学习路径"、触发删"学习"；模式E 节补承接 |
| readme-EN | L13/L21/L27/L28 | A 相关行同步（EN 仍为旧四模式结构，历史遗留，本次仅同步 A 行——**missing evidence**：EN 全量重写待后续） |
| readme-EN | L33/L35 | **A-02 修复**：Mode C / Resuming 标题与正文分行 |
| evals/scenario_matrix.json | A-small-readonly | prompt `learning report` → `teardown report`（验收语句不动） |
| evals/trigger_cases.json | teardown_action 组 | 删词 `拆解学习`（子串"拆解"仍命中，行为零差异；58 例案例全部保持——评测测"技能是否触发"而非模式路由，学习类案例瘦身后路由到 E 仍需触发技能） |
| reports/skill-ir.json | — | version/generated_at/description/job_to_be_done 同步；reports 清单补 v3.2.0/v3.3.0/v4.0.0 三份迭代报告（前两份为历史遗漏） |
| manifest.json | — | version 4.0.0、updated_at 2026-10-25（release_gates 58 例数字不变） |

## 4. Prior-art（qiaomu 纪律，轻量）

- `npx skills find "teardown repo analysis"`（2026-10-25，可访问）：仅命中 roger-235/my_skill_repo@competitive-teardown（辩论向，2 installs）——无关。
- `npx skills find "learning path project"`（2026-10-25，可访问）：命中 learning-loop@ingest、code-primer 等（各 1 install）——无"拆解/学习职责分离"同类实现。
- `search_skillsmp.py "repo teardown learning path"`（2026-10-25，可访问，11 结果/首页 10）：无同类。
- 结论：本次为用户驱动的**内部职责重划**（invent），无直接先例可抄；方法论引用既有 `reports/prior-art-research.md` 与本技能自拆解报告（`分析结果/LEARNING_REPORT.md` §8）对标结论（官方 best practices：SKILL.md body <500 行仍满足，174 行）。

## 5. 设计优势标注

- **validated**：validate_skill.py 0 failures（version 4.0.0 三处一致）；evaluate_triggers.py 58/58（删词后行为不变）；validate_run.py 四 fixture exit 0/2/0/2；templates.md fence CommonMark 校验全配对；全仓活文档残留扫描（"拆解学习/LEARNING_REPORT"）清零（历史 reports 原文按设计史保留）。
- **hypothesis**：路由层变化（"学习"意图从 A 改道 E）在真实宿主语义路由中的准确性；模式E 接收全部学习意图后对进阶学习者的实际效果；TEARDOWN_REPORT.md 新名在真实运行中的使用体验。均依赖宿主与模型，missing evidence，待真实会话冒烟。

## 6. 兼容性声明

- 旧 run 目录不受影响：黑板协议与 validate_run.py 均不依赖报告文件名；旧 run 的 LEARNING_REPORT.md 为历史产物，保持原名。
- 续跑语义不变（schema_version 仍为 2.x）。
- 发布边界：本地 commit，未 push 未 Release（发布门禁）；安装副本重装三处（ZCode / OpenCode / DeepSeek Harness）后各自跑 validate_skill.py 冒烟。

## 7. 报告自查清单（B10）

- ✅ 每条变更带 file:line（§3 表）
- ✅ 用户拍板 4 项记录在案（§1）
- ✅ prior-art 带平台/日期/结论与 missing evidence（§4）
- ✅ validated / hypothesis 分级，不冒充（§5）
- ✅ 兼容性影响显式声明（§6）
- 不适用：双项目登记表（模式D 专属）；许可证判定记录（本次无代码借鉴）
