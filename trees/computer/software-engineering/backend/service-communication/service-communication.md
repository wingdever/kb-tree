---
description: "Service communication: transport mechanisms between processes, request-response versus events, brokers and protocol selection"
描述: "服务通信：进程间的传输机制、请求响应与事件、消息代理与协议选型"
name: "Service Communication"
名称: "服务通信"
---

# 服务通信（Service Communication）

> 来源：NestJS 官方微服务文档及各协议官方文档。接口形态与版本变化快，以官方文档为准。

服务通信解决的是**一个请求或事件如何跨进程边界到达另一个服务**。它位于服务治理之下：服务发现决定"发给谁"，传输层决定"怎么发"。同一个微服务框架常把多种传输机制抽象成统一接口，让应用代码在切换传输层时不用改。

## 两种消息风格

- **请求响应（request-response）**：发送方确认消息被接收并等回执，适合需要同步结果的调用。NestJS 为它建立两个逻辑通道——一个传数据、一个等响应；NATS 原生支持双通道，其他传输层由框架补建。
- **事件驱动（event-based）**：发送方发布即可，不等待特定响应。同一事件可有多个消费者，适合解耦、削峰与广播。Kafka、NATS JetStream 这类基于日志持久化的流平台更适合事件范式而非请求响应。

不需要同步结果时优先用事件，省掉双通道开销。

## 七大传输机制

- **TCP**：默认传输层，裸 socket，无 broker，可内建 TLS。
- **gRPC**：HTTP/2 + Protobuf，强类型契约与流式。
- **MQTT**：基于主题的轻量 pub/sub，低带宽、有 QoS 等级。
- **Redis**：借 Redis 的 pub/sub 或 Stream，部署简单。
- **NATS**：轻量消息系统，Core NATS 请求响应、JetStream 持久化。
- **RabbitMQ**：AMQP broker，exchange/queue 路由、送达确认、死信队列。
- **Kafka**：分布式日志，分区、高吞吐、消息可重放。

## 统一抽象的价值

NestJS 的 `ClientProxy` 把各传输层的 `send()`（请求响应）与 `emit()`（事件）统一成同一接口，因此切换 TCP、Redis、NATS 等不改动业务代码。这是框架层面的抽象，不消除底层机制的差异——消息是否持久、是否可重放、投递保证是什么，仍由所选传输层决定。

## 选型判据

- 需要最低延迟的同步内部调用 → gRPC 或 TCP。
- 需要消息不丢、复杂路由与重试 → RabbitMQ。
- 需要高吞吐事件流、回放与审计 → Kafka。
- 需要轻量骨干、不想运维重 broker → NATS。
- 已有 Redis、事件量不大 → Redis。
- 设备、边缘、低带宽场景 → MQTT。
- 同一系统可混用：对外 REST、对内 gRPC、异步走 broker，不必全局统一。

## 共同失败模式

- 把"发Events出去"当成"已被处理"：事件驱动没有回执，消费失败需另行处理。
- 请求响应缺超时与重试预算，慢下游拖垮整条链路。
- 无界队列堆积，最终 OOM 或雪崩。
- 忽略序列化边界：跨语言时长度前缀、编码与 schema 不一致导致静默错位。
- 为简单内部调用引入重型 broker，运维成本超过收益。
