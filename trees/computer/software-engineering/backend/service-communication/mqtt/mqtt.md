---
description: "MQTT transport: lightweight topic-based pub/sub with QoS levels, user properties and edge/IoT orientation"
描述: "MQTT 传输：基于主题的轻量发布订阅、QoS 等级、用户属性与边缘/IoT 场景"
name: "MQTT Transport"
名称: "MQTT 传输"
---

# MQTT 传输（MQTT Transport）

MQTT 是基于主题的轻量发布/订阅协议，最初为低带宽、不稳定网络的设备与边缘场景设计。在 NestJS 中它是内置 transporter 之一；消息按主题路由，发布方只管发，订阅方按主题接收。

## 核心特性

- **主题路由**：用层级主题（如 `sensors/room1/temp`）匹配订阅，支持通配符。
- **QoS 等级**：至多一次、至少一次、恰好一次，按可靠性与开销取舍。
- **轻量开销**：固定头部小，适合低带宽与资源受限设备。
- **保留消息与遗嘱消息**：新订阅者可立即拿到最新状态；客户端异常断线可广播通知。
- **元数据差异**：MQTT 5 用 headers / user properties 传递附加信息；MQTT 3 没有 header 通道，NestJS 的 metadata 不会随其传输。record 级 header（如 `MqttRecordBuilder` 设置）会覆盖同名 metadata。

## 适用与边界

- 适合设备、边缘、移动端等低带宽高延迟网络，以及一对多广播。
- 请求响应需通过成对主题自行约定，不如 NATS / RabbitMQ 原生。
- 消息持久性与重放取决于 broker 与 QoS，不是协议默认保证。

## 常见失败模式

- 在 MQTT 3 上依赖 metadata 传递 correlation id，结果静默丢失。
- 主题层级设计混乱，订阅通配符过宽导致消息风暴。
- 把所有消息设为最高 QoS，带宽与确认开销失控。
- 把设备侧的不可靠网络假设照搬到数据中心内部。

## 参考资料

- MQTT 规范：https://mqtt.org/
- NestJS 微服务文档：https://docs.nestjs.com/microservices/basics
