---
description: "RRF fusion, score normalization and query rewriting techniques"
描述: "RRF 融合、分数归一化与查询改写技术"
name: "Fusion and Query Transformation"
名称: "融合与查询变换"
---

# 融合与查询变换

## 融合（Fusion）：混合检索的合并规则

同时跑 BM25 和向量检索时，两路分数量纲不同（BM25 分数与余弦距离不可直接比较）。两种合并方式：

### RRF（互易秩融合，推荐默认）

不看原始分数，只看排名：

```
RRF_score = Σ 1/(k + rank_i)       k 通常取 60
```

- k=60 防止单一榜单头部结果过度主导。
- 在两榜都靠前的文档总分更高；只被单一检索器找到的文档被惩罚。
- 例：文档 A（BM25 第 1、稠密第 5）→ 1/61 + 1/65 = 0.0318；文档 B（两榜都第 3）→ 1/63 + 1/63 = 0.0317。

**RRF vs 分数归一化**：

| 维度 | 分数归一化 | RRF |
|---|---|---|
| 需分数校准 | 是 | 否 |
| 调参 | 权重 α | 常数 k（60 几乎总够） |
| 批依赖 | 是（分数随批次漂移） | 否（只看排名） |
| 简洁性 | 中 | 很简单 |

多数应用 RRF 是更安全默认。

### 分数归一化

Min-max 把两路分数缩放到 0–1，再加权求和：`final = α·dense_norm + (1−α)·sparse_norm`。α 控制信任哪一路，靠评估框架调（典型 0.3–0.8）。问题是归一化分数依赖当前批次结果，同一文档在不同批次得分不同，稳定性差。

## 查询变换（Query Understanding）

查询本身的质量决定检索上限。用户查询是噪声输入——可能模糊、缺上下文、表述与语料不匹配。**永远不要信任原始查询**。2026 常见模式：

- **查询改写（rewriting）**：把原始查询改写成检索友好的形式。例："上周我们聊的那个事怎么做" → 结合对话上下文改写为"企业版定价策略"。实现：小 LLM 调用，延迟 200–500ms。
- **查询分解（decomposition）**：复杂多部分问题拆成原子子查询，分别检索再合并。
- **Step-back 提示**：把具体问题抽象成更宽泛概念再检索。
- **查询扩展（expansion）**：加同义词/相关词（SPLADE 自动做，或手工词表）。
- **查询路由（routing）**：把查询分派到不同检索路径或索引。
- **HyDE（假设文档嵌入）**：LLM 先起草假答案，嵌入这段文本去搜真实文档。洞察：向量空间里"问题"与"答案"分布在不同区域，"假设答案"与真实答案更接近。代价多一次 LLM 调用。

这些技术相互独立，可组合。查询改写增加约 200–400ms，用改写缓存缓解。

## 融合 + 重排的完整流水线（生产参考）

```python
def retrieve_and_rerank(query, k_retrieve=50, k_final=10):
    # 1. 混合召回
    query_emb = embed(query)
    dense = vector_db.search(query_emb, top_k=k_retrieve)
    sparse = bm25_index.search(query, top_k=k_retrieve)
    fused = reciprocal_rank_fusion(dense, sparse)   # RRF 融合
    # 2. 重排
    docs = [d.text for d in fused[:k_retrieve]]
    scores = reranker.rerank(query, docs)
    ranked = sorted(zip(fused, scores), key=lambda x: x, reverse=True)
    return [doc for doc, _ in ranked[:k_final]]
```

延迟预算：embed 50–100ms + 并行检索 50–150ms + 重排 top50 100–300ms ≈ 200–550ms（生成前）。

## 自适应 / 纠正型检索

- **Adaptive RAG / Agentic 路由**：轻量 router 分析意图与复杂度——简单跳过检索，需内部事实触发混合搜索，需新鲜数据走 web 或 SQL。
- **CRAG（Corrective RAG）/ Self-RAG**：评估器判断检索文档相关性；置信度低时触发备用动作（web 搜索），而非基于坏数据幻觉答案。

## 参考资料

- Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods：https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
- RAG-Fusion: a New Take on Retrieval-Augmented Generation：https://arxiv.org/abs/2402.03367
