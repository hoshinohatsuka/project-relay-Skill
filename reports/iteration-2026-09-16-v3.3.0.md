# Iteration Report — project-relay v3.3.0（2026-09-16）

## 1. 本次迭代来源：模式D 借鉴计划中价值 4 条落地（用户批准）

承接 v3.2.0（高价值 B1–B6），用户本次批准中价值 4 条：**B7 预算冻结+恢复、B8 租约细化、B10 报告自查清单——实施到 Skill 本体**；**B9（MCP 双向同步）落点是用户主项目 Reverie（独立项目，非 Skill 本体），仅记录借鉴点，不在本版本实施**，待用户 Reverie 侧另行拍板。依旧**仅借鉴思想不抄代码**（参考方 lee-to/aif-handoff，SHA `af9b2ee`，双 MIT 兼容），SKILL.md 预算 30,000 内。

## 2. 三个借鉴点 → 落地改动映射

| 借鉴点 | 来源（aif-handoff af9b2ee） | 落地（本项目 v3.3.0） |
|---|---|---|
| B7 预算耗尽→自动冻结+恢复 | `packages/shared/src/runtimeLimitUtils.ts` + schema（runtime_limit_snapshot_json）+ docs "Runtime-Limit Snapshots and Auto-Pause"（blocked_external+retryAfter） | `references/multi-agent-handoff.md` §6 预算冻结流程（blocked + reason:"budget_exhausted" + retry_after ISO 时间 + checkpoint 记 blocked_external + 到点自动恢复）；`workflow-detail.md` §4 / `borrow-plan.md` D5 / `learning-plan.md` E5 三模式预算段统一引用；SKILL.md 资源预算段 + 失败表"预算耗尽"行；`validate_run.py` 新增 `retry_after` 校验（ISO 8601、仅限 blocked/failed、必须有 reason） |
| B8 租约细化：心跳+过期自动释放+优雅释放 | `packages/agent/src/coordinator.ts:1051-1055` + CHANGELOG（lease-based claiming：lockedBy/lockedUntil、heartbeat 续期、过期/死心跳释放、SIGINT/SIGTERM 优雅释放） | `references/multi-agent-handoff.md` §4 租约细则（claimed_until 到期时间 + heartbeat_at 心跳续租 + 过期/死心跳自动释放 + 会话结束显式释放）；SKILL.md 黑板协议段"租约纪律"；`validate_run.py` 新增 `claimed_until`/`heartbeat_at` 校验（ISO 8601）；fixtures 更新覆盖 |
| B10 每包 CHECKLIST 强制+"不适用要说明" | `CHECKLIST.md:1-8`（每包强制清单；不适用项在 PR/handoff 说明而非静默跳过；复发错误补入清单） | `references/templates.md`：模板 8（LEARNING_REPORT）加"报告自查清单"节（7 项）；模板 14（BORROWING_PLAN）加 7 项；模板 17（LEARNING_PATH）加 6 项；模板 13 C5 自查清单注明 B10 规则；新增模板 20"报告自查清单通则"（全模式产出报告必须带自查节，不适用项写明原因） |

**借 vs 抄**：全部为协议/文档/校验规则层面的理念翻译，零行参考方代码。B7 的 blocked_external→retry_after 是参考方状态机思想的映射，B8 的租约字段是对既有 claimed 单租约的显式化（未新增状态，只加可选时间字段）。

## 3. 改动文件清单

- `SKILL.md`：version 3.3.0；资源预算段补预算冻结规则；黑板协议段补租约纪律；失败表 +2 行；资源索引补模板 20；upstream 归因扩展。
- `scripts/validate_run.py`：`LEASE_FIELDS` 常量 + `check_lease_fields`（claimed_until/heartbeat_at/retry_after ISO 校验 + retry_after 状态/reason 绑定）。
- `references/multi-agent-handoff.md`：§4 租约细化、§6 预算冻结流程。
- `references/workflow-detail.md`：§4 资源预算与冻结（引用 multi-agent-handoff）。
- `references/borrow-plan.md`：D5 补预算冻结。
- `references/learning-plan.md`：E5 补预算冻结。
- `references/templates.md`：模板 8/13/14/17 自查清单节 + 模板 20 通则。
- `evals/fixtures/valid-transition-run`（+T-004 budget exhausted）+ `invalid-transition-run`（+T-003 bad iso + T-004 retry_after without reason）。
- `evals/EVALUATION_PLAN.md`：确定性基线说明更新。
- `manifest.json`：v3.3.0、release_gates +budget_freeze_gate、run_state_check 说明更新。
- `agents/interface.yaml`：safety 补 budget_freeze/lease_heartbeat。
- `README.md`：安全节补预算冻结；验证命令说明更新。
- `reports/skill-ir.json`（v3.3.0）、`reports/trigger-eval.json`（58/58 重生成）。

## 4. 门禁结果（本地，全部可复现）

| 门禁 | 结果 |
|---|---|
| `validate_skill.py` | ok:true, errors:0, version 3.3.0 |
| `evaluate_triggers.py` | ok:true, 58/58（路由未动） |
| `validate_run.py valid-standard-run` | exit 0（旧格式向后兼容） |
| `validate_run.py invalid-path-escape` | exit 2 |
| `validate_run.py valid-transition-run` | exit 0（含合法租约/预算冻结字段） |
| `validate_run.py invalid-transition-run` | exit 2（非法跃迁 + 坏 ISO 时间 + retry_after 无 reason） |
| SKILL.md 字节 | 25,827 ≤ 30,000 |

## 5. 第一性原理 + 对抗式审查

1. **B7 会不会过度设计？**——参考方的配额快照面向"provider 配额信号"，本研究落点是"预算项（社区查询/Agent 数/重试）耗尽"。预算耗尽在现实中确实发生过（社区查询超 12 次、深度档 Worker 超预算），之前只写"显式降档"，没有"冻结到恢复"的机制；冻结+retry_after 让恢复是计划内动作而非重新申请。判定：**合理**。边界：retry_after 的"到点恢复"依赖下次会话读取 checkpoint，属流程约束（与版本号同一诚实级别）。
2. **B8 字段会不会有人造假心跳？**——`heartbeat_at` 由 Agent 写、`claimed_until` 是承诺的到期时间；脚本只校验格式，不验证"这个 Agent 是否真的活着"。诚实标注：租约释放最终靠运行 Agent 遵守（写挂死心跳检查点），脚本提供的是**格式与存在性校验** + 协议纪律，不是进程级监督。参考方有进程级 heartbeat 实现，本研究是协议翻译——差异如实声明。
3. **B10 自查清单会不会变成模板表演？**——qiaomu 规范反对"仪式性目录"；自查清单的防御对象是"报告声称完成但实际偷懒"，清单项全部绑定可判据（file:line 在否、URL+日期在否、分母在否），不是主观自评。且"不适用项必须写明原因"本身防静默跳过。判定：**有判据、防表演**。
4. **墨菲：三处预算段（workflow-detail/borrow-plan/learning-plan）会不会口吻不一致？**——B7 采用"统一规则 + 三处引用"结构（multi-agent-handoff §6 为权威源，三处各一段并指向它），避免复制粘贴漂移。已检查三处措辞一致。
5. **变更禁区遵守**：schema_version 未动；触发合同 58 例未动；SKILL.md 25,827 ≤ 30,000；references 只增补。

## 6. 验收标准对照

- 触发评测全过（58/58）✅；validate 0 failures ✅；SKILL.md ≤30,000 ✅
- 新/旧 fixtures 全过，向后兼容 ✅
- 预算冻结、租约字段、自查清单三机制全部可复现验证 ✅
- 本地 commit（不 push）✅

## 7. 遗留与诚实验证边界

- **B9（MCP 双向同步）**：按借鉴计划落点指向用户主项目 Reverie（多模型接力工具链），不在 Skill 本体实施。本版本仅更新借鉴计划记录状态（BORROWING_PLAN.md §2 标"待 Reverie 拍板"）。若用户要在 Reverie 集成，需另行批准范围。
- **missing evidence**：预算冻结的"到点自动恢复"在真实跨会话续跑中的效果；租约过期释放的真实遵守率；自查清单对报告质量的实测提升——均为流程约束，脚本保证机制存在不保证模型必然遵守。