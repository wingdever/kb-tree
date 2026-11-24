---
description: "RabbitMQ transport: AMQP broker with exchange routing, delivery acknowledgements, retries, dead-letter queues and durable messages"
描述: "RabbitMQ 传输：AMQP 代理，含 exchange 路由、送达确认、重试、死信队列与持久消息"
name: "RabbitMQ Transport"
名称: "RabbitMQ 传输"
---

# RabbitMQ 传输（RabbitMQ Transport）

> 来源：RabbitMQ 官方文档与 NestJS 官方微服务文档。配置项与版本变化快，以官方文档为准。

RabbitMQ 是基于 AMQP 的消息代理，在 NestJS 中以 RMQ transporter 接入。它适合需要复杂路由、可靠投递与失败隔离的场景。

## 核心特性

- **exchange / queue 路由**：消息先到 exchange，再按绑定规则投递到队列，支持直接、主题、扇出等多种路由。
- **送达确认与持久化**：生产者确认、消费者 ACK、消息与队列持久化，保证崩溃后消息仍存活。
- **重试与死信队列**：失败消息可重试，超限后进入死信队列供排查，而不是无限重投。
- **队列组语义**：多个消费者竞争同一队列，天然形成实例间负载均衡。
- **元数据**：作为 message headers 传递；`getMetadata()` 只返回单字符串值，其余用 `getMessage()` 读。record 级 header（`RmqRecordBuilder`）覆盖同名 metadata。

## 适用与边界

- 适合对可靠性、路由灵活性与失败隔离要求高的业务消息。
- 运维一个 broker  cluster 有成本；简单内部调用用它偏重。
- 不追求 Kafka 式的日志重放与超大规模流处理。

## 常见失败模式

- 消费者自动 ACK，处理失败却已确认，消息丢失。
- 无死信队列，毒消息反复重投堵塞队列。
- exchange 与 binding 设计混乱，路由不可预测。
- 队列无界增长，积压最终压垮 broker。
- 把 RabbitMQ 当 RPC 用，忽略请求响应超时与关联 ID。
