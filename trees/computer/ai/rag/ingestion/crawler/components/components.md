---
description: "Crawler system components and common engineering choices across scheduling, fetching, parsing, storage and operations"
描述: "爬虫系统构成与各环节常用工程选型：调度、抓取、解析、去重、存储与运维"
name: "Crawler Components and Stack"
名称: "爬虫构成与工程选型"
---

# 爬虫系统构成与工程选型

爬虫不是一个“发请求的脚本”，而是一套由发现、调度、抓取、解析、去重、存储与运维组成的系统。工程选型的分歧通常不在算法，而在规模：单机能跑通的，不必先上分布式；只抓几个页面的，不必先上框架。

## 六个核心环节

| 环节 | 做什么 | 常见工程选项 |
|---|---|---|
| **URL 发现与调度** | 从种子、sitemap、RSS、链接里得到候选 URL，排优先级、控制重抓 | 单机用 Scrapy Scheduler；分布式用 Redis（如 Scrapy-Redis）；超大规模 URL 流用 Kafka |
| **抓取 / Downloader** | 发 HTTP 请求、处理状态码、重试、会话、压缩 | 同步用 requests；异步用 httpx / aiohttp；框架内用 Scrapy Downloader |
| **渲染** | 执行 JavaScript，拿到浏览器里的 DOM | Playwright 最常用；Puppeteer 在 Node 生态常见；Selenium 更偏老项目 |
| **解析 / 抽取** | HTML 转 DOM，抽正文、字段、链接 | lxml / parsel 快且主流；BeautifulSoup 容错好、上手快；正文抽取常用 trafilatura / readability-lxml |
| **URL 与内容去重** | 同一页多个 URL、同一内容多个版本合并 | URL 规范化 + SHA-256 精确哈希；近重复用 SimHash / MinHash；海量 URL 集合用 Redis Set / Bloom Filter |
| **限速与合规** | robots、每站并发、退避、条款与版权 | Protego / urllib.robotparser 解析 robots；每站用 token bucket；Scrapy 用 AutoThrottle + DOWNLOAD_DELAY |

## 三个支撑环节

| 环节 | 做什么 | 常见工程选项 |
|---|---|---|
| **管道与存储** | 清洗、校验、写库、保留版本 | 原始 HTML 放 S3 / MinIO；元数据放 PostgreSQL；全文检索放 OpenSearch / Elasticsearch；批处理放 Parquet |
| **监控** | 成功率、429/403、队列深度、重复率、延迟 | Prometheus + Grafana；日志用 Loki / ELK；异常用 Sentry |
| **分布式协调** | 多 worker 分片、租约、失败重投 | Redis 最常见；Kafka 适合高吞吐 URL 流；RabbitMQ 适合任务队列 |

## 按规模选型

- **小规模**：`requests + BeautifulSoup + PostgreSQL + cron`，够用且简单。
- **中规模**：`Scrapy + Redis + PostgreSQL + S3/MinIO`，调度、去重、限速、管道都有现成件。
- **大规模**：`Kafka/Redis + 多 worker + 对象存储 + OpenSearch + Prometheus`，重点转向分片、背压与可观测性。

## 选型判断

1. **先定规模与预算**。每天几千页和每天几千万页，选型完全不同；不要用大规模方案解决小规模问题。
2. **渲染只给必要页面**。静态 HTML 与公开接口优先；全站上无头浏览器会把成本抬高一个数量级。
3. **存储分层**。原始响应、解析结果、检索索引分开存；否则解析器升级或索引重建时只能重抓。
4. **队列先单机后分布式**。单机队列能撑住就不要引入跨机协调；分布式会带来租约、重复与背压问题。
5. **合规先于技术**。robots、条款、版权与个人信息决定“能不能抓”，技术只决定“抓得快不快”。

## 常见误判

- **把 Scrapy 当成全部**。Scrapy 串起调度、下载、解析与管道，但不替代 URL 规范化、内容去重与合规判断。
- **把 BeautifulSoup 当成爬虫**。它只负责解析，不负责请求、渲染与调度。
- **一上来就分布式**。没有单机基线，分布式只会把重复抓取与限速问题放大。
- **只堆代理池**。代理池不是合规方案；遇到访问限制应走官方 API、授权或降低频率。
- **只看抓取量**。页面数增长可能只是重复与模板页增长；要看可检索的干净文本。

## 一句话主线

爬虫由发现调度、抓取、渲染、解析、去重、限速、存储与监控组成；选型按规模与合规约束走，单机能解决就不上分布式，渲染只给必要页面，存储分层，抓取量不等于数据质量。

## 参考资料

- Scrapy 2.x 官方文档（架构与组件）：https://docs.scrapy.org/en/latest/topics/architecture.html
- Redis 官方文档（集合、有序集合与队列）：https://redis.io/docs/latest/
- Apache Kafka 官方文档（高吞吐 URL 流与分区）：https://kafka.apache.org/documentation/
- Playwright 官方文档（浏览器渲染与网络拦截）：https://playwright.dev/docs/
- OpenSearch 官方文档（全文检索与索引）：https://docs.opensearch.org/
