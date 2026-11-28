---
description: "Scrapy crawler framework: engine, scheduler, downloader, spiders, middlewares and pipelines"
描述: "Scrapy 爬虫框架：引擎、调度器、下载器、Spider、中间件与管道"
name: "Scrapy"
名称: "Scrapy 爬虫框架"
---

# Scrapy

Scrapy 是 Python 的爬虫框架，不只是“请求库 + 解析库”的组合。它把调度、下载、解析、去重、限速与数据管道串成一条可配置的流水线；写爬虫时，主要工作从“管并发和重试”变成“定义 Spider 与规则”。

## 架构与数据流

一次请求在 Scrapy 里大致这样走：

1. **Engine** 从 Spider 取起始请求，交给 Scheduler。
2. **Scheduler** 排队、去重，按优先级把下一个请求交给 Downloader。
3. **Downloader** 发 HTTP 请求，经过下载器中间件，拿到 Response。
4. **Spider** 解析 Response，产出 Item 与新 Request；新 Request 回到 Scheduler。
5. **Item Pipeline** 清洗、校验、去重、写库；Engine 在适当时候关闭。

下载器中间件处理请求/响应与异常；Spider 中间件处理 Spider 的输入输出。它们适合放通用逻辑，不要把业务判断塞进中间件。

## 一个项目里放什么

- `spiders/`：每个站点或一类站点一个 Spider，定义起始 URL 与解析规则。
- `items.py`：字段契约；先定字段，再写解析，避免边抓边加字段。
- `pipelines.py`：清洗、校验、去重、存储；多个 Pipeline 按优先级顺序执行。
- `middlewares.py`：请求头、会话、失败处理等横切逻辑。
- `settings.py`：并发、延迟、重试、robots、管道与中间件开关。

> 判断：先把 Item 字段和 Pipeline 契约定清楚，再写 Spider；字段事后补，通常会把清洗逻辑散落在解析函数里。

## 关键设置

| 设置 | 作用 | 建议 |
|---|---|---|
| `ROBOTSTXT_OBEY` | 是否遵守 robots.txt | 生产抓取显式设为 `True` |
| `DOWNLOAD_DELAY` | 同一站点的请求间隔 | 按站点承受度设，不要全局一个值 |
| `CONCURRENT_REQUESTS_PER_DOMAIN` | 单站点并发 | 与延迟一起调，避免打爆单站 |
| `AUTOTHROTTLE_ENABLED` | 自适应限速 | 长尾站点多时开启，减少 429/503 |
| `RETRY_TIMES` | 重试次数 | 只对临时错误重试；403/404 不重试 |
| `ITEM_PIPELINES` | 管道顺序 | 校验在前，存储在最后 |
| `DUPEFILTER_CLASS` | 请求去重 | 默认按请求指纹；URL 规范化仍要自己做 |

Scrapy 的默认去重是请求指纹，不等于 URL 规范化：带跟踪参数、打印版、重定向后的最终 URL，仍可能被当成不同请求。需要在上游做规范化，或在 Pipeline 里补内容去重。

## 解析与跟进

- 用 `response.css()` / `response.xpath()` 抽节点，不要用正则切 HTML。
- 跟进链接用 `response.follow()`，它会处理相对 URL；手拼绝对 URL 容易漏掉 base href。
- 分页、详情页、列表页分开写解析函数；一个 Spider 里堆所有逻辑，规则会互相污染。
- 需要登录态时用 Cookie 中间件或显式会话；不要把个人登录态用于未授权批量抓取。

## 常见坑

- **在 Spider 里写阻塞代码**：`time.sleep()`、同步 `requests` 会卡住 Twisted reactor；用异步延迟或框架提供的下载器。
- **并发开太大**：`CONCURRENT_REQUESTS` 是全局，单站压力要看 `CONCURRENT_REQUESTS_PER_DOMAIN` 与延迟。
- **把 403 当临时错误**：重试只会加重封禁；应停止并检查授权或改用 API。
- **Pipeline 顺序错**：先存储后校验，脏数据已经落库；校验与去重必须排在存储前。
- **只靠默认去重**：URL 参数与重定向造成重复抓取；需要规范化与内容指纹补一层。
- **动态页面硬抓**：Scrapy 默认不执行 JS；需要渲染时接 Playwright/Splash，或直接找接口。

## 什么时候不用 Scrapy

- 只抓几个页面：`requests` + BeautifulSoup 更轻。
- 页面完全依赖 JavaScript：渲染与反爬挑战会让 Scrapy 的默认下载器不适用，先找接口或换浏览器方案。
- 需要大规模分布式：Scrapy 单机够用，跨机要接 Scrapy-Redis 等队列方案，复杂度和运维成本会明显上升。

## 一句话主线

Scrapy 把调度、下载、解析、去重与管道做成一条可配置的流水线；先把 Item 契约、单站限速、robots 与去重定好，再写 Spider，不要把它当成“更快的 requests”。

## 参考资料

- Scrapy 2.x 官方文档（架构与数据流）：https://docs.scrapy.org/en/latest/topics/architecture.html
- Scrapy 2.x 官方文档（设置项参考）：https://docs.scrapy.org/en/latest/topics/settings.html
- Scrapy 2.x 官方文档（Spider 与选择器）：https://docs.scrapy.org/en/latest/topics/spiders.html
