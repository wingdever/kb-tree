---
description: "NATS transport: lightweight messaging with core request-response, JetStream persistence, wildcard subjects and header metadata"
描述: "NATS 传输：轻量消息系统，核心请求响应、JetStream 持久化、通配符主题与头部元数据"
name: "NATS Transport"
名称: "NATS 传输"
---

# NATS 传输（NATS Transport）

NATS 是轻量消息系统，在 NestJS 中是内置 transporter 之一。它用主题（subject）路由，核心价值是"少运维"——不需要 Consul、etcd 或服务网格即可做服务间发现与通信。

## 核心特性

- **请求响应原生支持**：底层天然提供请求响应所需的双通道，无需框架补建。
- **通配符订阅**：如 `time.us.*`，可用 `NatsContext` 读取生产者发送的真实 subject。
- **JetStream 持久化**：在 Core NATS 的即发即弃之上提供持久化、重放与流能力。
- **队列组**：同一服务的多个实例加入同一队列组，由 broker 侧分摊消息，形成实例间负载均衡。
- **元数据**：correlation id 等作为 message headers 传递；`getMetadata()` 只返回单字符串值，其余用 `getHeaders()` 读。

## 适用与边界

- 适合微服务消息骨干、需要轻量部署与请求响应/事件并存的场景。
- Core NATS 默认即发即弃；要持久化与重放需 JetStream。
- 多语言参与需实现 NATS 协议；NestJS 侧有 NatsContext、wildcard 等一等支持。

## 常见失败模式

- 以为所有 NATS 消息都持久，未启用 JetStream 却期望重放。
- 通配符订阅过宽，收到大量无关消息。
- 把 metadata 放进 payload，污染业务消息。
- 队列组名配置不一致，导致消息只被单一实例消费。

## 参考资料

- NATS 文档：https://docs.nats.io
- NestJS 微服务文档：https://docs.nestjs.com/microservices/basics
