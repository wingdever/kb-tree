---
description: "Redis transport: pub/sub and stream based messaging with channel routing, fixed JSON packet shape and metadata field"
描述: "Redis 传输：基于发布订阅与流的消息、channel 路由、固定 JSON 包与 metadata 字段"
name: "Redis Transport"
名称: "Redis 传输"
---

# Redis 传输（Redis Transport）

> 来源：Redis 官方文档与 NestJS 官方微服务文档。配置项与版本变化快，以官方文档为准。

Redis 传输借 Redis 的发布/订阅或 Stream 在微服务间传消息。在 NestJS 中它是内置 transporter 之一；如果系统已在用 Redis，用它承载轻量事件可以避免再运维一套 broker。

## 核心特性

- **channel 路由**：Redis 上由 **channel** 选择 handler，而不是消息里的 `pattern` 字段。请求 `sum` 发到 `sum` channel，回执走 `sum.reply`；对象 pattern 用其 route 作 channel 名。
- **固定包形状**：包以纯 JSON 文本发布，形状固定，因此非 Nest 系统也能调用 handler 并应答。
- **metadata 字段**：客户端附加的 metadata 作为 packet 的 `metadata` 字段（字符串值记录）传递，不进业务 payload。
- **部署简单**：复用现有 Redis，无需独立消息集群。

## 适用与边界

- 适合轻量事件分发、已有 Redis 的团队、低到中等消息量。
- pub/sub 是即发即弃，无持久化与重放；需要可靠队列时用 Redis Stream 或换 RabbitMQ / Kafka。
- channel 模型与 pattern 模型的对应关系需明确，否则 handler 静默失配。

## 常见失败模式

- 把 pub/sub 当可靠队列，消费者下线期间消息丢失。
- 混淆 channel 与 pattern，以为 pattern 字段决定路由。
- 单个 Redis 同时承担缓存、会话与消息，负载互相干扰。
- 消息体过大，拖慢 Redis 并影响缓存命中延迟。
