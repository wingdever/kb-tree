---
description: "LlamaIndex, LangChain, Haystack and RAGFlow selection"
描述: "RAG 框架与工具的选型指南"
name: "RAG Frameworks and Tools"
名称: "RAG 框架与工具"
---

# RAG 框架与工具

框架只在管道有真正的编排复杂度时才"挣得自己的位置"。单语料、单 provider 的简单问答，provider SDK + 向量客户端足够（<50 行）。

## 你真的需要框架吗

- **分支 1**：单语料、单 provider、直接问答 → 直接用 provider SDK（OpenAI embeddings + Qdrant/Chroma/pgvector）。
- **分支 2**：多源摄入、几十种文档格式、解析痛苦 → 框架值回票价。LlamaIndex readers 支持 160+ 格式；Haystack converters、RAGFlow 深度 PDF 解析省去数周自定义 loader。
- **分支 3**：Agentic、多步检索 → 用框架，否则你会糟糕地重造 LangGraph 且没有测试。条件路由、人在回路检查点、有状态多轮检索正是 LangGraph 1.0 的用武之地。

反例：Octomind 在生产跑了 LangChain 12 个月后于 2024 年移除，理由是抽象层让底层修改困难或不可能。provider SDK 已吸收了框架过去抽象的多数能力（原生工具调用、流式工具调用、提示缓存）。

## 开源框架对比（2026）

| 框架 | 最适合 | 许可 | 自托管 | 判断 |
|---|---|---|---|---|
| **LangChain / LangGraph** | 多步 agentic 管道 | MIT | 是 | 生产默认；有状态、可控、人在回路 |
| **LlamaIndex** | 文档密集摄入 | MIT | 是 | 开箱解析最强；160+ 连接器 |
| **Haystack** | 企业 NLP、EU 团队 | Apache-2.0 | 是 | 类型化管道最强；生产可审计 |
| **DSPy** | 大规模提示优化 | MIT | 是 | 研究级、曲线陡；用评估数据自动优化 prompt |
| **RAGFlow** | PDF/文档解析 | Apache-2.0 | 是 | 免费深度文档解析引擎（表格、公式、布局） |
| **Dify** | 低代码/无代码团队 | 修改版 Apache-2.0 | 是 | 最快原型、控制最少 |
| **txtai** | 轻量单文件应用 | Apache-2.0 | 是 | 最小依赖，单包约 30 行跑通 |
| **Semantic Kernel** | .NET / 微软生态 | MIT | 是 | C# 团队的答案 |

## 选型建议

- 文档密集问答 → LlamaIndex；扫描件/表格多 → 加 RAGFlow。
- Agentic 应用（检索是众多工具之一）→ LangChain/LangGraph。
- 需要自己拥有并调试的生产系统 → Haystack。
- 简单稳定范围的管道 → 150 行自写代码常是最佳选择。
- 无工程师的快速原型 → Dify。
- 不想管基础设施 → 托管服务（Bedrock Knowledge Bases、Vertex AI RAG Engine、Vectara、Ragie）。

## 配套组件

- **向量库**：Pinecone（托管）、Weaviate/Qdrant（开源）最常提及。
- **重排**：Cohere Rerank 被反复推荐为精度选择。
- **解析**：Unstructured.io。
- **评估**：RAGAS。

## 迁移现实

架构要允许分阶段演进：单库先跑通，再按查询复杂度换引擎，最后补排序与观测。迁移设计应从第一天就存在——稳定 ID、元数据版本化、摄入与检索解耦、查询层抽象。

> 注：排名来自厂商相邻的评测文章，承诺前先核对当前价格与特性。

## 参考资料

- LlamaIndex 文档：https://docs.llamaindex.ai/
- LangChain 文档：https://python.langchain.com/
