---
description: "NestJS microservices: transport-based architecture, transporters, message and event patterns, ClientProxy, hybrid applications and resilience"
描述: "NestJS 微服务：基于传输层的架构、transporter、消息与事件模式、ClientProxy、混合应用与韧性"
name: "NestJS"
名称: "NestJS"
---

# NestJS

NestJS 是 TypeScript 优先的 Node.js 应用框架，微服务是其中的一部分。官方定义是：**Nest 中的微服务本质上是一个使用不同于 HTTP 的传输层（transport）的应用**。依赖注入、装饰器、异常过滤器、管道、守卫与拦截器等核心概念在微服务中同样适用；它提供代码结构与完整生态，但不内置服务发现与客户端负载均衡。

## 传输层

transporter 负责在微服务实例间传递消息，多数原生支持 request-response 与 event-based 两种风格。Nest 用统一接口屏蔽各 transporter 的实现细节，因此可在不改应用代码的情况下切换传输层。

- **内置 transporter**：TCP（默认）、Redis、NATS、MQTT、RabbitMQ、Kafka、gRPC。
- **NATS / RabbitMQ 队列组**：把同一服务的多个实例放进同一队列组，由 broker 侧分摊消息，形成实例间的负载均衡。
- **混合应用**：同一进程既做 HTTP 服务又监听微服务传输层，用 `connectMicroservice()` 挂载。

## 消息与事件模式

微服务用 **pattern** 识别消息与事件。pattern 是普通值（字符串或对象字面量），会随消息体一起序列化发送，发送方与消费方借此约定哪些请求由哪个 handler 处理。

- **`@MessagePattern()`**：用于 request-response，只能放在 controller 中（provider 中使用会被忽略）。handler 可同步、async 或返回 Observable——返回 Observable 时每个发射值都是一次响应，直到流结束。
- **`@EventPattern()`**：用于事件驱动。同一 event pattern 可注册多个 handler，Nest 会并行触发全部。
- **pattern 限制**：对象 pattern 最多 5 层嵌套、每对象 20 个 key、每数组 20 项、key 最长 256 字符、字符串值最长 4096 字符、整体最多 100 个 key；超出部分在匹配前被 `[TOO_MANY_KEYS]` 之类的标记替换。超过 1 MiB 的 JSON pattern 按纯字符串匹配，不解析。

## ClientProxy

`ClientProxy` 让客户端应用与微服务交换消息或发布事件。

- **获取方式**：`ClientsModule.register()` / `registerAsync()`，或 `ClientProxyFactory.create()` 创建自定义 provider；`@Client()` 属性装饰器也可用但不推荐（难测试、难共享）。
- **惰性连接**：`ClientProxy` 不立即建连，在首次调用前建立并复用；需要提前建连时在 `onApplicationBootstrap()` 中调用 `connect()`。
- **`send()`**：request-response，返回**冷 Observable**，必须订阅才会真正发送消息；pattern 需匹配 `@MessagePattern()`。
- **`emit()`**：事件驱动，返回**热 Observable**，立即尝试投递，无需订阅；pattern 需匹配 `@EventPattern()`。

## 序列化与传输细节

TCP 传输不是裸 JSON：`JsonSocket` 先写 JSON 文本的长度、再写 `#`、再写文本本身，格式为 `length#jsonText`。长度按 UTF-16 code units 计（JavaScript `String#length`），不是字节数，也不是 Unicode 码点数——写错计数会在非 ASCII 字符上错位。TCP options 支持自定义 `serializer` / `deserializer`。Redis 传输把包作为纯 JSON 文本发布，并由 channel 而非 `pattern` 字段选择 handler（如 `sum` 与 `sum.reply`）。

## 韧性

核心 `@nestjs/microservices` 不内置熔断。较新版本提供 Resilience 模块，用 `@Retry`、`@Timeout`、`@CircuitBreaker`、`@Bulkhead`、`@Fallback`、`@Idempotent` 等装饰器与 preset 声明策略，需在根模块注册 `ResilienceModule.forRoot()`。要点：

- 状态按进程隔离：每个实例有自己的 breaker、bulkhead 与出站限流，重启即清零，半开状态放行单次探测。
- fallback 必须廉价且独立，绝不能回调它所替代的依赖。
- 幂等存储必须注册外部存储（如 PostgreSQL），否则记录只存于进程内存，重启丢失且生产环境拒绝启动。
- 对 breaker 打开、bulkhead 拒绝等状态跃迁设置告警。

## 选型定位

NestJS 的强项是代码结构、TypeScript 工具链、生态集成（REST / GraphQL / WebSocket / Swagger / 队列 / 定时任务）与团队一致性。它把服务发现交给 Kubernetes Service/DNS、Consul 等外部设施，把客户端负载均衡交给队列组或服务网格，把韧性交给 Resilience 模块或 opossum 等库。若需要框架原生内置发现、均衡与熔断，Moleculer 更合适；若追求单实例 HTTP 性能，Fastify 更合适，也可作为 NestJS 的 adapter 使用。

## 常见失败模式

- 把 `send()` 当普通 Promise 调用却不订阅，消息根本没发出。
- pattern 超出嵌套与 key 数限制，handler 静默失配。
- 自写熔断却忽略状态按进程隔离，重启后策略清零。
- fallback 回调原依赖，故障沿备用路径继续传播。
- 用可变 tag 或未固定 transporter 配置，导致环境间行为不一致。
- 把 NestJS 当成自带服务发现的框架，容器化环境下重复搭建注册中心。

## 参考资料

- NestJS 微服务与韧性文档：https://docs.nestjs.com/microservices/basics
