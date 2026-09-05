# 产出模板

所有报告中文书写；代码、路径、标识符保持原文。占位符 `<>` 需替换。

## 0. 黑板状态文件（跨时段/跨 Agent 协作必需）

**run-manifest.json**
```json
{
  "schema_version": "2.0",
  "skill_version": "2.0.0",
  "run_id": "last30days-20260905",
  "mode": "teardown",
  "target": {"repo": "https://github.com/owner/repo", "commit_sha": "<HEAD sha>", "default_branch": "main"},
  "tier": "standard",
  "status": "in_progress",
  "budget": {"community_queries_used": 5, "workers": 3},
  "updated_at": "2026-09-05T12:00:00+08:00"
}
```

**task-ledger.json**
```json
{"tasks": [
  {"id": "T-001", "title": "模块组A深读", "role": "module-worker",
   "status": "done", "input_scope": "src/auth/**", "output_path": "artifacts/T-001/findings.md"},
  {"id": "T-002", "title": "知乎调研", "role": "community-worker",
   "status": "blocked", "input_scope": "zhihu", "reason": "登录墙 missing evidence"}
]}
```

**evidence-ledger.jsonl**（每行一条）
```json
{"id": "E-001", "kind": "code", "ref": "src/main.py:8", "level": "L1", "confidence": "high", "note": "FastAPI 实例化"}
{"id": "E-101", "kind": "community", "ref": "https://...", "query": "...", "accessed": "2026-09-05", "source_type": "firsthand", "verdict": "..."}
```

**checkpoint 文件（checkpoints/CP-<n>.json）**
```json
{"n": 3, "stage": "P4-module-deep-read", "checksum": "<sha256 of ledger files>", "next": "P7 对抗复核", "ok": true}
```

## 1. 提示词翻译文档 `notes/05-prompts/<功能>_prompt_zh.md`

```markdown
# <功能描述>（提示词翻译）
## 元信息
- 来源：<repo>/path/to/file.py:L12-L48（commit <sha>）
- 变量名：<SYSTEM_PROMPT> / 动态构建函数 <_build_prompt>
- 所属模块：<模块名> · 触发场景：<何时被调用>
## 中文翻译
<逐段翻译；保留 JSON/Markdown/代码块结构与 {variable} 占位符>
## 关键参数
- `{variable}`：<含义与可能的取值>
## 代码上下文
<调用链：谁组装它、传给哪个 API、失败时的回退>
```

## 2. 提示词索引 `notes/05-prompts/INDEX.md`
表：序号/文档/原文件/功能描述 + 四路扫描覆盖说明（各路命中数 + 未检查范围）。

## 3. 基线测绘 `notes/02-baseline.md`
一句话定位；上游框架与运行时 / 脚手架来源 / 参考项目 / 自研核心四层（每层带证据）；核心代码地图（入口→主流程→数据→对外接口）。

## 4. 需求→模块映射 `notes/03-requirement-module-map.md`

```markdown
模块计数口径：<判定规则一句话>
| 需求 | 模块数 | 模块（职责） | 关键文件 | 备注 |
|---|---|---|---|---|
| R1 用户登录 | 3 | 路由、会话、存储 | a/b.py:12, c.ts:40 | 依赖外部 IdP |
```
表尾附"文档宣称但未找到实现"（`[待确认]`）。

## 5. 模块矩阵 `notes/04-module-matrix.md`
三段：选型矩阵（模块/选型/版本/理由+**证据级别 L1-L4**/替代品/权衡）、解耦评估清单（每项 ✔/✖/部分+证据）、性能审计清单（症状→证据→影响→修法；区分静态风险/可验证假设/真实 benchmark）。

## 6. 社区调研 `notes/06-community.md`
按平台分节；每条：`[类型] 结论 — 平台，URL，访问日期，来源类型，可访问状态`；末尾 `missing evidence` 清单。

## 7. P7 对抗复核清单 `notes/07-review.md`
逐项勾选：□需求无漏映射 □模块无重复计数（口径一致） □选型理由非纯 L4 冒充 □社区说法已对代码反证 □性能建议有证据 □学习路径可执行 □覆盖率有分母 □无未标注的推测。发现问题 → 回对应阶段修补。

## 8. 最终报告 `LEARNING_REPORT.md`

```markdown
# <项目名> 拆解学习报告
> 档位：<x> · 覆盖率：<y>%（分母=<候选模块集代码行>）· 日期 <date> · commit <sha> · 未分析范围：<...>

## TL;DR（3–5 条）
## 1. 项目概述
## 2. 数据流分析（Mermaid sequenceDiagram）
## 3. 基准源码参考（四层）
## 4. 需求→模块映射（含计数口径）
## 5. 模块选型矩阵（含证据级别）
## 6. 解耦与性能评估（区分静态风险与 benchmark）
## 7. 提示词与 Agent 设计（条件：仅 LLM 项目）
## 8. 社区口碑与踩坑（含来源分歧与 missing evidence）
## 9. 学习路径（阅读顺序/复刻练习/可迁移清单）
## 10. P7 复核记录与关键分歧
---
本报告由 AI 生成，仅供学习参考，结论请独立验证。源项目：<URL>（License: <...>）
```

## 9. 五类复述（模式B H1 产出）

```markdown
1. 我确定知道的事情（每条附 file:line）
2. 我高度推测的事情（每条附依据）
3. 我不知道的事情
4. 我怀疑前任理解有误的事情（只列疑点，不下结论）
5. 我准备验证的事情（每条附验证方法）
```

## 10. 假设登记表 `.ai/ASSUMPTIONS.md`

```markdown
| ID | 假设 | 证据 | 置信度 | 验证方式 | 状态 |
|---|---|---|---|---|---|
| A-001 | <...> | <file:line / 文档> | 高/中/低 | <跑什么测试/读什么> | 待验证/已证实/已证伪 |
```
证伪时：修正 PROJECT_STATE 相关结论，checkpoint 注明。

## 11. RTM 追踪矩阵 `.ai/TEST_PLAN.md` 内

```markdown
| 需求 | 能力 | 模块 | 文件 | 测试 | 验收条件 | 状态 |
|---|---|---|---|---|---|---|
| R001 | 注册 | AUTH-01..03 | src/auth/* | TEST-AUTH-001.. | 注册成功率 100% | ✅ |
```

## 12. 交接包（模式B，写入 `.ai/`；微型项目可合并为单文件 HANDOFF.md）

- **PROJECT_STATE.md**：基线 commit/分支/当前状态/已知 BUG（BUG-001 格式）/测试覆盖率
- **REQUIREMENTS.md**：R001…+验收标准
- **ARCHITECTURE.md**：组成与依赖方向 + 核心代码地图
- **DECISIONS.md**：决策 + 理由 + **变更禁区清单**
- **TODO.md**：执行单元 + 顺序 + 所属 Vertical Slice
- **TEST_PLAN.md**：RTM（模板 11）
- **HANDOFF.md**（硬格式，在途状态）：

```markdown
PROJECT: <名称>
BASELINE COMMIT: <sha>
CURRENT BRANCH: <分支>
CURRENT STATUS: <已完成/未完成/覆盖率>
KNOWN BUGS: BUG-001 ...
DO NOT CHANGE: <禁区清单>
NEXT OBJECTIVES: 1. ... 2. ...
SUCCESS CONDITIONS: <可执行命令与判据，如 npm run build 通过、pytest 通过>
ARCHITECTURAL CONSTRAINTS: <技术栈约束>
KNOWN ASSUMPTIONS: A-001...
OPEN QUESTIONS: Q-001...
```

- **checkpoints.md**：`CP-<n> | 时间 | 需求 ID | 做了什么 | 测试结果 | commit SHA | 下一单元`

工作落地并验收后：HANDOFF.md 归档至 `.ai/archive/`，常驻四件（STATE/REQUIREMENTS/ARCHITECTURE/DECISIONS）继续维护。

## 13. 模式C 交接文档（离场 AI 交棒用）

写入 `<项目>/.ai/handoffs/HANDOFF-<主题>-<日期>.md`。**最小骨架规则**：额度紧张时按"骨架 → 明细"两段落盘，写完骨架（头部/红线/状态表/下一步）就算有效合约，明细可以后补。

```markdown
# 交接文档：<主题>（<日期>）

> 写给下一个接手的 Agent。<前情一句话：上一轮会话做了什么、处在什么模式>。
> <未提交警告：代码全部在工作区未提交 / 已 commit 至 <sha>；相应地告诉接手者该做什么>。
> 本文档是**意图与状态**的权威记录；**事实以代码为准**（冲突时按真相层级仲裁）。
> TL;DR (EN): <one-sentence English summary of state + next step, so any agent can onboard>

## 〇、红线（必须遵守，违反即事故）
1. <工作目录绝对路径（下称缩写）>。
2. <只读区/禁写区，逐条给绝对路径>。
3. <绝不泄漏：密钥文件、.env、凭据（只写文件名，绝不写值）>。
4. <环境怪癖：用哪个 python/解释器、哪个 shell、命令的转义坑>。
5. <来之不易的纪律：如"outcome 未知时禁止自动重试""不要主动 commit">。

## 一、本次会话范围 + 状态表
| # | 任务 | 状态 |
|---|------|------|
| 1 | <任务> | ✅ 完成 / ⬜ 未开始 / ⚠️ 部分 |
<计划全文出处（如曾存于某 plan 文件）>

## 二、已完成明细（根因 → 修复 → 证据）
### <任务名>（✅，<测试结果 N/N>）
**根因**：<为什么坏，不许只写"改了什么">
**修复**：<文件:行号 + 关键决策；用户拍板的标"用户已定">
**验证**：<测试数字/命令输出摘要>；<未验证的写"凭记忆，未验证">

## 三、待办批次（按此顺序执行）
### <下一项>（<优先级>）
位置：<file:line>；方案：<已定方案或"未定，需先调研">；
验收：<可判据命令与期望>；坑：<已探明的失败方式与兜底>。

## 四、关键架构事实（防下一个 Agent 重探）
<非显而易见的不变量、白名单/生成器联动、"某某文件决定了某某行为"这类花大力气才发现的事实>

## 五、测试基线（交接时刻）
<各测试套件的精确数字：vitest x/x、pytest x/x、tsc 是否全绿；未跑的套件如实写"未跑">

## 六、下一步的第一件事
**<唯一的第一步>**，然后 <后续顺序>。不要：<清单>。

## 附：无技能接手协议（任何 AI 均可照此接手）
1. 先独立侦察项目（不读本文先扫代码），写出五类复述：确定/推测/不知道/怀疑本文有误/待验证。
2. 再读本文，逐条对比；冲突按真相层级裁决：运行结果 > 源码 > 需求/验收 > 架构决策 > 本文 > 你的推测。
3. 本文"红线"默认绑定；与代码事实冲突时停下问用户。
4. 未验证的推测一律记入假设登记表，不许伪装成事实。
5. 每完成一步：跑测试 → 更新状态 → git checkpoint。
```

**自查清单（C5 用）**：□红线置顶且逐条具体 □状态表与磁盘证据一致 □已完成带证据等级 □测试基线是重跑数字 □下一步无歧义 □无技能附录在 □未提交清单在 □旧文档已归档、指针已更新。
