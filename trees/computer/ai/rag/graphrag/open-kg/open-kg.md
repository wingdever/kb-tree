---
description: "Open knowledge graphs available online: Wikidata, DBpedia, OpenAlex, GeoNames, ConceptNet and selection criteria"
描述: "网上可用的开放知识图谱：Wikidata、DBpedia、OpenAlex、GeoNames、ConceptNet 与选型标准"
name: "Open Knowledge Graphs"
名称: "开放知识图谱"
---

# 开放知识图谱

网上确实有一批可用的开放知识图谱，但“开放”要分四层看：能不能访问、能不能批量下载、能不能商用、能不能再分发。很多图谱 API 免费，却不允许全量镜像；很多数据 CC0，但质量和时效参差。

## 主要开放图谱

| 图谱 | 主要内容 | 访问方式 | 许可与注意 |
|---|---|---|---|
| **Wikidata** | 多语言实体、属性、关系、陈述与引用 | SPARQL、API、JSON/RDF dump | CC0；覆盖面广，但事实完整度与精度参差，需按 rank 与引用筛选 |
| **DBpedia** | 从 Wikipedia 抽取的结构化实体与关系 | SPARQL、dump、Linked Data | CC BY-SA；版本相对旧，映射与抽取误差要抽样核验 |
| **OpenAlex** | 论文、作者、机构、主题、引用关系 | REST API、快照 | CC0；适合学术图谱，作者/机构消歧仍是主要噪声 |
| **GeoNames** | 地名、坐标、行政层级、别名 | dump、API | CC BY 4.0；地理实体强，非通用知识图谱 |
| **ConceptNet** | 常识关系、词与短语的多语言连接 | dump、API | CC BY-SA 4.0；口语与常识丰富，但噪声与歧义明显 |
| **OpenStreetMap** | 道路、POI、行政边界等地理要素 | Overpass、dump、API | ODbL 1.0；是地理图，不是通用实体图 |
| **OpenKG.cn** | 中文开放图谱与数据集集合 | 各项目页面/下载 | 各数据集许可不一，必须逐个核对，不能按“整站开放”理解 |
| **Freebase** | 早期通用实体图谱 | 历史 dump | 已停止维护；只适合历史研究，不建议新项目依赖 |

YAGO、BabelNet 等也有开放或学术版本，但商用与再分发限制要逐项确认；Google、Microsoft 的知识图谱不开放全量，只有受限 API。

## 选型维度

1. **许可**：是否允许商用、批量下载、再分发、派生作品；CC BY-SA 的 share-alike 会传染。
2. **覆盖**：领域、语言、实体类型、关系类型是否匹配；通用图谱在垂直领域通常不够深。
3. **结构**：有没有稳定 ontology、identifier 与类型体系；能否与自有实体对齐。
4. **时效**：版本日期、更新频率、事实引用；DBpedia 与 Freebase 的陈旧问题尤其明显。
5. **访问**：SPARQL、API、dump 哪种可用；全量 dump 的体量与更新成本。
6. **质量**：事实精度、实体消歧、关系方向、重复与冲突；需要抽样评估。
7. **可连接**：是否有 QID、DOI、坐标、sameAs 等 join key；否则对齐成本很高。

## 接入 GraphRAG 的方式

- **实体链接**：把查询与文档中的 mention 对齐到图谱 ID（如 Wikidata QID），再做子图扩展。
- **只取子图**：按实体取一跳/两跳邻居、关键属性与关系；不要把整个图谱塞进上下文。
- **作为种子图**：用开放图谱提供通用实体与关系，再用私有语料补领域事实、时间与权限。
- **做校验与扩展**：用图谱验证实体类型、别名、上下位关系；用图路径补充多跳证据。
- **保留 provenance**：记录事实来自哪个图谱、哪个版本、哪条陈述；不同图谱冲突时不要静默合并。

## 常见坑

- **把“可访问”当成“可商用”**：API 免费不等于许可宽松；CC BY-SA 与 ODbL 都有再分发义务。
- **直接依赖过期图谱**：DBpedia、Freebase 的版本旧，实体与关系可能已变化；要标注版本与抓取时间。
- **全量 dump 硬扛**：Wikidata 全量很大，先做子集/主题切片，再按需更新。
- **实体歧义**：同名人物、公司、地名很多；只按标签匹配会把错误实体拉进上下文。
- **事实冲突**：多个图谱对同一属性给出不同值；要保留来源与置信度，不要合并成“唯一真相”。
- **上下文膨胀**：把邻居全量展开会挤占窗口；按查询意图裁剪属性与跳数。

## 一句话主线

开放知识图谱可以作为 GraphRAG 的冷启动与实体底座：优先 Wikidata/OpenAlex 这类许可清晰的源，按实体取子图、保留来源与版本，再用私有语料补领域事实；先看许可与时效，再谈覆盖。

## 参考资料

- Wikidata 数据访问（CC0；SPARQL、dump 与 API）：https://www.wikidata.org/wiki/Wikidata:Data_access
- DBpedia 官方文档（数据集、SPARQL 与许可）：https://www.dbpedia.org/
- OpenAlex 官方文档（CC0 学术图谱与快照）：https://docs.openalex.org/
- GeoNames 官方文档（地名数据与许可）：https://www.geonames.org/
- ConceptNet 官方文档（常识图谱与数据格式）：https://conceptnet.io/
- OpenStreetMap 官方文档（ODbL 许可与数据使用）：https://www.openstreetmap.org/
