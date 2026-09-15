# 社区调研策略与引用规范（P6）

目标：回答"社区怎么评价这个项目、别人踩过什么坑、有哪些值得学的讨论"。铁律：**无引用不结论**。

## 1. 平台优先级与预算

| 优先级 | 平台 | 检索方式 | 说明 |
|---|---|---|---|
| P0（必做） | GitHub 本仓 | issues / discussions / releases / README 评论区 | 用 `site:github.com/<owner>/<repo>` 或仓库页直接读；按 👍 排序看 top 问题 |
| P1 | Stack Overflow | WebSearch `"<project>" site:stackoverflow.com` | 用法问题与坑 |
| P1 | HuggingFace | WebSearch + 站内搜 models/papers/spaces | ML/LLM 项目优先 |
| P2 | X/Twitter | WebSearch `"<project>" twitter` 或 `site:x.com` | 一手反馈与作者动态 |
| P2 | YouTube | WebSearch `"<project>" tutorial review site:youtube.com` | 入门演示与实测 |
| P3（尽力而为） | 知乎 | WebSearch `"<项目名>" site:zhihu.com` | 中文深度解读 |
| P3 | 小红书 | WebSearch `"<项目名>" 小红书` | 中文上手体验，注意营销噪音 |
| P3 | Facebook / LinkedIn | WebSearch 限定站点 | 多为团队动态，价值密度低，快速扫过即可 |

预算（WebSearch/抓取调用合计）：快速 ≤4、标准 ≤12、深度 ≤24。先 P0/P1 后 P2/P3，预算耗尽即收尾并在报告中声明覆盖了哪些平台。

## 2. 查询模板

- 口碑：`<project> review` / `<project> 值得学吗` / `<project> 踩坑`
- 对比：`<project> vs <竞品>`（竞品从 P2/P4 得出）
- 教程：`<project> tutorial 2026` / `<project> 入门`
- 事故与坑：`<project> breaking change`、`<project> issue <报错关键词>`
- 作者生态：`<author> project`、`<project> roadmap`

每个平台用 1–2 条最贴的模板，不要刷屏式搜索。

## 3. 记录规范（`notes/06-community.md` + evidence-ledger.jsonl）

每条发现一行记录，字段齐全（缺失字段如实标注）：

```markdown
- [口碑|坑|教程|对比] 结论一句话（事实/观点要区分） — 平台，URL，访问日期 2026-09-05，作者/频道，发布时间，来源类型（官方|一手用户|媒体|SEO），可访问状态
```

同时写入 evidence-ledger.jsonl：`{"id":"E-101","kind":"community","ref":"https://...","query":"last30days review","accessed":"2026-09-05","source_type":"firsthand","verdict":"..."}`。

- **搜索摘要只作线索不作结论**：引用前必须点开原文核过；点不开就记"摘要级证据"，降权标注。
- 事实（"v2.0 改了配置格式"）需可复现；观点（"太难用了"）注明是个别用户还是普遍说法。
- 日期过旧（>2 年）的教程标注"可能过时"。
- 星标数/点赞数只说明热度，不说明质量，不得当结论引用。
- 平台不可达/无结果/登录墙：写 `missing evidence: <平台>`，只记失败，不用缓存摘要或想象冒充正文。
- 知乎/小红书命中营销软文特征（堆副标题、无技术细节、留联系方式）时降权或弃用。
- 同名项目混淆：核对 owner/repo 与上下文，不匹配的排除并记录。

## 4. 与代码证据冲突时

P7 交叉验证规则：代码为准，社区说法作为"作者/用户宣称"记录，分歧显式写入报告。典型冲突：README 宣称的性能 vs 代码里的同步阻塞实现。

## 5. 模式D 借鉴场景查询模板

借鉴计划（模式D）中，P6 九平台与预算规范不变，查询目标从"评价这个项目"扩展为"我要从它那里借鉴什么、有什么坑"：

- 坑与最佳实践：`<参考项目> 借鉴 踩坑` / `<参考项目> best practices` / `<框架> migration pitfalls`
- 迁移与兼容：`<框架/库> upgrade experience` / `<参考项目> vs <用户项目所用框架>`（竞品与迁移对照）
- 版权与许可证讨论：`<参考项目> license 争议` / `<参考项目> copying code`（社区对版权/许可证的讨论仅作线索，事实以 LICENSE 文件与 check_license.py 结构结果为准）
- 作者生态：`<参考项目> roadmap`（判断该设计是否还会演进、是否值得借鉴）

每条仍按第 3 节记录规范（查询/URL/日期/来源类型/可访问状态/结论）；搜索摘要不作结论；登录墙记 missing evidence。社区说"值得抄"与代码反证冲突时按第 4 节以代码为准。
