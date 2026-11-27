---
description: "Cloudflare free tier: Workers 100k requests/day, D1 5GB, R2 10GB with free egress, 10k Neurons/day, and Tunnel's inbound-free reverse proxy"
描述: "Cloudflare 免费档的额度边界：计算、数据、存储、队列、边缘 AI 与内网穿透"
name: "Cloudflare Free Tier"
名称: "Cloudflare 免费档"
---

# Cloudflare 免费档

Cloudflare 的免费不是"试用一个月"，而是**长期存在的 Free 计划**：一个账号同时拿到 CDN/WAF、Workers 计算、SQLite 数据库、对象存储、消息队列、边缘 AI，以及一条把内网服务暴露到公网的反向隧道。不需要绑卡，额度按日或按月重置。

它的价值不在单项额度大，而在**这些额度能拼成一个端到端可跑的小系统**：域名解析、静态资源、接口、数据库、文件、定时任务、甚至模型推理都在同一家，省掉跨云拼接的凭证与网络成本。

## 额度总表

| 能力 | 免费额度 | 重置/限制 |
|---|---|---|
| Workers 计算 | 10 万请求/天，单次 CPU 10 毫秒 | 每日 UTC 00:00 重置，超限返回错误码 1027 |
| Workers 其他硬顶 | 100 个 Worker、5 个 Cron 触发器、单请求 50 个子请求 | 单 Worker 体积 64 MiB、启动 1 秒 |
| KV | 存 1 GB；读 10 万/天，写/删/列各 1,000/天 | 按日重置，写额度最紧 |
| D1（SQLite） | 存 5 GB 总量；读 500 万行/天，写 10 万行/天；10 个库 | 单库上限 500 MB，Time Travel 保留 7 天 |
| R2（对象存储） | 存 10 GB/月；A 类 100 万、B 类 1,000 万/月；**出网不计费** | 仅标准存储，低频存储不在免费档 |
| Queues | 1 万操作/天（一条消息约 3 次操作） | 消息最多保留 24 小时，不可配置 |
| Workers AI | 1 万 Neurons/天 | 约合 0.11 美元，50+ 模型，按模型折算 |
| Zero Trust / Access | 50 用户 | 用于给隧道和内部应用加登录门 |
| TURN / SFU | 1,000 GB 出网/月 | WebRTC 实时音视频 |

## 三个最值钱的额度

**R2 的出网免费**比它那 10 GB 存储重要得多。对象存储的账单通常死在流量上：图片、模型权重、数据集被反复拉取，出网费能超过存储费十倍。R2 把出网归零，等于给了你一个可以放心当图床和制品库的桶。

**D1 的 5 GB SQLite** 对个人项目是够用的关系库：会话记录、任务台账、抓取结果都能塞进去，不用自己维护 Postgres。代价是单库 500 MB、单条 SQL 10 万字节、单查询结果 50 MB，适合"多张小表"而不是"一张巨表"。

**Workers AI 每天 1 万 Neurons** 覆盖的不只是对话模型，文生图与向量化模型也按 Neuron 计价，每天归零。把嵌入计算放在这里，比申请一家"送 token"的平台更省心，因为额度是天天回血的。

## Cloudflare Tunnel：把内网服务挂到公网

这是免费档里最像"基础设施"的一项：本机或内网跑着服务，`cloudflared` 从内部主动向外建立一条加密长连接，Cloudflare 边缘把公网请求顺着这条连接回送到你的机器。**路由器不用开任何入站端口，本机 IP 不外露**，等于反向代理 + 内网穿透 + 自动 HTTPS 三合一。

它有两种用法，免费范围不同：

- **Quick Tunnel（免账号）**：一条命令 `cloudflared tunnel --url http://localhost:8080`，几秒内拿到一个随机 `trycloudflare.com` 子域名。不需要账号、不需要域名、不需要 DNS 记录，适合把本地预览、Webhook 回调地址、Agent 跑出来的页面临时给别人看。加了 `--allowed-mail` 还能要求访客邮箱验证，这个也是免费的。
- **正式 Tunnel（需账号 + 域名）**：域名托管在 Cloudflare DNS 后，可以绑定固定主机名、配 Access 登录策略、跑多个副本。每个账号**自带 1,000 条隧道**不收费，每条隧道默认 25 个副本；超出按 4.50 美元/条/月。隧道本身不按流量计费。

## Tunnel 的免费边界

- Quick Tunnel 单条同时处理 **200 个在途请求**，超了直接 429；不支持 Server-Sent Events，流式接口会断。
- Quick Tunnel **没有可用性承诺**，进程一停 URL 就失效，每次重建子域名都会变——不能拿它当生产入口。
- 正式 Tunnel 的前提是**域名在 Cloudflare DNS 里**；没有域名，就只能用 Quick Tunnel 的随机地址。
- 隧道数按"存在即计数"，停用但没删的隧道也占名额，清理时要真删。

## 三个容易撞墙的地方

1. **KV 的写额度**：读 10 万/天、写 1,000/天，差两个数量级。任何"每次请求都回写缓存"的写法都会在半天内打满；要持久化状态，优先 D1 或 R2。
2. **Workers 的 10 毫秒 CPU**：这是 CPU 时间不是墙钟时间，但大 JSON 解析、正则回溯、同步循环照样能烧穿；重活拆到 Queues 消费者或外部服务。
3. **Queues 的 24 小时保留**：免费档不是持久队列，进程崩溃期间的消息会过期，需要可靠投递就得在 D1 里记状态自己补。

## 一句话主线

Cloudflare 免费档的定位是**"一个人的全栈底座"**：够跑通从域名到数据库到推理再到内网穿透的整条链路，瓶颈集中在写入频次、CPU 时间和队列可靠性这三处，而不是总量。

## 参考资料

- Cloudflare 定价页（Workers AI 10,000 Neurons/天、KV、R2、TURN 免费额度）：https://www.cloudflare.com/plans/
- Workers 限额（10 万请求/天、CPU 10ms、子请求 50、Cron 5 个）：https://developers.cloudflare.com/workers/platform/limits/#worker-size
- Workers 与 D1 计价（D1 每日行读写与 5GB 存储）：https://developers.cloudflare.com/workers/platform/pricing/
- D1 限额（单库 500MB、10 个库、Time Travel 7 天）：https://developers.cloudflare.com/d1/platform/limits/
- R2 计价与免费档（10GB/月、A 类 100 万、B 类 1,000 万、出网免费）：https://developers.cloudflare.com/r2/pricing/
- Queues 计价（免费 1 万操作/天、保留 24 小时）：https://developers.cloudflare.com/workers/platform/pricing/
- Quick Tunnel 文档（免账号、200 在途请求、不支持 SSE、无可用性承诺）：https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/
- Quick Tunnel 限制说明与错误码 429：https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/
- Tunnels for Platforms（每账号 1,000 条隧道免费、超出 4.50 美元/条/月）：https://developers.cloudflare.com/tunnel/features/tunnels-for-platforms/
- Cloudflare 博客：Quick Tunnel 的邮箱保护（--allowed-mail 免费）：https://blog.cloudflare.com/protected-quick-tunnels/
