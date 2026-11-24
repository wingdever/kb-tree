---
description: "Cross-Encoder, ColBERT late interaction and LLM rerankers"
描述: "交叉编码器、ColBERT 延迟交互与 LLM 重排器"
name: "Reranking"
名称: "重排"
---

# 重排（Reranking）

标准模式：从混合索引召回 50–100 个候选（50–100ms），再用 cross-encoder 或 LLM 重排器对候选精排（100–400ms），保留 top 5–20 给生成。端到端约 200–500ms 换 10× 质量提升。

## 为什么需要重排

即使最好的嵌入模型（Voyage-3-large、text-embedding-3-large）也把每个文档压成**单个向量**，丢失细粒度的查询-文档交互。重排器在查询期**联合读取** query 和文档，精准得多。生产基准上重排器在任何嵌入模型之上再加 **8–14 NDCG 点**。

## 重排器类型

| 类型 | 代表 | 延迟(50 候选) | 特点 |
|---|---|---|---|
| 托管 cross-encoder | Cohere Rerank 3.5/4 | 80–220ms | 多语言、强默认；$2/1K |
| 托管 cross-encoder | Voyage rerank-2.5 | 100–250ms | 长上下文、RAG 调优 |
| 自托管 cross-encoder | BGE-Reranker-v2-m3 | 90–140ms | 开源 Apache 2.0、多语言、自托管默认 |
| 自托管 cross-encoder | ms-marco-MiniLM | 40–110ms | 延迟优先、仅英语 |
| 延迟交互 | ColBERT v2 | 50–200ms | 快，但需 token 级索引 |
| LLM-as-reranker | GPT-4o-mini/Haiku | 300–1000ms | 最高质量、最贵 |

**MTEB reranking 分数**（2026-08）：BGE-reranker-v2-m3 59.7、Cohere Rerank 3.5 63.4、ColBERT v2 56.2、ms-marco-MiniLM-L-6 43.1。自托管 BGE 与闭源 API 差距只有 3–4 分——日查询 >5 万时自托管单位经济性好得多；<5 万时 Cohere 的 $2/1K 比养一张闲置 A10G 便宜。

## 三种 LLM 重排风格

- **Listwise（RankGPT 式）**：LLM 一次看全部候选，输出排列。最准、最贵、最难确定性。
- **Pointwise**：LLM 独立给每个文档 1–10 分。易并行、弱（无比较信号）。
- **Pairwise 锦标赛**：两两比较，按胜数汇总排名。可靠但成本平方级。

## Cross-Encoder 深入

把 query 与候选拼接送入 Transformer，每个 token 全交叉注意力，直接输出相关性分。

- **代价**：无法预计算，每条候选需完整前向；延迟随候选数**线性增长**——重排 200 个候选是 50 个的 4× 延迟。
- 多数情况下前 200 token 决定相关性，可把候选块截断到 256 token 做重排（送入 LLM 的仍是完整块）。
- 标准用法：便宜地取 k=50–200，重排 top k=5–20。

## ColBERT（延迟交互）

不把文档压成单向量，而是每 token 一个向量；相似度 = 每个查询 token 对文档 token 的最大相似度之和（MaxSim）。

- 文档向量预计算并索引 → 质量接近 cross-encoder，延迟接近 bi-encoder。
- **重排成本对候选数次线性**：实测 ColBERT 重排 500 候选与 cross-encoder 重排 50 候选耗时相当。
- **代价：存储**。ColBERTv2 用残差压缩把存储降到稠密索引的 5–10×（未压缩 50–100×）。100 万块 × 512 token 约 200–400GB（压缩前）。<50 万块可管理。
- 适合：长尾召回（k=200+ 才出正确答案）、多向量查询（分解子查询）、低延迟预算。
- RAGatouille、PLAID、jina-colbert-v2 是 2026 生产级实现，可装入 Qdrant/Weaviate/LanceDB。

## 什么时候跳过重排

先验证第一阶段召回的 Recall@k：
- **Context Recall < 0.70**：正确块根本没召回——问题是切块/嵌入覆盖/索引缺失，重排救不了（见 `../../eval/`）。
- **Recall > 0.85 但精度低**：正确块在 top-100 却没浮到 top-5——这正是重排的目标。

降低重排延迟的技巧：候选池 top-100→top-50（损失 <2% 召回、时间减半）、候选截断 256 token、按 (query, 候选集 hash) 缓存重排分（成熟系统命中率 30–60%）。

> 相关：召回见 `../recall/`；融合见 `../fusion/`。
