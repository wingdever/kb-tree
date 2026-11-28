---
description: "Knowledge tree for vector databases and ANN indexes"
描述: "向量数据库：索引算法、产品对比与元数据过滤"
name: "Vector Databases and ANN Indexes"
名称: "向量数据库"
---

# 向量数据库与 ANN 索引

向量数据库专门存"意思坐标"并毫秒级找相似，是 RAG 与语义搜索的底座。核心是用 ANN（近似最近邻）以一点召回换巨大速度。本主题已拆成 4 个子知识点目录。

## 什么时候才需要

- **该上**：需要毫秒级相似查询，且数据规模已超出内存暴力扫描。
- **别上**：数据量很小，或查询本质是精确键匹配与事务操作。
- 2026 模式：前 90 天用嵌入式（LanceDB、Chroma、FAISS），毕业到生产再迁专用库。

## 参考资料

- Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs：https://arxiv.org/abs/1603.09320
- Billion-scale similarity search with GPUs（FAISS）：https://arxiv.org/abs/1702.08734
