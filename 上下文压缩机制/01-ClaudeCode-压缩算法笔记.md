# Claude Code 上下文压缩算法笔记（cc-notebook 源）

> 来源：[win4r/cc-notebook](https://github.com/win4r/cc-notebook) 《Claude_Code上下文压缩算法深度分析.md》，访问于 2026-10-25。
> 证据等级：**转述**——该文是对 Claude Code 2026-03-31 前后源码快照（`src/services/compact/` 11 文件）的逆向分析，非官方文档；关键数字与结构以本文为准引用，落地设计时逐条标注。
> 用途：project-relay 模式C「当前会话上下文.md」的设计参考。

## 1. 四层递进压缩体系

1. **微压缩 Microcompact**：规则清理旧工具输出，<1ms，不调 LLM。
2. **自动压缩 Auto-Compact**：阈值触发；优先 Session Memory，否则传统压缩。
3. **传统压缩 Full Compact**：Fork Agent 生成摘要，5–30s。
4. **Session Memory 压缩**：复用后台已沉淀的记忆，<10ms。

设计原则：**用廉价的规则操作延迟昂贵的 LLM 调用，只在不得已时丢弃信息**。

## 2. 触发阈值（关键数字）

- `MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000`：给摘要输出预留的额度。
- 有效上下文窗口 = 模型窗口 − min(模型最大输出, 20K)。
- `AUTOCOMPACT_BUFFER_TOKENS = 13_000`：阈值 = 有效窗口 − 13K。例：Opus 200K → 200,000 − 20,000 − 13,000 = **167,000 tokens**（≈93% 水位）。
- 警告/错误阈值各再缓冲 20K；手动 /compact 阻塞限制 3K。
- **断路器**：连续失败 ≥3 次跳过自动压缩（据 BQ 数据曾有会话连败 3,272 次、日浪费约 25 万次 API 调用——断路器是对"自动重试失控"的防线）。
- `shouldAutoCompact` 决策树拒绝项：session_memory/compact 来源（防递归）、上下文折叠代理、配置关闭、响应式压缩模式、折叠模式（"自动压缩在 93% 会干扰折叠"）、最后才判 token 差值。

## 3. 九段式摘要结构（对模式C 最有直接参考价值）

1. **Primary Request and Intent** — 用户全部请求与意图
2. **Key Technical Concepts** — 关键技术概念
3. **Files and Code Sections** — 文件、重要性原因、代码片段
4. **Errors and fixes** — 错误、修复方式、用户反馈
5. **Problem Solving** — 问题解决过程
6. **All user messages** — 逐条列出非工具结果的用户消息
7. **Pending Tasks** — 待办
8. **Current Work** — 当前工作，含文件名与代码片段
9. **Optional Next Step** — 下一步计划，**"包含最近对话的直接引用"**

外层格式：`<analysis>`（思考草稿，最终删除）+ `<summary>`（保留部分）。

## 4. 微压缩细节

- 白名单工具：Read、Bash、Grep、Glob、WebSearch、WebFetch、Edit、Write。
- 子路径 A（时间触发）：缓存过期时保留最近 N 个结果，旧 tool_result 替换为 "[Old tool result content cleared]"，不改 tool_use。
- 子路径 B（缓存编辑）：不改本地消息，通过 `cache_edits` API 块让服务端定点删缓存，保护 Prompt Cache 命中率；`pendingCacheEdits/pinnedCacheEdits` 管理，成功后 `pinCacheEdits()` 固定。
- Token 估算：字符数/4；图片/文档固定 2000；总和 ×4/3 保守填充。

## 5. 传统压缩（Fork Agent）

- Fork Agent 分支当前会话生成摘要，**共享主会话的 prompt cache**。
- 预处理管线：stripImages → stripReinjectedAttachments → normalizeMessagesForAPI。
- 强力前导词禁止工具调用（自适应思考模型可能调工具导致 maxTurns:1 下无输出）。
- 后处理：删 `<analysis>`、`<summary>` 换 "Summary:" 标题、压缩空行。
- **部分压缩两个方向**：`from`（摘要最近消息）与 `up_to`（摘要旧消息、保留新消息，摘要含第 9 章 "Context for Continuing Work"）。

## 6. 保留与重注入

- Session Memory：**最少保留 10K tokens 且 ≥5 条含文本消息，最多 40K**。
- 压缩后重注入：最近读取文件前 5 个、每个 ≤5K、总预算 50K；外加 Plan 文件、MCP/技能/代理列表增量。
- PTL 重试（压缩请求自身超限）：可解析缺口则按 API 轮次精确删除；否则删最旧 20% 的组，最多重试 3 次，保证至少留 1 组。

## 7. 压缩后上下文重建的消息序列

CompactBoundaryMessage（含 token 统计、触发类型）→ 摘要用户消息 → 保留的最近消息 → 重注入附件 → Hook 结果。摘要消息带 transcript 回溯路径、"直接继续不要打招呼"指令（Resume directly — do not acknowledge the summary）、自主模式继续工作循环指令。

## 8. 关键算法

- `groupMessagesByApiRound`：按 assistant `message.id` 变化分组（同轮流式块共享 id）。
- `calculateMessagesToKeepIndex`：从 lastSummarizedIndex+1 向前扩展，直到满足 min 双条件或触顶 40K 或碰旧 CompactBoundary。
- `adjustIndexToPreserveAPIInvariants`：不切断 tool_use/tool_result 配对、不分离同 message.id 的 thinking 块（孤儿 tool_result 真实 bug 场景）。
- 混合 token 计数：优先 API usage 精确值，回退估算。

## 9. 对 project-relay 的直接启示（落地见 05 计划）

- 9 段结构 → 「当前会话上下文.md」分段骨架（交棒场景调整段序与内容）。
- "All user messages" 逐条 + 第 9 段"最近对话直接引用" → 用户原话不失真。
- 断路器/防递归/边界消息 → OWNERSHIP REVISION 同步机制（已有，互证）。
- 微压缩"旧输出替换为占位符" → "引文而非全文"规则（file:line 代替贴大段输出）。
