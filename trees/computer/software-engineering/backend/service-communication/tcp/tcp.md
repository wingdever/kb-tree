---
description: "TCP transport: default NestJS microservice transport, length-prefixed JSON packets, built-in TLS and non-Nest interoperability"
描述: "TCP 传输：NestJS 默认微服务传输、长度前缀 JSON 包、内建 TLS 与跨系统互通"
name: "TCP Transport"
名称: "TCP 传输"
---

# TCP 传输（TCP Transport）

TCP 是 NestJS 微服务的**默认传输层**，基于 Node 的 `net` / TLS 模块，无消息 broker。它适合服务少、拓扑简单、需要低开销同步调用的场景，也适合与非 Nest 服务直接通信。

## 数据包格式

TCP 传输不写裸 JSON：`JsonSocket` 先写 JSON 文本长度，再写 `#`，再写文本本身，即 `length#jsonText`。长度按 **UTF-16 code units** 计（JavaScript `String#length`），不是字节数，也不是 Unicode 码点数——写错计数会在非 ASCII 字符（如 emoji）上失步。包的形状固定，因此非 Nest 系统无需 `@nestjs/microservices` 也能调用 handler 并应答。

## 关键配置

- **host**：默认 `localhost`（空值也表示 localhost）；容器中被其他主机连接时必须设 `0.0.0.0` 或 `::`。
- **port**：默认 3000。
- **tlsOptions**：基于 Node TLS，加密微服务与客户端之间的通信。
- **serializer / deserializer**：自定义出站/入站序列化。
- **maxBufferSize**：单个入站包最大字符数，默认 16 MB。
- **incompleteMessageTimeout**：对端在包中间静默多久后断开，默认 30s。
- **messageReceiveTimeout**：单个包从首字符到末字符的时限，默认 300s，后续读取不延长。
- **maxSendBufferSize / drainTimeout**：对端不读时最多排队多少字节、排队多久。
- **maxConcurrentMessages**：同一对端并发处理上限，默认 1000。
- **gracefulShutdown / gracePeriod**：优雅关闭与最长等待。

非数字值（如未设置环境变量经 `Number()` 得到的 `NaN`）会回退到默认值。

## 适用与边界

- 默认、轻量、无 broker；request-response 与 event-based 都支持。
- 无内置服务发现、持久化与重放；多实例负载均衡需外部机制。
- 长度前缀格式是与非 Nest 系统互通的关键约定，手写客户端必须严格遵守。

## 常见失败模式

- 容器里沿用默认 `localhost`，导致外部无法连接。
- 用字节数或码点数计算长度前缀，非 ASCII 负载错位。
- 把 TCP 当持久消息系统，期望消息不丢或可重放。
- 忽略 `maxBufferSize` 与超时，超大包或半开连接拖垮服务。

## 参考资料

- NestJS 微服务文档：https://docs.nestjs.com/microservices/basics
