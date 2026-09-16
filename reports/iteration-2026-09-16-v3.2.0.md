# Iteration Report — project-relay v3.2.0（2026-09-16）

## 1. 本次迭代来源：模式D 借鉴计划落地（用户批准）

用户用模式D「借鉴计划」对 aif-handoff（[lee-to/aif-handoff](https://github.com/lee-to/aif-handoff)，290★/39fork/MIT/TypeScript 应用）做了双项目拆解，产出 `参考资料/项目接手Skill与handoff的借鉴计划/`（run-id `borrow-aif-handoff-20260916`，黑板校验通过）。用户随后拍板：**批准高价值 6 条（B1–B6），仅借鉴思想不抄代码**，SKILL.md 允许超 25,000 至 30,000 字节。

**锚定修正（本次拆解的重要发现）**：aif-handoff 是完整的 Autonomous Kanban + AI subagents 应用，不是 SKILL.md 技能。它对标的不是"技能本体"，而是模式B/C 背后的**问题域**（跨 AI 交接/任务生命周期/评审闭环）。因此借鉴方式是**把工程机制翻译成协议语言**（references/scripts），不是抄代码——正好落在模式D 的"仅理念"默认路径上。参考方 SHA `af9b2ee` 全部证据 L1/L2 记录在 evidence-ledger。

## 2. 六个借鉴点 → 落地改动映射

| 借鉴点 | 来源（aif-handoff af9b2ee） | 落地（本项目 v3.2.0） |
|---|---|---|
| B1 收敛感知自动评审门 | `packages/agent/src/reviewGate.ts:203-212`（closure_first：旧 blocker 清空但出现新 blocker → 人工）+ `autoReviewHandler.ts:76-80`（绝不静默放行） | SKILL.md P7/H7/E3 收敛门规则 + handoff-guide H7 + learning-plan E3 + templates 模板 7/13/19 + manifest release_gates `convergence_gate` |
| B2 结构化评审契约 | `packages/agent/src/reviewContract.ts:22-40, 78-87`（三固定小节 + sha1 finding id 去重 + 前次回喂） | templates 模板 7/19 三小节格式（Blocking/Advisories/Previous Findings）+ SKILL.md P7/H7/E3 引用 + handoff-guide 模板 13 七节 |
| B3 交接所有权版本号 | `packages/data/src/taskOwnership.ts:28-42`（expectedOwnershipRevision 乐观并发） | 模板 13 `OWNERSHIP REVISION` 字段 + handoff-guide H0/H2 冲突规则 + SKILL.md C4 + 公理 14 + 失败表"旧交接冒充最新" |
| B4 显式状态机 | `packages/shared/src/stateMachine.ts:31-34, 57-71`（拒绝码 + CLEAN_STATE_RESET） | `scripts/validate_run.py`：`TASK_TRANSITIONS` 转移表校验 + `check_task_transitions`（非法跃迁拒绝、末态必须等于当前 status）+ 回归 fixtures `valid-transition-run`/`invalid-transition-run` |
| B5 不可变审计补 actor/快照 | `packages/data/src/audit.ts:20-35`（actor/statusSnapshot/assigneesSnapshot） | `validate_run.py` `check_evidence_audit_fields`（可选 actor/status_snapshot/from_status/to_status）+ fixture 覆盖 |
| B6 运行时画像 | `packages/runtime/src/resolution.ts`（task→project→system→env 回退） | 模板 13 `RUNTIME PROFILE` 字段 + SKILL.md C4 + 公理 13 |

**借 vs 抄得到什么**：全部为**理念翻译**——参考方是数据库/TypeScript 实现，本研究把它变成协议字段、文档段落、stdlib 校验规则；零行参考方代码进入本项目。双 MIT 兼容（`check_license.py` exit 0），归因全部带来源 SHA+file:line。

## 3. 改动文件清单

- `SKILL.md`：version 3.2.0；P7/H7/E3 收敛门；H0/C4 版本号+画像；黑板协议 B4/B5 注释；预算 30,000；失败表 +3 行；upstream 归因补 aif-handoff。字节 24,906 ≤ 30,000。
- `scripts/validate_run.py`：+`TASK_TRANSITIONS`/`TRANSITION_DENIED_CODES`/`EVIDENCE_AUDIT_FIELDS`；+`check_task_transitions`；+`check_evidence_audit_fields`。
- `evals/fixtures/valid-transition-run/`、`evals/fixtures/invalid-transition-run/`（新回归正反例）。
- `evals/EVALUATION_PLAN.md`：确定性基线 +2 条 validate_run 命令。
- `references/templates.md`：模板 13 + 版本号/画像/七节评审收敛记录；模板 7 + 结构化/收敛门；新增模板 19 评审收敛记录格式。
- `references/handoff-guide.md`：H0/H2 版本号冲突；H7 结构化契约+收敛门。
- `references/learning-plan.md`：E3 结构化输出+收敛门。
- `references/relay-principles.md`：公理 13/14/15；标题"十条思想"→"十五条思想"。
- `manifest.json`：v3.2.0、context_budget_bytes 30000、release_gates +convergence_gate + 状态机门禁说明。
- `agents/interface.yaml`：freeze/handoff 输出描述补新机制。
- `README.md`：模式B/C 描述、验证命令 +2、已验证/未验证、致谢。
- `reports/skill-ir.json`、`reports/trigger-eval.json`（58/58 重生成）。

## 4. 门禁结果（本地，全部可复现）

| 门禁 | 结果 |
|---|---|
| `validate_skill.py` | ok:true, errors:0, version 3.2.0 |
| `evaluate_triggers.py` | ok:true, 58/58（路由未动，借鉴点全在协议层） |
| `validate_run.py valid-standard-run` | exit 0（旧格式向后兼容） |
| `validate_run.py invalid-path-escape` | exit 2 |
| `validate_run.py valid-transition-run` | exit 0（转移链+审计字段合法） |
| `validate_run.py invalid-transition-run` | exit 2（非法跃迁 done→pending + actor 非字符串 + to_status 非法） |
| `validate_run.py` 模式D 本次 run 目录 | exit 0 |
| SKILL.md 字节 | 24,906 ≤ 30,000 |

## 5. 第一性原理 + 对抗式审查（对本次改动）

1. **收敛门会不会误伤正确完成的工作？**——收敛门只在"复核发现未清零"或"清零后出新阻塞"时触发人工交接。零发现时照常通过；它惩罚的是"假装收敛"，不惩罚真实完成。边界：小任务一次性通过不受影响（templates 模板 19 注明"小节齐才允许结论"）。
2. **状态机转移表是不是过度设计？**——用户方任务状态从 v2 就固定为 5 个枚举（pending/claimed/done/blocked/failed），`validate_run.py` 原先只查枚举合法性，拦不住"done 又变回 pending"这类错误。转移表仅 5 状态 × 每条白名单，是全枚举集内的显式化，不新增状态；字段可选，旧 run 目录不受影响（已验证向后兼容）。判定：**不过度**。
3. **OWNERSHIP REVISION 由谁保证递增？**——协议约束（模板 + H2 规则），脚本不做（文档是 Markdown 不是 JSON，无 machine 校验位）。诚实标注：版本号有效性最终靠离场 AI 遵守 + 接手 AI 的 H2 对比，属流程约束而非技术强制（与 H5 门禁同一诚实级别）。
4. **墨菲：加了可选字段会不会有人冒充"已审计"？**——字段是**可选**，校验只在存在时检查合法性；不宣称"所有 run 都有审计"。B5 的价值是"想要可重放审计时协议已支持"，不是"强制所有证据审计"。
5. **变更禁区遵守**：schema_version 未动（黑板协议兼容）；触发合同 58 例未动（路由零变化）；SKILL.md 未超 30,000；references 只增补不改删既有节。

## 6. 验收标准对照

- 触发评测全过（58/58）✅；validate 0 failures ✅；SKILL.md ≤30,000 ✅；密钥扫描（无新增密钥类内容，仅文档与 stdlib 脚本）✅
- 新回归 fixtures 正反例通过 ✅；旧 fixtures 向后兼容 ✅
- 本地 commit（不 push）——按用户发布门禁执行

## 7. 遗留与诚实验证边界

- **missing evidence**：收敛门在真实复核中的端到端效果（需真实会话验证）；版本号递增在长会话中的遵守率；审计字段在真实多 Agent run 中的使用率。这些是流程约束，脚本只保证"提供了机制"，不保证"模型必然遵守"。
- 参考方拆解报告与借鉴计划全文留在 `参考资料/项目接手Skill与handoff的借鉴计划/`（gitignore 隔离，不随包发布），后续用户可随时回查归因。