---
description: "Free observability quotas: Sentry Developer 5k errors/month for one user, Grafana Cloud 10k series and 50GB logs with 14-day retention"
描述: "免费监控与可观测额度：错误追踪、日志指标、存活探测各自的上限"
name: "Free Observability"
名称: "免费监控与可观测"
---

# 免费监控与可观测

监控不是一个产品，而是三条互不相干的链路：

- **错误追踪**：捕获异常与堆栈，回答"哪里炸了"。
- **日志与指标**：聚合运行数据，回答"最近在发生什么"。
- **存活探测**：定时访问端点，回答"现在还能访问吗"。

免费额度也按这三条分别给，且限制的维度不同：错误按"事件数"、日志按"摄入量 + 保留天数"、探测按"监控项数量"。

## 错误追踪：Sentry 免费档

Sentry 的 Developer 档是 $0、无期限，但**只给一个人用**：每月 5,000 个错误、500 万 spans、50 次会话回放、5GB 日志、5GB 应用指标、1GB 附件、1 个定时任务监控、1 个 uptime 监控、30 天回看。

它的取舍很关键：免费档**没有按量付费预算**，第 5,001 个错误直接被丢弃，等下个周期重置；也**没有 API 与第三方集成**，告警只能走邮件，接不了 Slack 或群机器人。所以它适合"单人 + 小项目 + 能接受邮件告警"的场景，一旦要多人协作就得升 Team。

## 日志与指标：Grafana Cloud 免费档

Grafana Cloud 的 free 是"永远免费、不用绑卡"，各项上限分别是：**1 万个活跃指标序列**、日志 50GB/月、链路追踪 50GB/月、性能剖析 50GB/月、**保留 14 天**、3 个活跃用户；负载测试 500 虚拟用户小时，合成监控 10 万次 API 测试 + 1 万次浏览器测试。

对个人项目来说 50GB 日志几乎用不完，真正的约束是**14 天保留**和**3 个用户**：出问题超过两周再回头查就没了，团队第四个人进不来。

## 存活探测与自托管

存活探测最省钱的形态是自托管：Uptime Kuma 这类工具没有配额概念，一台 1 核 1G 的小机器就能盯几十个端点，还能自定义通知渠道（这点恰好补上 Sentry 免费档只能发邮件的短板）。

自托管的真实成本是**机器的可用性**：用监控去盯一台服务器，那台服务器挂了监控也就跟着哑了。所以"监控别人"的服务最好放在另一台机器或另一家云上，别和被监控对象同生共死。

## 怎么选

| 场景 | 组合 |
|---|---|
| 单人、单机 Agent | Sentry 免费档接异常 + Uptime Kuma 盯存活 |
| 多服务、要看日志与指标 | Grafana Cloud free（14 天保留够排障） |
| 要多人协作、要群告警 | Sentry 升 Team，或 Grafana 付费档 |
| 只在局域网/内网 | 全自托管（Sentry、Loki、Uptime Kuma 都开源） |

## 四个坑

1. **超量直接丢**：Sentry 免费档没有溢出预算，超出的事件不落库，排查时会出现"明明报错了却看不到"。
2. **保留期短**：Grafana 14 天、Sentry 30 天，跨月复盘基本无据可查，重要指标要自己另存。
3. **用户数比额度更硬**：Sentry 1 人、Grafana 3 人，团队一扩就撞墙。
4. **自托管不是零成本**：软件免费，机器、磁盘、备份、以及"监控与被监控同机"的可靠性问题都要自己承担。

## 一句话主线

免费可观测的正确用法是**"错误用托管、日志用托管、存活用自建"**：托管服务吃掉存储与查询的复杂度，自建只承担最轻的探测，既不超额也不失明。

## 参考资料

- Sentry 定价（Developer 免费档：1 用户、5k 错误、5GB 日志、50 回放、30 天）：https://sentry.io/pricing/?gad_source=1
- Sentry 免费档实测说明（无 PAYG 预算、超量丢弃、无第三方集成、30 天回看）：https://maple.dev/ja/guides/sentry-pricing/
- Grafana Cloud 定价（10k 活跃序列、50GB 日志、14 天保留、3 用户）：https://grafana.com/pricing/?pg=grafana-vs-arize
- Grafana Cloud 免费档汇总（日志/追踪/剖析各 50GB、k6 500 VUh、前端 25 万会话）：https://grafana.com/get/?cta=downloads
- Grafana 部署方式（自托管与 Cloud 的能力对照）：https://grafana.com/grafana/deployment-options/
