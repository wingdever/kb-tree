---
description: "Building knowledge graphs with LLMs: ontology, entity resolution, provenance and validation"
描述: "知识图谱构建：本体、实体消歧、溯源与校验"
name: "Knowledge Graph Construction"
名称: "知识图谱构建"
---

# 知识图谱构建

图数据库是存储技术，知识图谱是放进它的内容。LLM 让图构建从规则流水线转向生成式抽取，但**把噪声四起的 LLM 输出变成干净、去重、可查询的图，才是真正的工程**。先于 GraphRAG 范式存在的关键一步。

## 何时才开始建

只有当关系密集型查询在试点中胜过文档检索后才启动。写**能力问题（competency questions）**，定义版本化本体，分配稳定实体 ID。图提升显式遍历与冲突表达，但增加本体、实体解析和管理成本。

一个常见错误：**因为图看起来比混合搜索更高级就建图**。

## 五大核心能力

1. **本体与 schema 强制**：无约束 LLM 抽取会产生混乱的重叠谓词（works_at / employed_by / is_staff_at）。生产流水线强制类型化 schema（Pydantic 或 OWL/SHACL），让抽取的节点与边符合一致的领域模型。先定干系人每周会跑的查询，再建最小 schema——别数据还没来就上 500 类 OWL 层级。
2. **实体解析与去重**：识别 "IBM"、"International Business Machines"、"IBM Corp." 是同一规范节点，结合嵌入相似度、词法模糊匹配、LLM 消歧。**本质二次复杂度，需人工判断，是工具支持最弱的一步**。重复节点摧毁遍历价值；跳过实体解析是常见致命错误。
3. **来源溯源与时间有效性**：每个节点和边保留到源文档、页、时间戳的反向引用，并记录有效性窗口（valid_from / valid_to）——事实随时间演化。用 W3C PROV-O 等记录血缘，支持引用、审计、受控检索。
4. **社区摘要与图-向量混合索引**：既支持精确多跳 Cypher/SPARQL 遍历（"找供应商 X 两跳内的所有厂商"），也支持 Leiden 社区检测的层级全局综合（Microsoft GraphRAG 模式）。
5. **增量更新而非全量重建**：每次十几个文件变化就重跑整个 10 万文档语料的 LLM 抽取，成本高到不可接受。成熟工具支持增量 delta 摄取与局部社区重摘要。

## 抽取流水线（LLM 时代）

- 传统：spaCy + StanfordNLP（规则+统计）。
- 大模型时代：LLM Prompt + LangChain/LlamaIndex 零样本抽取，精度更高。
- **抽取必须带 source span、confidence、extractor version、tenant/ACL、valid time**。
- 每条边都要有出处；无出处就不建边（反模式：creating edges without source-span provenance）。
- LLM 抽的三元组**必须校验**：人工审核或置信度阈值，合规与金融场景强制。
- 图查询暴露跨敏感边界的路径——在图 API 层按子图/标签限权，别写进 LLM 提示。

## 工具生态

| 工具 | 定位 | 特点 |
|---|---|---|
| **Neo4j LLM Knowledge Graph Builder** + neo4j-graphrag | 端到端（建+查） | Web UI/API 摄取 PDF/网页，schema 引导抽取，实体去重，写入 Neo4j + 向量；成熟 ACID、Cypher、可视化 |
| **Microsoft GraphRAG** | 全局语料综合 | LLM 抽实体关系 → Leiden 聚类社区 → 层级社区摘要；Global 查询强，索引贵 |
| **LlamaIndex PropertyGraphIndex** | 可组合 Python 抽象 | 并行多抽取器，持久化到 Neo4j/Memgraph/FalkorDB/Neptune/Kuzu，向量+图同时查 |
| **Cognee** | 模块化记忆引擎 | add→cognify→search，关系+向量+本体图统一，支持时间图、反馈重加权 |
| **Graphiti (Zep)** | 时间图/agent 记忆 | 每条边带有效期，事实演化，增量快，需 Neo4j |

## 前沿方向（2026）

- **GraphAnchor**：把演进的 KG 索引与 RAG 多跳检索循环紧耦合，从 top-k 检索文档增量锚定实体关系，用索引偏置后续检索并支撑跨段接地。
- **DIAL-KG**：元知识库编排驱动双轨（三元组/事件）抽取、治理裁决、schema 归纳，事务式集成与自适应 schema 生长。
- **增量/检索增强构建**：流式与 RAG 式构建、动态 schema 归纳、事件驱动优化；实体共指与对齐仍是召回误差主源。
- 多模态/多语言、人机协作策展、轻量 SLM 做治理校验是趋势。

## 落地清单

- [ ] 能力问题证明图的必要性。
- [ ] 本体与实体身份已版本化。
- [ ] 每条边有 source span、时间、ACL、抽取血缘。
- [ ] 实体解析（规范化、合并策略、审计轨迹）到位。
- [ ] 高影响边需人工或可信规则批准。
- [ ] 合并、回滚、纠错测试通过。
- [ ] 发布不可变图版本与回滚清单；源文档保持权威。

## 参考资料

- From Local to Global: A Graph RAG Approach to Query-Focused Summarization：https://arxiv.org/abs/2404.16130
- A Survey on Knowledge Graphs: Representation, Acquisition and Applications：https://arxiv.org/abs/2003.02320
