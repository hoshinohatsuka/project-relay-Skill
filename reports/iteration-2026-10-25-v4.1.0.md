# 迭代报告 v4.1.0：模式B/C 上下文压缩增强（2026-10-25）

## 用户拍板记录

1. **方向**（2026-10-25 指令）：先学习上下文压缩技术（cc-notebook、AI-fundamentals、百度博客、codex 源码），再优化模式C——导出交接文档后必须再产出「当前会话上下文.md」；模式B 是真正的"项目接手"，必须承接该新产物，使下一个 AI 完整理解上一个 AI 的流程与用户意图。
2. **方法**（用户纠偏，同日）："这个计划太急躁了，应当用本技能来优化本技能：用模式D对比你的学习成果和项目接手技能的模式C/B"——先行模式D 对比，产出借鉴计划，再按清单实施。模式D 对比成果归档于 `上下文压缩机制/05-模式D-对比与借鉴计划.md`。
3. 版本 `v4.1.0`（minor：新增产物与承接规则，向后兼容——旧 run 无当前会话上下文.md 时 B 端按无意图材料处理）；重装三处安装副本按惯例执行；不 push（发布门禁）。

## 参考侧调研（三源 + 诚实的 missing evidence）

| 来源 | 取得方式 | 证据等级 |
|---|---|---|
| win4r/cc-notebook《Claude_Code上下文压缩算法深度分析》 | raw 全文提取 | 转述（逆向分析，2026-03-31 快照） |
| ForceInjection/AI-fundamentals《claude-code-context-compression》（Apache-2.0） | raw 全文提取 | 转述（与上互证） |
| openai/codex@970111f6cb 压缩子系统（本地只读克隆） | 源码深读 9 文件 | validated（file:line） |
| 百度星河社区博客《上下文压缩实践》 | **不可达**（JS 渲染，四工具失败，无镜像） | missing evidence——借鉴点均不依赖此源 |

学习成果归档 `上下文压缩机制/00–03`；codex 正式拆解报告 + 黑板（validate_run ok，13 证据）在 `../../codex/拆解结果/`。

## 借鉴映射（J1–J13 摘要，全文见 05 计划）

| 编号 | 借鉴 | 来源 | 落点 |
|---|---|---|---|
| J1 | C 产出两件套（新增 当前会话上下文.md） | codex prompt.md:1（压缩即交棒） | SKILL 模式C 全节、TPL 模板13、HG §9 |
| J2 | 用户消息原文保留（保最近删最旧） | codex compact.rs:719-798 | 配套模板①⑨段 |
| J3 | 九段结构化摘要 | CC 9 段式 + codex 4 要点 | 配套模板 |
| J4 | 接手者前置语（中文化改写非直译） | codex summary_prefix.md:1 | 配套模板头部 |
| J5 | 固定文件名 + REVISION 两件同步 | codex compact.rs:617-619 防递归 | SKILL C4、TPL、HG |
| J6 | 新信息优先 + 最近对话直接引用 | CC 摘要第9段；codex .rev() | 配套模板⑨段 |
| J7 | 三步保命落盘 | CC 保命哲学（与既有 C4 互证） | SKILL C4、HG §9 C4 |
| J8 | B 端分区承接（意图段先读/状态段 H2 读）+ H2 意图仲裁 + H7 过时标注 | codex compact.rs:646-695 重注入 + 既有 H1/H2/H7 | SKILL L62-64、HG §1/2/3/8 |
| J9 | C0 主动预警 | CC 82% 水位理念 | SKILL C0、HG §9 C0 |
| J10 | C0 用户特别嘱咐 | codex compact_prompt 可覆盖 | SKILL C0、配套模板头部 |
| J11 | 决策含被否方案（防重提） | codex "key decisions made" | 配套模板②段 |
| J12 | 术语黑话 + 文件索引（引文不贴全文） | CC Key Concepts；codex "critical data" | 配套模板③④段 |
| J13 | 软预算 ≤6KB + 引文规则（数字 hypothesis） | CC 预算原理 validated | 配套模板规则区 |

不采纳项（断路器/"Resume directly"/cache_edots 微压缩/水位数字等 7 项）及理由见 05 计划 D4。

## 变更清单（file 级）

| 文件 | 变更 |
|---|---|
| SKILL.md | description C 段；L19 模式表 C 行；L44 C→B 闭环句；L62 H0 搜索位+意图材料；L63 H1 分区阅读；L73 导语两件套；L77 C0 预警+嘱咐；L81 C4 三步落盘；L82 C5 两件自查；L84 指引；frontmatter 4.1.0 |
| references/templates.md | 模板13 改"交接两件套"；自查清单追加 5 项；新增配套件九段模板（四反引号外层 fence）+ 软预算/分区阅读规则 |
| references/handoff-guide.md | §1 搜索位+意图材料；§2 H1 分区阅读段；§3 H2 意图仲裁；§8 H7 配套件过时标注；§9 C0 两条新增、C4 三步、新增 §9.6 配套产物、C5 两件、C→B 闭环 |
| agents/interface.yaml | handoff input/output 补意图材料与分区；freeze output 改两件套 |
| README.md | 模式B 节分区承接；模式C 节两件产物 |
| readme-EN | B/C 两行 + Mode C 节（历史遗留四模式结构，本次仅同步 B/C 行，同 v4.0.0 声明） |
| evals/scenario_matrix.json | C-freeze 验收 +2、B-misleading-handoff 验收 +1（案例数 12 不变；trigger_cases 58 例零改动） |
| reports/skill-ir.json | intent.description/job_to_be_done C 段同步；generated_at |
| manifest.json | version 4.1.0、updated_at |

## 验证与兼容声明

- 六条门禁命令结果见下（本文件末尾"验证记录"）。
- **旧 run 兼容**：无 当前会话上下文.md 的项目，B 端 H0/H1 分区规则自然退化为原有行为（无意图材料即按现状处理）；validate_run.py 零依赖该文件名。
- 触发合同不变：评测测技能级触发而非模式路由；C 的新产物不引入新触发面。

## 验证记录

| 门禁 | 结果 |
|---|---|
| validate_skill.py | ok=True，0 failures，version=4.1.0 |
| evaluate_triggers.py | 58/58 通过 |
| validate_run valid-standard-run / invalid-path-escape / valid-transition-run / invalid-transition-run | exit 0 / 2 / 0 / 2（符合预期） |
| check_license.py（模式D D7 门禁，skill 仓 vs codex 克隆） | ok=True：MIT ↔ Apache-2.0，无缺失无矛盾 |
| SKILL.md 字节 | 28,170 ≤ 30,000（manifest context_budget_bytes） |
| CommonMark fence 检查（templates/handoff-guide/SKILL/README） | 未闭合：无 |
| 新词覆盖 | 「当前会话上下文」出现在 SKILL/templates/handoff-guide/interface.yaml/README/readme-EN/scenario_matrix 七处活文档 |
| codex 拆解黑板 validate_run | ok=True，13 证据，0 错误 |

commit：见 git log（a37c964 之后）；未 push（发布门禁）。
