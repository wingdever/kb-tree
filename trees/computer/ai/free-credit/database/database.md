---
description: "Free database and cache quotas: Supabase 500MB, Neon 100 CU-hours, Turso 5GB, Firestore 1GiB, Atlas 512MB, Upstash 250MB"
描述: "免费数据库与缓存的额度边界：Postgres、SQLite、文档库、Redis 各自怎么计费"
name: "Free Databases & Cache"
名称: "免费数据库与缓存"
---

# 免费数据库与缓存

数据库的免费额度不能只看"给多少 GB"，要先看它**按什么计费**，因为计费模型决定了"闲置要不要钱"：

- **按存储计**：只算占了多少空间，闲置不花钱。文档库、SQLite 托管多是这种。
- **按计算时长计**：算"计算单元 × 小时"（CU-hours），闲置会缩零就几乎不花钱，不缩零就一直烧。
- **按请求计**：算行读取数、命令执行数，查询多就算得多，与数据量无关。

同一个 "free" 标签下，这三类的实际可用量能差一个数量级。

## Postgres：两家的免费档思路不同

**Supabase** 卖的是"全家桶"：500MB 数据库 / 项目、50,000 月活用户、5GB 出网 + 5GB 缓存出网、1GB 文件存储、最多 2 个活跃项目、25 个 Edge Functions。它的关键条款是**项目闲置 1 周自动暂停**，要手动恢复；暂停的项目不计入 2 个项目上限。数据库 500MB 是按项目算，不是按账号算。

**Neon** 卖的是"纯 Postgres + 分支"：100 个项目、每项目 10 个分支、每项目 1GB 存储（全账号合计上限 20GB）、每项目每月 100 CU-hours 计算、5GB 公网传输。0.25 CU 跑 400 小时差不多就是 100 CU-hours，所以"每天跑十来个小时"的小应用能长期留在免费档；闲置 5 分钟自动缩零，且**不能关掉**。

一句话：要 Auth、存储、函数一整套，选 Supabase，但得接受闲置暂停；只要一个干净的 Postgres 加分支做迁移测试，选 Neon，计算额度按项目独立发。

## SQLite 托管：按行计费

**Turso** 的免费档给 100 个数据库、5GB 存储、每月 5 亿行读、1,000 万行写、3GB 同步、1 天时间点恢复。SQLite 库是"一个文件"，所以闲置库只占存储、不占计算，很适合"一用户一库/一 Agent 一库"的多租户结构。

注意口径冲突：定价页写 100 个库，对比页写 500 个，接入前以定价页和控制台实际显示为准。

## 文档库与 KV

**Firestore（Spark 档）**：1 GiB 存储、每天 5 万次文档读、2 万次写、2 万次删、每月 10 GiB 出网。配额按**美国太平洋时间零点**重置，且**每个项目只有一个库能享免费配额**，第二个库开始直接计费。

**MongoDB Atlas 免费集群（M0）**：512MB 存储（含索引的未压缩 BSON 字节）、每 7 天滚动周期 10GB 入 / 10GB 出、排序内存 32MB、每个项目只能有 1 个免费集群。512MB 是硬顶，到了就只能升配或删数据。

## 缓存：Redis 的免费档最小

**Upstash Redis** 免费档：250MB 数据、每月 50 万条命令、10GB 带宽、单账号 1 个数据库。这里有个容易被旧文章误导的点：早期文档写的是"每天 1 万条命令"，现行定价口径已改成"**每月 50 万条**"——按天算反而更少，别看错版本。

自建 Redis、PocketBase、Postgres 当然"软件免费"，但要一台常开的机器，真正的成本是服务器而不是数据库。免费托管的价值就在于把这台机器省掉。

## 按用途选

| 用途 | 首选 | 理由 |
|---|---|---|
| 带登录的小应用 | Supabase | Auth + 存储 + 函数一套，50,000 MAU 够用 |
| 纯 Postgres、要分支 | Neon | 每项目独立 100 CU-hours，缩零不烧钱 |
| 一用户一库 / 边缘读 | Turso | 库是文件，闲置只占存储 |
| 客户端直连、实时同步 | Firestore | 免费额度按天发，SDK 直连 |
| 文档型、要跑聚合 | Atlas | 512MB 够验证 schema |
| 缓存 / 限流 / 队列 | Upstash | 50 万命令/月，按请求计 |

## 五个坑

1. **闲置会暂停或缩零**：Supabase 一周不活跃就暂停，Neon 5 分钟缩零。演示前记得先唤醒，别在客户面前等冷启动。
2. **额度按项目不按账号**：Supabase 500MB/项目、Neon 1GB/项目，但 Neon 全账号存储合计封顶 20GB——多开项目不一定能多用。
3. **出网另算**：Supabase 5GB + 5GB 缓存、Neon 5GB、Atlas 每 7 天 10GB，数据被频繁拉取时先撞的是流量不是容量。
4. **免费配额只给一个库**：Firestore 与 Atlas 都是"每项目一个库/集群享免费"，第二个开始计费。
5. **口径会变**：Upstash 从"每天 1 万命令"改成"每月 50 万"，Turso 的库数在不同页面写 100 与 500。以定价页为准，别信二手教程。

## 一句话主线

免费数据库的可用量由**计费模型**决定而不是由 GB 数决定：按存储计的适合放大文件，按计算计的适合低频应用，按请求计的适合小额高频缓存；选之前先问"我的负载是闲置多、查询多，还是写入多"。

## 参考资料

- Supabase 定价（500MB/项目、5GB 出网、1GB 存储、2 个活跃项目、1 周闲置暂停）：https://supabase.com/pricing?id=12
- Supabase 计费文档（各档配额、按项目计数据库大小）：https://supabase.com/docs/guides/platform/billing-on-supabase
- Supabase 带宽说明（免费档 5GB + 5GB 缓存出网）：https://supabase.com/docs/guides/storage/serving/bandwidth
- Neon 免费档 FAQ（100 项目、1GB/项目、100 CU-hours、5 分钟缩零、5GB 传输）：https://neon.com/faqs/free-plan-limits-and-quotas
- Turso 定价（100 库、5GB、5 亿行读、1,000 万行写、1 天 PITR）：https://turso.tech/pricing?frequency=monthly
- Turso 对比页（另一处写免费档 500 库，口径冲突）：https://turso.tech/comparisons/neon
- Firestore 配额（1 GiB、5 万读/2 万写/天、10 GiB 出网、太平洋时间重置）：https://firebase.google.cn/docs/firestore/quotas?hl=zh-cn
- MongoDB Atlas 免费集群限制（512MB 存储、10GB 入/出、32MB 排序、每项目 1 个）：https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/
- Upstash Redis 定价（250MB、50 万命令/月、10GB 带宽、1 个库）：https://upstash.com/pricing/redis
- Upstash 旧版文档（“每天 1 万命令、256MB”的旧口径）：https://docs.upstash.com/redis/overall/pricing
