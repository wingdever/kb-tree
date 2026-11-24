---
description: "Knowledge tree for vector databases and ANN indexes"
描述: "向量数据库知识树导航"
name: "Vector Databases and ANN Indexes"
名称: "向量数据库"
---

# 向量数据库与 ANN 索引

向量数据库专门存"意思坐标"并毫秒级找相似，是 RAG 与语义搜索的底座。核心是用 ANN（近似最近邻）以一点召回换巨大速度。本主题已拆成 4 个子知识点目录。

## 什么时候才需要

- **该上**：十万级以上向量、秒级返回、要与元数据混合过滤。
- **别上**：几百条资料（内存数组几毫秒搞定）、纯精确关键词匹配、强事务 OLTP。
- 2026 模式：前 90 天用嵌入式（LanceDB、Chroma、FAISS），毕业到生产再迁专用库。

