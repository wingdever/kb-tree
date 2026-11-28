---
description: "Navigation page for memory and RAG topics"
描述: "记忆与 RAG：记忆分层与检索的配合方式"
name: "Memory and RAG"
名称: "记忆与 RAG"
---

# 记忆与 RAG

记忆与 RAG 在同一条链上：RAG 解决「知识从哪来」，记忆解决「什么该留下」。本页只讲这两者的交界与分工，具体机制各自成文。

## 三条主线

- **RAG 机制**：五步流程、为什么需要 RAG（对比微调与大上下文）、生产级流水线、工程原则与参考架构。
- **记忆分层**：短期记忆、长期记忆、状态与检查点，以及记忆治理与层级设计。
- **检索即工具**：把检索交给 Agent 自主调用，四类 Agent、四种适用场景、能力边界与落地顺序。

## 其余相关能力

- 切块：八种方法、父子里程碑、Contextual 与 Late chunking。
- 检索：混合检索、BM25、RRF、cross-encoder、查询变换。
- 嵌入：模型选择、input_type 陷阱、Matryoshka 表示。
- 索引：HNSW/IVF/PQ、产品对比、元数据过滤。
- 图与结构化：知识图谱、RAPTOR、语义层、查询路由。
- 评估：RAG Triad、四层方案、RAGAS。
- 框架：LlamaIndex/LangChain/Haystack 等选型。
- 生产：RBAC、索引新鲜度、成本、上线清单。

> 检索质量应作为一等指标，而不是事后补充。

## 参考资料

- MemGPT: Towards LLMs as Operating Systems：https://arxiv.org/abs/2310.08560
- Generative Agents: Interactive Simulacra of Human Behavior：https://arxiv.org/abs/2304.03442
