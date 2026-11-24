---
description: "LLM Wiki lifecycle: Ingest, Query, Lint operations and six query templates beyond Q&A"
描述: "LLM Wiki 生命周期：Ingest/Query/Lint 三操作与六类查询模板"
name: "LLM Wiki Lifecycle"
名称: "LLM Wiki 生命周期"
---

# LLM Wiki 生命周期

LLM Wiki 通过三个核心操作持续演进——Ingest（摄入）、Query（查询）、Lint（健康检查）。它们共同实现"知识复利"。

## Ingest（摄入）

新资料丢进 `raw/` 后，LLM Agent：

1. **Parse**：识别来源类型（本地文件、YouTube URL、HTTP 页面），抽取文本。
2. **Route**：读 schema 摘要 + 源文本，返回相关 slug 列表，把工作限定在相关页面。
3. **Synthesize**：对每个相关 slug，拿现有页面 + 新源重写页面，遵守 **"keep and expand" 不变量**——保留既有信息并扩展，不丢失旧知识。
4. **Embed**（可选）：用 text-embedding-3-small 重嵌更新页，就地更新索引。
5. **更新 index.md 与 log.md**：重建索引，日志追加一条带时间戳的记录（哪些 slug 被触碰、哪个源触发）。

关键：**一篇新文章可能触发 10–15 个页面的连锁更新**——这正是人类放弃维护 Wiki 的苦差事（更新交叉引用太繁琐），而 LLM 不会厌烦、不会忘记。

## Query（查询）

- 问题**指向 Wiki，而非原始素材**；答案从已编译、已互链的页面综合而来，并附来源引用。
- 若实现里用嵌入，则把问题用同一模型嵌入，在 Wiki 页索引上做余弦相似度检索 top-k，加载整页正文组装上下文。
- 好答案可通过 `--save` 归档成新 Wiki 页（slug 由问题派生）——知识进一步复利。

## Lint（健康检查）

定期审计 Wiki 结构：孤儿页、缺失页、断裂的 `[[slug]]` 链接、过期嵌入、缺失的来源引用；`--deep` 模式让 LLM 检查页面间的**事实矛盾**。这是编译器模式里的"测试套件"——保证编译产物不会悄悄腐化。

## 六类查询模板（Beyond Q&A）

Wiki 不止能回答事实问题，还能支撑六类更高阶查询：

| 类型 | 示例 |
|---|---|
| 综合类 | "贯穿一切的核心洞见是什么？" |
| 找缺口 | "我 Wiki 里完全缺失的重要主题有哪些？" |
| 辩论类 | "我的来源之间最大的分歧是什么？" |
| 产出类 | 生成学习指南、FAQ、幻灯片大纲 |
| 健康类 | 一致性/完整性审计 |
| 个人应用类 | "基于我所知，我现在最可能犯的错是什么？" |

这些模板把 Wiki 从"问答库"变成"推理与创作的底座"。

## 为什么循环能持续

Ingest 让新知识复利累积，Query 让已编译的知识被直接消费（便宜且带引用），Lint 保证结构不腐化。三者配合，Wiki 才能长期可信——单有 Ingest 会累积错误，单有 Lint 没有新知，单有 Query 则无积累。

> 相关：三层架构见 `../architecture/`；适用场景与 RAG 对比见 `../practice/`；增量维护的通用思想见 `../../../agent/context/`。
