# Claude Code 上下文压缩机制笔记（AI-fundamentals 源）

> 来源：[ForceInjection/AI-fundamentals](https://github.com/ForceInjection/AI-fundamentals)（Apache-2.0）《Claude Code 上下文压缩机制深度解析》，路径 `08_agentic_system/context/claude-code-context-compression.md`，访问于 2026-10-25。
> 证据等级：**转述**——与 01 笔记（cc-notebook）独立成文但同源快照，两者数字互相印证（93% 自动压缩水位、20K 摘出预留、13K 缓冲、断路器 3 次、微压缩白名单），可视为中高置信转述。
> 用途：同 01；本篇独有贡献是"五层防御"框架与策略对比表。

## 1. 五层防御体系

- **L1** 上下文窗口限制（硬边界）
- **L2** 宏观压缩（主动 + 响应式）
- **L3** 缓存编辑微压缩（cache_edits，服务端定点清除）
- **L4** 时间触发微压缩（距上次交互 >60 min，缓存已过期 → 本地消息替换）
- **L5** 压缩后状态清理（`runPostCompactCleanup()` 重置 readFileState 与 UI 状态，防脏读）

## 2. 三档水位线（Opus 200K 例）

| 水位 | 比例 | token | 行为 |
|---|---|---|---|
| warn/err | ~82% | 147K | UI 提示 Context Low |
| autoCompact | ~93% | 167K | 触发主动压缩 |
| blocking | ~98% | 177K | 强制阻塞等用户手动处理 |

计算：`effectiveCW = CW − min(maxOut, 20K)`；自动阈值 = effectiveCW − 13K 缓冲。响应式：API 返回 413 Prompt-too-long 时被动触发（信息损失最高——直接丢弃最旧 API 轮次）。

## 3. 摘要与拼接

- Legacy Compact 引入 `compact_boundary`（压缩边界）消息；最终结构：**[历史摘要] + [压缩边界] + [近期最新消息]**。
- 格式化（`formatCompactSummary`）：删 `<analysis>` 草稿块，`<summary>` 换 "Summary:" 标题。
- 压缩指令强制保留："Key decisions, technical concepts and code patterns" 与完整代码片段；传统压缩最大输出 20K tokens。

## 4. 微压缩双路径

- L3 Cached MC：缓存有效时不改本地消息，`cache_edits` 让服务端清特定工具缓存（白名单 TOOLS_CLEARABLE_RESULTS：SHELL/GLOB/GREP/FILE_READ/WEB_FETCH/WEB_SEARCH）。
- L4 Time-Based MC：缓存过期后直接改本地消息，旧工具结果 → `[Old tool result content cleared]`。
- 每次请求前执行，<1ms，零 LLM 调用。

## 5. Session Memory（SM Compact）

- 零主线程 LLM 消耗：后台 Forked Agent 以 Markdown 持久化到 `.claude/memory`，仅授予记忆文件读写权限，双重阈值控制更新频率。
- 自动压缩路由：**SM Compact 优先 → Legacy Compact 降级**。
- `/compact` 是手动兜底入口，位于主动链路末端。

## 6. 新旧信息取舍原则

- 聚焦"接下来要做什么"，但强制保留关键决策与完整代码片段。
- **永不切断 tool_use/tool_result 配对；永不分离共享 message.id 的消息块**。
- 响应式压缩信息损失最高。

## 7. 其他机制（与交棒间接相关）

- 缓存边界隔离：`__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__` 切分静态规则与动态状态。
- 上下文折叠（读时重构历史组织形式，优化 Attention；93% 自动压缩会干扰它故有互斥）。
- 可观测性：`tengu_compact` / `tengu_cached_microcompact` / `tengu_time_based_microcompact` / `tengu_sm_compact` 埋点，阈值可环境变量或 GrowthBook 调整。

## 8. 策略对比表（原文要点）

| 属性 | Microcompact | Session Memory | Legacy | PTL Recovery |
|---|---|---|---|---|
| 调用 LLM | 否 | 是（后台隔离） | 是（Fork Agent） | 否 |
| 信息损失 | 最小 | 中等 | 中等 | 高 |
| 延迟 | <1ms | <10ms | 5~30s | ~0s |
| Cache | 保留 | 破坏 | 共享（Fork 继承） | 破坏 |
| 断路器 | 无 | 无 | 有（3 次） | 有（3 次） |

**设计哲学**：渐进式降级、缓存优先、安全配对保证、可观测可配置。

## 9. 对 project-relay 的直接启示

- 五层防御 = **渐进降级**的层次化表述，与 C4"骨架→明细"同构：能保多少保多少，最坏情况下骨架仍在。
- "永不切断配对"的协议层等价物：交接文档的"已完成明细"必须带"根因→修复→证据"三件套，拆开任何一件都让下一位无法复用（对应借鉴点 J11 决策完整性）。
- Session Memory 的 `.claude/memory` Markdown 持久化 → 「当前会话上下文.md」同为"磁盘上的会话记忆"，但定位是**单项目、交棒时点、面向接手者**。
