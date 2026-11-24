---
description: "Navigation page for memory and RAG topics"
描述: "记忆与 RAG 主题的导航页"
name: "Memory and RAG"
名称: "记忆与 RAG"
---

# 记忆与 RAG

本页汇总记忆与 RAG 相关知识点目录的入口。

## RAG 部分 → `../basics/`

- RAG 机制五步、为什么需要 RAG（vs 微调/大上下文）、生产级流水线、工程原则、参考架构。

## 记忆部分 → `../memory/`

- 短期记忆、长期记忆、状态与检查点、记忆治理、记忆层级。

## Agentic RAG 部分 → `../agentic-rag/`

- 检索即工具、四类 Agent、四种适用场景、能力边界、落地顺序。

## 其余展开

| 目录 | 内容 |
|---|---|
| `../chunking/` | 八种切块方法、父子里程碑、Contextual / Late chunking |
| `../retrieval/` | 混合检索、BM25、RRF、cross-encoder、查询变换 |
| `../embedding/` | 模型选择、input_type 陷阱、Matryoshka |
| `../vdb/` | HNSW/IVF/PQ、产品对比、元数据过滤 |
| `../graphrag/` | 知识图谱、RAPTOR、语义层、查询路由 |
| `../eval/` | RAG Triad、四层方案、RAGAS |
| `../frameworks/` | LlamaIndex/LangChain/Haystack 等选型 |
| `../prod/` | RBAC、索引新鲜度、成本、上线清单 |

> 检索质量应作为一等指标，而不是事后补充。
