---
description: "gRPC transport: HTTP/2 and Protocol Buffers based RPC with strong contracts, streaming and call metadata"
描述: "gRPC 传输：基于 HTTP/2 与 Protocol Buffers 的 RPC，强契约、流式与调用元数据"
name: "gRPC Transport"
名称: "gRPC 传输"
---

# gRPC 传输（gRPC Transport）

gRPC 是基于 HTTP/2 的高性能 RPC 框架，默认用 Protocol Buffers 同时作为接口定义语言与线上格式，由 `protoc` 生成各语言桩代码，是 CNCF 孵化项目。在 NestJS 中它是内置 transporter 之一。

## 核心特性

- **四种通信模式**：Unary、服务端流、客户端流、双向流。
- **强类型契约**：proto 定义服务与消息，生成代码跨语言一致，编译期即可发现契约错误。
- **HTTP/2 底座**：多路复用、头部压缩、长连接，适合高频低延迟内部调用。
- **可插拔认证**：TLS / token 等机制。
- **调用元数据**：correlation id、tenant、locale 等附加信息走 call metadata，不进 payload。

## 适用与边界

- 适合服务间高频、低延迟、强类型要求的内部调用，以及需要流式的场景。
- 浏览器直连需 gRPC-Web 代理；默认不纳入 HTTP 缓存；二进制负载不可直接阅读。
- 服务发现与负载均衡通常交给 Kubernetes Service 或服务网格。
- 对外可保留 REST，用一份 proto 契约经 HTTP 映射产出两套表面。

## 常见失败模式

- 把 gRPC 当对外公开 API，忽略浏览器与缓存限制。
- proto 破坏性变更不升版本号，导致上下游同时失效。
- 把 correlation id 等塞进 payload，污染业务 schema。
- 只追求基准吞吐，忽略实际瓶颈常在数据库与序列化。

## 参考资料

- gRPC 文档：https://grpc.io/docs/
- NestJS 微服务文档：https://docs.nestjs.com/microservices/basics
