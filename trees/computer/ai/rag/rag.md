---
description: "Knowledge tree for retrieval-augmented generation engineering"
描述: "RAG 工程知识树导航"
name: "Retrieval-Augmented Generation"
名称: "检索增强生成"
---

# RAG 知识树

RAG（检索增强生成）让模型在查询时从自有数据中检索相关事实，而不是只依赖训练记忆。本目录把 RAG 工程拆成 14 个子知识点，每个自成一个目录、目录内放同名介绍 md。

## 子知识点目录

| 目录 | 内容 |
|---|---|
| `basics/` | 机制五步、为什么需要 RAG（vs 微调/大上下文）、生产流水线、工程原则、参考架构 |
| `chunking/` | 已展开为子树：basic、semantic、contextual、eval、special（入口 `chunking/chunking.md`） |
| `retrieval/` | 已展开为子树：recall、rerank、fusion（入口 `retrieval/retrieval.md`） |
| `query-transform/` | 查询变换：HyDE、多路查询、Step-back、分解、路由式改写 |
| `multimodal-rag/` | 多模态 RAG：视觉文档检索、ColPali 晚期交互、统一嵌入、Agentic Vision RAG |
| `embedding/` | 已展开为子树：models、training、matryoshka（入口 `embedding/embedding.md`） |
| `vdb/` | 已展开为子树：ann、products、filter、cost（入口 `vdb/vdb.md`） |
| `graphrag/` | 已展开为 6 个子知识点：graphdb、kg-construction、ontology、raptor、semantic-layer（含 text-to-sql 子树）、frameworks（入口 `graphrag/graphrag.md`） |
| `memory/` | 已展开子树：短期/长期记忆、记忆层级、状态检查点、记忆治理，以及 dsh 的 MCP memory 挂载（入口 `memory/memory.md`） |
| `agentic-rag/` | 已展开子树：patterns、self-correcting、retrieval-as-tool（入口 `agentic-rag/agentic-rag.md`） |
| `eval/` | RAG Triad、四层方案、RAGAS、Agentic RAG 评估难题 |
| `frameworks/` | LlamaIndex/LangChain/Haystack/RAGFlow 选型、迁移路径 |
| `prod/` | RBAC、索引新鲜度、延迟、成本、上线清单 |
| `llm-wiki/` | 已展开子树：architecture、lifecycle、practice（知识编译模式：Raw→Wiki→Schema） |
| `learning/` | RAG 学习资源：中文开源教程与出版书配套代码仓库 |

另有 `memory-rag/` 为导航页，指向拆分后的各目录。

## 建议阅读顺序

基础：`basics` → `chunking` → `embedding` → `vdb` → `retrieval` → `query-transform`（检索前后配合）。进阶：`graphrag` → `agentic-rag` → `memory` → `multimodal-rag`。保障：`eval` → `prod` → `frameworks`。替代路线：`llm-wiki`（不依赖向量检索的知识编译范式）。

## 一句话主线

从"检索而非记忆"的基础出发，把文档切好块（`chunking`）、选对嵌入与索引（`embedding`/`vdb`）、用混合检索与重排精排（`retrieval`），需要关系推理时上 `graphrag`、需要自主多跳时上 `agentic-rag`，用 `eval` 量化、用 `prod` 保障安全与成本，最后用 `frameworks` 落地。

若想要一条**非向量的替代路线**——把知识编译成持续维护、Git 版本控制的可读 Wiki，让查询从 Wiki 而非原始片段综合而来——见 `llm-wiki/`，它是 RAG 从解释器模式到编译器模式的演进。
