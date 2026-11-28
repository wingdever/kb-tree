---
description: "Graph-guided crawl planning: topic to anchor entities, relation neighbors, source mapping and crawl plan"
描述: "主题图谱扩展抓取：主题到锚点实体、关系邻居、来源映射与抓取计划"
name: "Topic Graph Crawl"
名称: "主题图谱扩展抓取"
---

# 主题图谱扩展抓取

只给一个主题时，最难的不是抓，而是“不知道要抓哪些东西”。开放知识图谱可以补上这一段：先把主题落到一组实体，再沿关系取邻居，最后把实体映射到具体来源，生成可执行的抓取计划。

图谱负责“抓什么”，来源映射负责“去哪抓”；两者不能混为一谈。

## 六步链路

```text
主题
  ↓ 实体链接 / 标签检索 / 别名扩展
锚点实体
  ↓ 关系白名单 + 1–3 跳
候选实体
  ↓ 相关性排序 + 去枢纽 + 去重
实体集合
  ↓ 实体 → 来源映射
抓取计划
  ↓ 抓取 / 解析 / 回填
新实体与新链接
```

1. **主题落到锚点**。主题往往不是单个实体（“Agent 开发”是领域，不是实体）；先找一组锚点：AI agent、LLM agent、tool use、RAG、multi-agent、planning、MCP。
2. **沿关系扩展**。按关系白名单跳 1–3 跳；每跳记录路径，便于后面解释“为什么这个实体相关”。
3. **排序与裁剪**。按路径长度、关系类型、节点中心度、主题相关性排序；去掉泛化节点、消歧页与高入度枢纽。
4. **实体映射来源**。每个实体转成可抓的 URL、API 查询或搜索词，而不是停在一个图谱 ID。
5. **生成抓取计划**。每条目标带来源类型、查询/URL、期望字段、优先级与预算。
6. **抓取后回填**。从页面抽新实体与链接，重新做实体链接；有预算与停止条件，避免无限扩张。

## 关系怎么选

不是所有边都值得跳。按主题类型选关系白名单：

| 主题类型 | 优先关系 | 目的 |
|---|---|---|
| 技术 / 产品 | subclass of、part of、used for、requires、implemented by | 找上下位、组件、依赖与实现 |
| 公司 / 组织 | owns、subsidiary of、founder of、located in | 找母公司、子公司、人物与地点 |
| 学术 / 研究 | authored by、cites、published in、same topic | 找作者、论文、期刊与主题邻居 |
| 人物 | affiliated with、member of、known for | 找机构、角色与代表作品 |
| 地理 | located in、adjacent to、part of | 找行政层级、周边与组成 |

要避免的关系：`sameAs` 链、纯分类边、`related to` 这种无边界的泛关系。它们会把图扩展成“什么都相关”。

## 实体怎么变成抓取目标

同一个实体，不同来源给不同东西：

- **Wikidata**：实体页、`official website`、`described at URL`；适合拿别名、官网与跨库 ID。
- **DBpedia**：摘要页、`homepage`、外部链接；适合补通用描述，但要注意版本旧。
- **OpenAlex**：作者/机构/论文 ID 与 API 查询；适合学术主题。
- **GitHub**：仓库搜索词；适合开源实现与工具。
- **arXiv**：论文查询；适合方法与基准。
- **厂商文档 / 官网**：产品文档、价格、更新日志。
- **通用搜索**：实体名 + 限定词；只作为发现，不直接当事实源。

一个实体可以映射多个目标；优先级按“官方性、结构稳定性、更新频率、合规成本”排序。

## 输出契约

抓取计划至少包含：

```json
{
  "topic": "Agent 开发",
  "anchor_entities": [{"name": "AI agent", "kg_id": "...", "source": "Wikidata"}],
  "targets": [{
    "entity": "AI agent",
    "relation_path": ["subclass of"],
    "source_type": "wikidata_entity",
    "url_or_query": "https://www.wikidata.org/entity/...",
    "expected_fields": ["aliases", "official_website"],
    "priority": "high",
    "budget": {"max_pages": 1}
  }],
  "stop_conditions": {"max_depth": 2, "max_targets": 200, "min_relevance": 0.6}
}
```

没有 `relation_path` 的计划不可解释；没有 `stop_conditions` 的计划不可执行。

## 停止条件与质量门禁

- **跳数**：1–2 跳通常够用，第 3 跳开始噪声迅速上升。
- **扇出**：单个实体最多取 N 个邻居；枢纽节点单独限流。
- **相关性**：用主题分类器或 embedding 相似度给候选打分，低于阈值不扩展。
- **去重**：同一实体多来源合并；同一 URL 规范化后只留一条。
- **预算**：每个来源的页数、请求数、渲染次数都有上限。
- **人工复核**：第一版计划先抽样审查，再放开自动执行。

## 常见失败

- **把主题当实体**。主题是领域时，直接查标签往往查不到；必须先做锚点集合。
- **只跳不筛**。图扩展的组合爆炸很快，第二跳就可能得到成千上万实体。
- **被枢纽节点带偏**。通用概念（软件、系统、公司）连接一切；需要中心度惩罚或白名单。
- **图谱 ID 当 URL**。实体页不是你要的业务页面；必须做来源映射。
- **图谱太旧**。开放图谱的版本与时效有限；关键事实要回到原始页面核对。
- **许可误判**。图谱数据可查，不等于可批量镜像或再分发；计划里要带许可字段。

## 一句话主线

用开放知识图谱把主题展开成“锚点实体 → 关系邻居 → 候选实体”，再用实体到来源的映射生成带路径、字段、预算与停止条件的抓取计划；图谱解决“抓什么”，来源映射解决“去哪抓”，质量门禁解决“抓到哪停”。

## 参考资料

- Wikidata 数据访问（SPARQL、实体 URL 与 dump）：https://www.wikidata.org/wiki/Wikidata:Data_access
- OpenAlex 官方文档（实体 ID、API 与快照）：https://docs.openalex.org/
- DBpedia 官方文档（SPARQL 与数据集）：https://www.dbpedia.org/
- Scrapy 2.x 官方文档（把计划落成 Spider 与 Pipeline）：https://docs.scrapy.org/en/latest/topics/architecture.html
