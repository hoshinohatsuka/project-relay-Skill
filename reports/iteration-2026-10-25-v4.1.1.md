# 迭代报告 v4.1.1：交接文档命名规范固定化（2026-10-25）

## 用户拍板（2026-10-25，查阅测试/两件套后）
原命名 `HANDOFF-<主题>-<日期>.md` 中"主题"段改为固定文字**「项目交接」**→ 新规范 **`HANDOFF-项目交接-<日期>.md`**；HANDOFF 前缀与日期段不变；"仅稍微更改这一部分，其他没有任何问题"。同轮拍板：commit 全部修改并 push 远程（已授权）；重装 ZCode + 新导入 OpenCode / DSH / Antigravity。

## 变更清单
| 文件 | 变更 |
|---|---|
| SKILL.md | C4 默认文件名 + 命名规范注记；frontmatter 4.1.1 |
| references/templates.md | 模板13 主件路径 + "文档内标题仍可写实际主题"注记 |
| agents/interface.yaml | freeze output 文件名 |
| readme-EN | L17 表格 + L34 Mode C 节（<topic>/<subject> → 项目交接） |
| 测试/ | HANDOFF-上下文压缩增强-2026-10-25.md 重命名为 HANDOFF-项目交接-2026-10-25.md；当前会话上下文.md 配套引用同步 |

不变：触发合同 58 例、validate_run、模板结构、模式B/C 语义；同日多次交棒同名覆盖的语义与配套件"永远最新"一致（用户已确认无其他问题）。历史文档（含 上下文压缩机制/05 对旧命名的历史描述）保持原文不改。

## 验证
validate_skill 0 failures（4.1.1）/ 触发 58/58 / validate_run 0-2-0-2 / SKILL.md 28,258B ≤30,000 / grep 残留：活文档无 `HANDOFF-<主题>`（历史 reports 保留原文）。
