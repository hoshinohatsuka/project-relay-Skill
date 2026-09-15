# Iteration Report — project-relay v3.1.0「模式E 教学模式」（2026-09-16）

## 1. 本次来源与动机

用户新想法"学习计划"：模式A 产"拆解报告"，对小白用户不友好——小白不知道从哪里看起。模式E 把**同一分析引擎**（P1–P6）重新编排成"课程"：分阶段学习路径、鲜活例子走读、举一反三练习、以及用户常用指令（第一性原理/对抗式/墨菲/联网调研）的教学化三清单。用户拍板：命名"模式E 教学模式"（让小白一眼懂）、版本 v3.1.0、练习档位沿用先例 8–12/3–5、三清单每清单 5–8 条、默认小白画像 + E0 询问调整。另批准 SKILL.md 可略超 25,000 字节（1M 上下文时代以精确性优先）。

## 2. 设计决策与处置

- **模式E 落为 E0–E7**：E0 目标确认（地址缺失先问、默认小白、默认全目标）→ E1 教学化侦察（复用 P1–P3 + 依赖序）→ E2 学习地图（30 分钟/2 小时/1 天/1 周 四阶段 + 前置清单 + 鲜活例子）→ E3 三思维清单（第一性原理/对抗式/墨菲，每条绑证据，引导不代答）→ E4 举一反三（Use→Modify→Debug→Create→Compare，提示+验收不代答）→ E5 社区学习调研（P6 复用）→ E6 解耦 + review/性能思维教学 → E7 汇总 LEARNING_PATH.md（含切模式A 入口）。
- **先例处置（repo-learner-suite，MIT，4★）**：keep/adapt global→local 认知流、练习阶梯、深度档（8–12/3–5）；reject Jupyter 脚手架 + mock 验证 + 交互式 HTML（与安全边界#1"不运行目标代码"冲突）；invent 三思维清单教学法、小白分档、review/性能思维教学、与模式A 共享引擎。
- **教学纪律**：三清单是提问引导不是灌输；练习只给提示与验收，答案由用户在自己 IDE 产出（防 AI 代答）；鲜活例子是引用（file:line+SHA）不是执行。
- **门禁配套**：trigger_cases 新增第 8 概念组 learning_action + 10 例（58 例全过；分母已封顶 min(5,max(3,n)) 不受组数影响）；validate_skill.py 加 模式E 标记/`- id: learn` token/场景 E 覆盖；scenario_matrix + EVALUATION_PLAN 增 E 双场景（小白路径 + 三清单证据断言）；manifest v3.1.0 + context_budget_bytes 25000（可略超决策写入 SKILL.md 资源预算段与本文档）。

## 3. 对抗式审查（对 v3.1.0 成品）

1. **"E 是 A 换皮"** → 验收硬指标：LEARNING_PATH.md 必含"30 分钟第一课"（教学化断言）+ 三清单每条绑 file:line；A 的报告结构不满足。
2. **"小白还是看不懂"** → E0 确认水平 + 每阶段生词表 + 前置清单带"去哪补" + 鲜活例子真实代码走读。
3. **"三清单空话"** → 每条强制证据；P7 复核增加该项。
4. **"练习代答"** → 只给提示 + 验收；反馈限"会不会破坏 X"式校验。
5. **"E/A 触发混淆"** → learning_action 组精确词组（避开裸"学习"防误伤既有"值得学习的开源项目"近邻例）+ E0 产出偏好询问 + E7 尾部切 A 入口。
6. **"预算超限失控"** → 允许略超 25K 但正文仍保持骨架自足（当前 20,9xx B，余量充足），超限内容优先下沉 references。

## 4. 墨菲清单（模式E 专属）

地址缺失先问不猜 / 链接失效转本地路径 / 术语淹没用生词表 / AI 代答输出审查 / 超大项目先学核心 30% / 三清单空泛绑证据——全部落入 learning-plan.md 失败模式表与 SKILL.md 速查表。

## 5. 门禁结果（本地开发副本）

- 打包版 validate_skill.py 0 错误（v3.1.0）；evaluate_triggers.py 58/58；validate_run fixtures 0+2。
- qiaomu validate：无预算警告（20,9xx < 25,000）；仅剩已知本地 aif-handoff 嵌套失败 + 2 条既有 argparse 警告（非本次引入）。
- SKILL.md 预算：见终检；manifest context_budget_bytes 25000（可略超）。
- missing evidence：宿主自动触发、模式E 面向真实小白的端到端学习效果、登录墙平台召回率。

## 6. 发布边界

本地开发副本未 push。按用户惯例：本地测试满意后自行推送（远程 `hoshinohatsuka/project-relay-Skill`，建议 v3.1.0 打 tag + Release）。