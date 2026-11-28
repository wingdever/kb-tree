---
description: "HNSW, IVF, PQ, DiskANN and ScaNN index algorithms"
描述: "HNSW、IVF、PQ、DiskANN 与 ScaNN 索引算法"
name: "ANN Index Algorithms"
名称: "ANN 索引算法"
---

# ANN 索引算法

暴力扫描百万级高维向量太慢，ANN（近似最近邻）以一点召回换巨大速度。五种算法家族主导生产。

## 算法对照

| 算法 | 年份 | 原理 | 优点 | 代价 | 适用 |
|---|---|---|---|---|---|
| **HNSW** | 2016 | 多层可导航近邻图 | 召回/延迟 Pareto 最优；多数 VDB 默认 | 内存大、构建慢、删除难 | 内存内、百万级、延迟敏感 |
| **IVF** | 2010s | k-means 分桶，搜最近桶（`nprobe`） | 简单、GPU 友好、配 PQ 好 | 同速下召回低于 HNSW；桶数要调 | 千万级、分布稳定 |
| **PQ** | 2010 | 向量压缩成子量化器乘积 | 内存降 10–100× | 召回损失；单独用不佳 | 亿级、成本优先 |
| **DiskANN** | 2019 | SSD 上的单遍图索引 | 单机十亿级、存储便宜 | 延迟高于内存 HNSW | 超内存规模 |
| **ScaNN** | 2020 | 各向异性量化 + IVF | 极低延迟下强召回 | 第三方 VDB 较少 | Google 硬件 |

## HNSW 深入

分层近邻图：增量构建多层图，从顶层稀疏图向下层稠密图下降，实现对数复杂度搜索。

- 召回质量最好、查询延迟最低；是 Qdrant、Weaviate、Chroma、pgvector 的默认。
- **Pinecone 例外**：称从未使用 HNSW，运行自研索引（PQFS、IVF 等）。
- 插入高效、**删除难**——生产多用 tombstone + 定期重建。
- 内存占用大。

## IVF / IVF-PQ

先用 k-means 把向量聚类分桶，查询只扫最近的几个桶（桶数由 `nprobe` 控制）。聚类边界处向量可能漏掉。配 PQ 压缩向量本身，内存效率大幅提升——千万级、数据分布稳定的场景。

## 其他

- **PQ（Product Quantization）**：把高维向量切成子空间，每个子空间用码本量化，内存降 10–100×。单独用召回差，通常叠加在 IVF 或 HNSW 上。
- **DiskANN**：图索引放 SSD，单机十亿级、存储便宜，延迟略高。Milvus 提供 DiskANN 作为 on-disk 索引。
- **ScaNN**：Google 的各向异性向量量化，强召回 + 极低延迟。

## 工程经验

- 百万级以内**默认 HNSW**；规模上来评估 IVF；真正亿级且存储成瓶颈才上 PQ 并接受精度损失。绝大多数团队的第一版 HNSW 都够用。
- 2026 常见组合：**HNSW 做热层**（近 30 天、内存）+ **IVF-PQ/DiskANN 做冷层**。
- 别信合成基准——用你自己的嵌入、过滤、查询日志做基准。

## 集合通信速记（训练侧对照）

AllReduce = ReduceScatter + AllGather；检索侧的关键是选对 ANN 索引。

## 参考资料

- Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs：https://arxiv.org/abs/1603.09320
- Billion-scale similarity search with GPUs（FAISS）：https://arxiv.org/abs/1702.08734
- DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node：https://arxiv.org/abs/1806.05141
