---
description: "Free vector search quotas: Pinecone Starter 2GB and 1M ops/month, Qdrant Cloud 1M 768-dim vectors, Upstash 1GB and 10K queries/day"
描述: "免费向量检索额度：按存储、按向量维度乘积、按每日查询计"
name: "Free Vector Search"
名称: "免费向量检索"
---

# 免费向量检索

向量库的免费额度有三种口径，混着看会误判：

- **按存储**：给多少 GB 或 RAM，能装多少条取决于维度。
- **按"向量数 × 维度"乘积**：看着是 2 亿，其实是"维度 × 条数"的上限。
- **按每日查询数**：能存很多，但查得少。

先算一条账：float32 向量每条占 `维度 × 4 字节`。768 维 ≈ 3KB/条，100 万条 ≈ 3GB（还不含索引与元数据）；1536 维翻倍。这个换算决定了"1GB 能装多少条"。

## 三条托管路线

**Pinecone Starter**：免费，含 **2GB 存储、每月 100 万次读 / 100 万次写、每月 500 万嵌入 token**（2026-11-04 至 12-31 促销翻倍到 1000 万，按模型计）。它是"超额阻断"型：超出月额度直接挡住，不扣费，下个周期重置。限制是 **Starter 只能在 AWS us-east-1**，且索引数、项目数、协作人数都很紧。

**Qdrant Cloud Free**：永久免费的单节点集群，**0.5 vCPU / 1GB RAM / 4GB 磁盘**，官方说大约装得下 **100 万条 768 维向量**。要留意回收规则：**闲置 1 周挂起、4 周不激活就删除**——它不适合"建好放着以后用"。

**Upstash Vector**：免费档给"2 亿 向量×维度"的乘积上限、**1GB 数据、每天 1 万次查询/更新、100 个命名空间、10 个索引、维度上限 1536**。按 1536 维折算，2 亿乘积其实只相当于约 13 万条，别被数字误导。

另有两个常见选项只作线索：Weaviate Cloud 有"1 集群 / 10 万对象 / 1GB 内存"的长期免费档，Zilliz Cloud 免费档给 5GB 存储与每月 250 万向量计算单元——两者都来自第三方汇总，接入前请回官方页核对。

## 最省钱的一条：复用已有 Postgres

如果已经在用免费的 Postgres（Supabase 或 Neon），直接开 `pgvector` 扩展，向量就存在同一个库里：**增量成本是 0**，不占额外的免费额度，也不用再学一套 SDK。代价是性能与索引能力不如专用向量库，适合"几万条以内、QPS 不高"的场景。

同理，自建 Qdrant、Milvus、Chroma 软件全免费，成本只是一台机器；本地开发甚至可以直接跑在笔记本上。

## 怎么选

| 场景 | 方案 |
|---|---|
| 边做边试、数据量小 | 已有 Postgres + pgvector（零增量成本） |
| 要托管、要省心 | Pinecone Starter（注意仅 us-east-1） |
| 百万级 768 维原型 | Qdrant Cloud Free（记得每月唤醒） |
| 高频小查询、要 Redis 生态 | Upstash Vector |

## 四个坑

1. **"2 亿向量"是乘积**：2 亿 ÷ 1536 维 ≈ 13 万条，不是 2 亿条。
2. **闲置会被回收**：Qdrant 1 周挂起、4 周删除；免费档不是存档服务。
3. **超额策略不同**：Pinecone 是阻断、Qdrant 是撞资源上限、Upstash 是日查询封顶，报错形态完全不一样。
4. **免费档常只给一个索引/一个库**：多环境（dev/staging/prod）共用一套额度，容易互相挤占。

## 一句话主线

免费向量检索的关键是**先把"维度 × 条数 × 4 字节"算清楚，再看额度是按存储、按乘积还是按查询给**：小数据量优先复用已有 Postgres，要托管再选专用库，并且记得免费档会回收闲置资源。

## 参考资料

- Pinecone 免费档额度（2GB、每月 100 万读/写、500 万嵌入 token）：https://www.pinecone.io/blog/turn-azure-data-into-an-ai-ready-knowledge-base
- Pinecone 定价（超额阻断、月额度重置、Starter 示例负载）：https://www.pinecone.io/pricing/
- Qdrant Cloud 免费档（0.5 vCPU/1GB RAM/4GB 磁盘、约 100 万 768 维、闲置 1 周挂起 4 周删除）：https://qdrant.tech/cloud/
- Qdrant 定价页（免费档资源与超限后的升级路径）：https://qdrant.tech/pricing/
- Upstash Vector 免费档（200M 向量×维度、1GB、每日 1 万查询、1536 维）：https://upstash.com/pricing/vector
- 免费向量库汇总（Weaviate 10 万对象/Zilliz 5GB，二手来源待核）：https://agentdeals.dev/best/free-vector
