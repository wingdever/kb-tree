---
description: "Pre/post filtering, adaptive filtering, RBAC and metadata design"
描述: "前后过滤、自适应过滤、RBAC 与元数据设计"
name: "Filtering and Metadata"
名称: "过滤与元数据"
---

# 过滤与元数据

## Pre-filter vs Post-filter

- **Pre-filter**：先按元数据过滤再做向量检索。正确，但过滤选择性低时慢。
- **Post-filter**：先检索再过滤。快，但可能返回不足 k 条结果。
- **自适应过滤（2026 模式）**：查询规划器估计过滤选择性，按查询动态选 pre 或 post。

```python
def adaptive_search(query_vec, filter_dict, k=10, selectivity_threshold=0.05):
    estimated = estimate_selectivity(filter_dict)
    if estimated < selectivity_threshold:
        return vector_store.search(query_vec, k=k, filter=filter_dict, mode="pre")
    else:
        return vector_store.search(query_vec, k=k*3, filter=filter_dict, mode="post")[:k]
```

## 元数据设计与 RBAC

生产系统里元数据（时间、部门、标签）通常存在关系库，向量库存坐标，两者通过 ID 关联，查询时先条件过滤再做相似检索。

- **安全 RBAC**：用户在 SharePoint 看不到的文档，不能通过 RAG 检索到其块。把 ACL 嵌入向量元数据（如 `allowed_groups: [hr, management]`），检索前按用户组过滤。
- **质量提升**：IEEE 研究显示带归属、血缘、质量分、分类、policy context 的元数据，检索精度明显高于仅用内容；Atlan 研究称治理型元数据能明显提升 Agent SQL 准确率。
- 时间戳、来源类型、溯源标记让检索器可对新鲜度打分，生成器可标记过时证据。

## 生产系统里的元数据字段

| 字段 | 用途 |
|---|---|
| `timestamp` / `publication_date` | 新鲜度打分、过时标记 |
| `source` / `allowed_groups` | RBAC、溯源 |
| `doc_type` / `tags` | 按类型过滤、路由 |
| `quality_score` | 低质过滤 |
| `chunk_id` / `parent_id` | 父子检索、去重、稳定 ID |

## 多租户与过滤下推

- Qdrant 的 payload 过滤下推最干净；Weaviate 对象模型元数据是一等公民。
- 强 tenant 隔离需按 tenant_id 预过滤，避免跨租户泄露。
- 过滤字段建索引（如 keyword/keyword 数组类型）以获得高效过滤。

## 参考资料

- Qdrant Filtering 文档：https://qdrant.tech/documentation/concepts/filtering/
- Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs：https://arxiv.org/abs/1603.09320
