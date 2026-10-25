# codex 上下文压缩机制拆解要点（源码级）

> 目标：openai/codex@`970111f6cb`（本地只读克隆 `H:\...\Skills\codex\codex`）· 拆解日期 2026-10-25。
> 证据等级：**validated**——全部结论绑定本地源码 file:line；完整报告与 13 条证据账本见 `../../codex/拆解结果/`（TEARDOWN_REPORT.md + 黑板三件，validate_run 通过）。
> 本文件是面向 v4.1.0 借鉴的要点提炼，非全文报告。

## 一句话

codex 把压缩实现为**一次 AI→AI 交棒**：新上下文 = 重注入的初始上下文 + **原文保留的用户消息**（倒序 20K 预算）+ **垫底的一份交接摘要**（四要点）；助手消息与工具调用全部丢弃，由摘要承载。

## 机制要点（证据 file:line）

### 压缩即交棒
- 摘要提示词（`codex-rs/prompts/templates/compact/prompt.md:1-9`）：*"You are performing a CONTEXT CHECKPOINT COMPACTION. Create a handoff summary for another LLM that will resume the task."* 四要点：①Current progress and key decisions made ②Important context, constraints, or user preferences ③What remains to be done (clear next steps) ④Any critical data, examples, or references needed to continue。
- 接手者前置语（`summary_prefix.md:1`）：*"Another language model started to solve this problem… Use this to build on the work that has already been done and avoid duplicating work."*
- 摘要指令可被用户**整体覆盖**（`config.compact_prompt`，`core/src/compact.rs:125-130`、`tasks/compact.rs:83-92`）。

### 保留算法（`core/src/compact.rs`）
- 用户消息预算 `COMPACT_USER_MESSAGE_MAX_TOKENS = 20_000`（L63）。
- `build_compacted_history_with_limit`（L710-814）：**倒序**（`.rev()` L719）塞预算；放得下→**原文整条保留**；放不下→截断并标 `retained_sources_incomplete`（L785-789）；预算耗尽即停。
- 旧摘要识别排除（`is_summary_message` L617-619，`SUMMARY_PREFIX` 前缀）——**防递归摘要**。
- 初始上下文（AGENTS.md 等规范注入物）重新生成注入，插在"最后一条真实用户消息"之前，**摘要永远垫底**（L646-695）。
- 摘要作为 `CompactionSummary` 用户消息追加最末（L809-811）；空摘要写 "(no summary available)"（L803-807）。

### 触发（三相位 + 双口径）
- pre-turn：新输入**记录前**触发，失败保留输入（`session/turn.rs:201-210`）。
- mid/post-turn：按 `needs_follow_up` 分相（`turn.rs:625-634`）。
- 阈值：满窗 × `effective_context_window_percent`（默认 **95%**，`protocol/src/openai_models.rs:1129`）+ 缓冲；scope 可选 `Total` 或 `BodyAfterPrefix`（初始前缀不计入，`session/context_window.rs:61-81`）。

### 失败恢复
- 压缩请求自身超窗 → `remove_first_item()` 从头删重试；注释明言"保缓存前缀、保最近消息"（`compact.rs:358-370`）。
- 模型切换兼容：`compaction_model_hash` 记录摘要生成模型，哈希变化触发再压缩（`compact.rs:431`、`compact_model_fallback.rs`）。
- pre/post compact hooks 可中止（`compact.rs:197-237`）。

### 三种实现同一生命周期
本地 Responses（流式生成摘要）/ 远程 V2 / **TokenBudget 硬重置**（跳过摘要直接开新窗，但仍走同一 hooks 与 `ContextCompaction` 事件——"modeled as compaction"，`compact_token_budget.rs:16-40`）。手动 `/compact` 按 provider 能力路由（`tasks/compact.rs:63-95`）。

### 可观测与窗口编号
全字段遥测（前后 token/耗时/策略 Memento，`compact.rs:444-536`）；`advance_auto_compact_window` 窗口编号记录"第几代压缩上下文"（L412）。

## 与 Claude Code 对比（一句话版）

codex 更简单直接（单层摘要 + 用户消息原文保留 20K），Claude Code 更层层设防（微压缩→SM→传统→PTL 四层、9 段固定结构、断路器、水位线三档）。**共同底座**：压缩产物=交接书；用户意图原文优先；新信息优先；防递归；结构化分段。完整对比表见拆解报告。

## 对 project-relay 的直接启示

- **J1 支点**：压缩=交棒 ⇒ 模式C 产「当前会话上下文.md」不是外加物，而是把压缩机制"会话上下文固化"的本质补进交棒协议。
- **J2**：用户消息原文保留 ⇒ ①段 verbatim 全录（保最近删最旧）。
- **J4**：接手者前置语 ⇒ 文件头部定位句。
- **J10**：`compact_prompt` 可覆盖 ⇒ C0 问用户"特别嘱咐"。
- **J5**：防递归 ⇒ 固定文件名 + OWNERSHIP REVISION 同步。
