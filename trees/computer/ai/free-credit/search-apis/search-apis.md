---
description: "Free search API quotas: Algolia Free 10K requests and 50K records, Typesense 720 trial hours, Meilisearch self-hosted forever free"
描述: "免费搜索 API 的额度：请求数、记录数、索引更新次数三种计量"
name: "Free Search APIs"
名称: "免费搜索 API"
---

# 免费搜索 API

搜索服务的免费额度按三种东西计量，缺一项就会误判：

- **请求数**：每月能搜多少次。
- **记录数**：索引里能放多少条文档，且单条有大小上限。
- **索引更新次数**：能改多少次数据，这一项最容易被忽略。

很多"免费搜索"其实不是长期免费，而是**一次性试用**：给一段集群时长，用完就转付费。区分"永久免费档"和"试用额度"是选型第一步。

## 有长期免费档的：Algolia

Algolia 的 Free 是明确写着"无需信用卡"的长期档：**每月 1 万次搜索请求、5 万条记录、5,000 次推荐请求、5,000 次抓取**<RichMediaReference>["https://www.algolia.com/pricing"]</RichMediaReference>。

条款里有几条硬限制：单条记录最大 **10 KB**、单个应用最大 **1 GB**、单个索引最大 **1 GB**、**每个账号只能有 1 个应用**；账号 **30 天不活跃可能被删除数据**，超出用量时服务会被挂起或在搜索结果里插入品牌标识<RichMediaReference>["https://www.algolia.com/policies/free-plan-details"]</RichMediaReference>。

记录数存在口径冲突：定价页写 50,000，部分 FAQ 写 Build 档 100 万条、Grow 档 10 万条。差异来自"Build（开发档）"与"Grow（上线档）"的免费层不同，接入前看自己账号的实际配额页。

## 只有试用额度的：Meilisearch 与 Typesense

这两家都开源，但**托管版没有长期免费档**：

- **Meilisearch Cloud**：只有 **14 天试用**、不用绑卡，之后 $20/月起（XS 实例 0.5 vCPU / 1GB RAM / 32 GiB 磁盘）<RichMediaReference>["https://www.meilisearch.com/pricing"]</RichMediaReference>。开源引擎 MIT 许可，**自托管永久免费、无用量上限**。
- **Typesense Cloud**：新用户给 **720 小时集群时长 + 10GB 带宽**，按连续运行折算约 30 天，属于一次性试用<RichMediaReference>["https://www.meilisearch.com/blog/typesense-pricing"]</RichMediaReference>。开源版同样可自托管。

结论很直接：想长期免费，就别用它们的云，用它们的二进制。

## 内容源与全网搜索 API

上面几家解决的是"给自己的数据建索引"，另一类是"直接搜别人已经建好的索引"，常见于 Agent 的联网检索：

- **知乎开放平台**：同时提供"知乎搜索"与"全网搜索"两个接口，各自 **5,000 次/天**，额度按日、北京零点重置、九类接口分池不互通；前者只检索知乎站内内容，后者覆盖公开网页。它把"中文长尾经验"和"网页检索"放在同一套鉴权下，是中文场景里比较少见的一档。
- **Brave Search API**：独立索引、不依赖第三方搜索引擎。免费档 **2,000 次/月、1 次/秒限速**；另一套更常见的口径是"每个套餐每月 $5 抵用额，按 $5/千次折算约 1,000 次"，两种说法目前并存，接入前看控制台<RichMediaReference>["https://brave.com/learn/index.xml"]</RichMediaReference>。注意**注册需要绑卡**，但可以把用量上限设为免费额度，做到不产生扣费；官方也提示免费层存在取消的可能（文中提到 2027-01-01 这个时间点）。
- **Tavily**：面向 Agent 的搜索接口，免费档 **每月 1,000 credits**，不用绑卡；Basic Search 每次 1 credit、Advanced 2 credits、Extract 每 5 个成功 URL 收 1 credit，失败不计费<RichMediaReference>["https://docs.tavily.com/documentation/api-credits?ref=apidog.com"]</RichMediaReference>。它还提供**免密钥（keyless）调用**，无需注册即可限量试用，额度用尽后再换 API key。

这三家的共同点：额度按"次/天"或"credit/月"发，**比自建索引便宜，但结果不可控**——排序、收录范围、时效都由平台决定，且随时可能改条款。

## 轻量托管：Orama Cloud

Orama 的核心库是 Apache-2.0，可嵌在浏览器、服务端或边缘函数里，**库本身不计费**。Cloud 版有一个免费额度：**最多 3 个索引、每索引 10 万文档、每月 150 次索引更新**——最后这个数字是全表最紧的，基本上只够"文档站偶尔同步"<RichMediaReference>["https://www.exploreai.directory/open-source-alternatives/orama"]</RichMediaReference>。该额度来自第三方整理，接入前请核对官方页。

## 真正的零成本方案

三种做法，按数据量从小到大：

1. **数据库自带检索**：Postgres 的 `tsvector` 全文检索、SQLite 的 FTS5、或 pgvector 做语义召回——数据本来就在库里，增量成本为 0。
2. **自托管单二进制**：Meilisearch、Typesense 都是单文件可执行，一台 1 核 1G 机器能撑中小型站点，没有请求数上限。
3. **边缘函数内嵌**：Orama 的库可以直接跑在 Worker 里，索引随代码发布，没有独立服务。

只有当"搜索质量与运维成本"大于"自己搭"的代价时，才值得换托管。

## 怎么选

| 场景 | 方案 |
|---|---|
| 文档站/博客站内搜索 | 数据库全文检索，或自托管 Meilisearch |
| Agent 要联网检索 | 知乎全网搜索（5,000/天）或 Tavily（1,000 credit/月） |
| 要即时搜索、容错、分面 | Algolia Free（1 万请求/月，注意 1 个应用） |
| 要独立网页索引 | Brave Search API（2,000 次/月，需绑卡设上限） |
| 想先试托管再决定 | Meilisearch 14 天试用 / Typesense 720 小时 |
| 边缘部署、无独立服务 | Orama 库内嵌或 Orama Cloud 免费档 |

## 四个坑

1. **"免费"可能是一次性试用**：Typesense 的 720 小时是总量，不是每月重置。
2. **记录数受单条大小限制**：Algolia 单条 10 KB，长文档要先切片，否则一条就顶十几条配额。
3. **索引更新单独计**：Orama 每月 150 次更新，写多读少的场景会先撞这一项。
4. **免费档会挂起或加标识**：Algolia 超限会挂起服务或插入品牌标识，30 天不活跃还可能清数据。

## 一句话主线

免费搜索 API 的额度是**"请求数 × 记录数 × 更新次数"的三重约束**：自己建索引的长期免费档只有 Algolia 明确，Meilisearch 与 Typesense 的云版都是一次性试用；而"搜别人索引"的知乎、Brave、Tavily 反而都有按天或按月的免费额度，代价是结果不可控。数据量小时优先用数据库自带检索或自托管单二进制，把托管留给"真的要质量"的场景。

## 参考资料

- Algolia 定价（Free：每月 1 万请求、5 万记录、5,000 推荐、5,000 抓取）：https://www.algolia.com/pricing
- Algolia 免费档条款（单条 10KB、单应用 1GB、单索引 1GB、1 个应用、30 天不活跃删数据）：https://www.algolia.com/policies/free-plan-details
- Algolia Grow/免费层说明（Build 100 万条、Grow 10 万条的口径差异）：https://www.algolia.com/fr/pricing
- Meilisearch 定价（Cloud $20 起、14 天试用、自托管 MIT 免费）：https://www.meilisearch.com/pricing
- Typesense 免费额度（720 小时集群 + 10GB 带宽，约 30 天）：https://www.meilisearch.com/blog/typesense-pricing
- Orama Cloud 免费额度（3 索引、每索引 10 万文档、每月 150 次更新，第三方整理）：https://www.exploreai.directory/open-source-alternatives/orama
- Orama 开源库（Apache-2.0、可嵌浏览器/服务端/边缘）：https://www.fumadocs.dev/docs/headless/search/orama-cloud
- 知乎开放平台额度（知乎搜索与全网搜索各 5,000 次/天，按日重置、分池）：https://developer.zhihu.com/docs/quota
- Brave Search API 免费档（2,000 次/月、1 次/秒；另见每套餐每月 $5 抵用额口径）：https://brave.com/learn/index.xml
- Brave 社区答复（$5/月免费抵用额需绑卡、可设用量上限）：https://community.brave.app/t/clarification-about-search-api-free-monthly-credits/656627
- Tavily 免费额度与 credit 计费（1,000/月、Basic 1 credit、Extract 每 5 URL 1 credit）：https://docs.tavily.com/documentation/api-credits
- Tavily 免密钥试用（keyless 限量、无需注册）：https://docs.tavily.com/documentation/keyless
