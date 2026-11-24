---
description: "Kafka transport: distributed log with partitions, high throughput, replayability and event-oriented messaging"
描述: "Kafka 传输：分布式日志，含分区、高吞吐、可重放与事件导向的消息模型"
name: "Kafka Transport"
名称: "Kafka 传输"
---

# Kafka 传输（Kafka Transport）

Kafka 是分布式日志/流平台，在 NestJS 中是内置 transporter 之一。与队列式 broker 不同，它以**追加日志**为中心：消息按分区持久化、可被多个消费者组独立读取与重放。

## 核心特性

- **分区与并行**：主题分为多个分区，分区内有序，不同分区可并行消费，吞吐水平扩展。
- **消费者组**：同组实例分摊分区，形成负载均衡；不同组各自读取全量日志。
- **持久化与重放**：消息按保留策略留存，可从任意 offset 重读，适合事件溯源、审计与回放。
- **事件导向**：官方明确指出 Kafka 这类基于日志持久化的流平台更契合事件消息范式，而非请求响应。
- **元数据**：作为 message headers 传递；`getMetadata()` 只返回单字符串值，其余用 `getMessage()` 读。

## 适用与边界

- 高吞吐事件流、日志聚合、需要回放与多消费者独立读取的场景。
- 请求响应需自行实现（关联 ID + 回复主题）或改用其他传输层。
- 分区数决定并行上限，分区键决定局部顺序，设计错误会造成热点或顺序错乱。
- 运维成本高于轻量 broker。

## 常见失败模式

- 用 Kafka 做同步 RPC，引入不必要的延迟与复杂度。
- 分区键选择不当导致热点，或错误假设全局有序。
- 消费者处理非幂等却开启自动提交，重放时重复生效。
- 忽略消费者组 rebalance，处理中被迫中断。
- 把消息保留期当长期存储，超出后被清理造成数据丢失。

## 参考资料

- Kafka 文档：https://kafka.apache.org/documentation/
- NestJS 微服务文档：https://docs.nestjs.com/microservices/basics
