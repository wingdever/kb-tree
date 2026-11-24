---
description: "Agent-to-agent protocol: tasks, messages, artifacts and three transport bindings"
描述: "智能体间协作协议：任务、消息、产物与三种传输绑定"
name: "Agent to Agent Protocol"
名称: "智能体与智能体协议"
---

# Agent to Agent Protocol

A2A 解决**跨组织、跨框架的 Agent 协作**：调用方先读对方的 Agent Card 决定是否委派，再用 Task 跟踪一次有状态的工作，结果以 Artifact 交付。传输可选 JSON-RPC、gRPC、HTTP+JSON 三种绑定，长任务的进度用 SSE 或 Webhook 推进。

## A2A 核心概念

- **Agent Card**：Agent 的自描述清单——身份、能力、skills、服务端点、鉴权方式、输入输出模态，可带 JWS 签名。客户端先读 card 再决定是否委派。
- **Task**：有状态的工作单元，`submitted → working → completed / failed / canceled`，可中断为 `input-required` / `auth-required`；支持多轮续任务（`taskId` + `contextId`）。
- **Message / Part**：一轮通信，角色 `user` / `agent`；Part 是最小内容单元（text / file（raw 或 url）/ data 三选一）。
- **Artifact**：任务输出，**结果应放在 Artifact 而不是 Message 里**。
- **Context**：把相关任务与消息归到同一会话。
- **更新机制**：轮询 `GetTask`、SSE 流式、Webhook 推送三种。
- **设计要点**：Agent 保持不透明——不共享内部提示词、记忆与工具列表；跨组织委派时这是核心价值。

## 与 MCP 的分工

MCP 纵向（Agent ↔ 工具/数据），A2A 横向（Agent ↔ Agent）：MCP 让一个 Agent 获得能力，A2A 让不同所有者的 Agent 互相委派。差别根子在控制权——MCP 客户端逐次指挥每次工具调用，拿到的是有明确 schema 的输入输出；A2A 交出任务后，远端 Agent 自己决定怎么完成，调用方看不到它的工具与提示词。

两者通常同场出现。采购 Agent 用 MCP 读自家库存库，再用 A2A 向供应商的销售 Agent 询价下单；供应商那一侧的 Agent 又用 MCP 查自己的仓库与定价系统。

## 结构

规范把协议拆成三层：**数据模型**（Task / Message / Part / Artifact 等字段定义，与传输无关）、**抽象操作**（SendMessage、GetTask、CancelTask 等能力）、**协议绑定**（把同一批操作映射到具体线格式）。换绑定不改语义，这是跨实现互通的前提。

### Interact layer

1. Inbound A2A Server
- SendMessage
- SendStreamingMessage
- GetTask
- ListTasks
- CancelTask
- SubscribeToTask
- CreateTaskPushNotificationConfig / Get / List / Delete
- GetExtendedAgentCard
2. Outbound A2A Client
### Data layer（数据模型）
0. AgentCard
- name
- description
- version: 0.1.0
- supportedInterfaces: [{
    url
    protocolBinding: JSONRPC
    protocolVersion: 1.0.1
}]
- capabilities: {streaming: false}
- defaultInputModes: [text/plain]
- defaultOutputModes: [text/plain]
- skills: [{
    id
    name
    description
}]
1. Context
contextId
2. Task
id：string，唯一，必填
status：object，必填
    state：枚举 submitted → working → completed / failed / canceled，可中断为 input-required / auth-required
    message：本条状态说明
    timestamp：状态更新时间
contextId
artifacts
history
metadata

3. Message
messageId
4. Part
kind: text / file（raw 或 url）/ data
5. Artifact
### Protocol layer

同一批操作有三种绑定，规范要求同一 Agent 的多绑定在功能、错误映射与鉴权上保持一致，客户端可任选其一并保留降级路径：

- **JSON-RPC 2.0 over HTTP(S)**：方法名 PascalCase（`SendMessage`、`SendStreamingMessage`、`GetTask`、`ListTasks`、`CancelTask`、`SubscribeToTask`、`GetExtendedAgentCard`）；流式用 SSE（`text/event-stream`），每个事件是一帧 JSON-RPC result。
- **gRPC**：与 JSON-RPC 同名的 RPC，数据模型是同一套 proto 定义；适合内网、强类型客户端与双向流的实现。
- **HTTP+JSON（REST）**：`POST /message:send`、`POST /message:stream`、`GET /tasks/{id}`、`GET /tasks`、`POST /tasks/{id}:cancel`、`POST /tasks/{id}:subscribe`；请求与响应建议用 `application/a2a+json`。
- **推送配置**：`Create / Get / List / DeleteTaskPushNotificationConfig` 挂在 `/tasks/{id}/pushNotificationConfigs`，用于断线后的异步通知。
- **版本与路由**：`A2A-Version` 请求头声明协议版本；多个 Agent 共用一个端点时用 `tenant` 区分，客户端必须回填 card 中声明的值。
- **流式事件只有两种增量**：`TaskStatusUpdateEvent`（状态变化）与 `TaskArtifactUpdateEvent`（产物分片）；收到终态事件即关流。

## Artifact范式

A2A 规定结果放在 Artifact（`artifactId` / `name` / `description` / `parts` / `metadata`），但没规定 Artifact 怎么产生。产物从 Agent 交到调用方有三条显式路径、两条隐式路径与一种混合做法，取舍看四个判据：**能否 schema 校验、能否增量流式、能否按 id 引用续改、换宿主后是否还成立**。

- 显式：提示词格式约定、结构化输出、显式 Artifact 工具。
- 隐式：运行时捕获、后处理解析。
- 混合：提示词引导 + 工具校验 + 解析兜底。

### 提示词格式约定

在系统提示或任务提示里约定固定容器，让模型把产物包在可识别的结构里——XML 标签（`<artifact name="report.md">…</artifact>`）、固定一级标题、或明确的分隔符。

- **优点**：零协议改动，任何模型与宿主都能用；产物仍是文本，人可读、可 diff、可审阅。
- **代价**：完全靠模型自律，长输出、多产物、正文里出现同名标签时会漂移；没有 schema 校验；调用方必须写解析器，还要容忍格式偏差。
- **判据上的表现**：可校验弱、可流式弱（只能按标签边界猜）、可引用无、复用性高。
- **适用**：原型期、单产物、以人读为主；不适合需要机器消费与增量更新的生产链路。

### 结构化输出

用 JSON Schema 或工具参数 schema 约束模型输出对象，字段承载产物元数据（`artifactId`、`name`、`mimeType`）与内容分片。

- **优点**：可机器校验、失败可重试、字段稳定；适合清单、评分、配置、引用列表这类结构化产物。
- **代价**：正文塞进 JSON 字符串要转义，几万字的报告或代码会让 token 成本与出错率同时上升；模型对 schema 的遵从度随输出长度下降；流式只能按 JSON 增量解析，体验差。
- **判据上的表现**：可校验强、可流式弱、可引用中（靠字段约定）、复用性中。
- **适用**：产物本身是结构化数据，或采用「元数据走 schema、正文走 Artifact 的 text part」的分离写法。

### 显式Artifact工具

由宿主提供 `write_artifact`、`create_file` 一类工具，参数按 A2A Artifact 的字段设计（`artifactId`、`name`、`mimeType`、`parts`）；Agent 每完成一段就调用一次，协议层把调用转成 `TaskArtifactUpdateEvent` 推给调用方。

- **优点**：产物与对话解耦，可按 id 引用、分段追加或替换、承载大文件，天然支持流式；存储与权限留在宿主手里。
- **代价**：宿主必须实现工具、存储与版本策略（同名是覆盖还是新版本）；工具名与参数各家不统一，跨实现移植要适配；Agent 漏调工具时会退化成纯文本，需要兜底。
- **判据上的表现**：可校验强（参数是 schema）、可流式强、可引用强、复用性中（依赖工具契约）。
- **适用**：生产链路、长文档、多产物、下游要直接取文件而不是再解析文本的场景。

### 运行时捕获

不要求模型产出可识别的容器，而是由宿主在工具执行后扫描副作用（工作区文件变更、新建的文件句柄），把新文件包装成 Artifact。

- **优点**：模型不必配合，产物天然是真实文件，适合编码与研究类工作区。
- **代价**：归因困难——哪些变更算产物、哪些是临时文件，需要忽略规则、体积上限与去重；也可能把中间态打包出去。
- **判据上的表现**：可校验弱、可流式中（随文件落盘推进）、可引用中（按路径或 id）、复用性中。

### 后处理解析

对话结束后从整段输出里抽取结果，用正则、标记切分或二次模型改写。

- **优点**：对既有 Agent 零改造，能补救没有工具与 schema 的实现，历史轨迹也能重放。
- **代价**：解释文字容易混进产物，示例与真实结果难区分；不可校验、不可流式、不可按 id 引用，失败时只能整段重来。
- **判据上的表现**：可校验无、可流式无、可引用无、复用性低。
- **适用**：迁移旧实现时的过渡手段，不宜作为新链路的设计选择。

### 混合模式

提示词引导 + 工具校验 + 解析兜底：提示词约定产物结构，专用工具负责落盘与校验，解析器只处理工具缺失的降级路径。

- **优点**：可在旧实现上渐进升级，任一环节失效时仍有可用的降级路径。
- **代价**：三条路径都要维护，行为不一致时排查成本高；必须有明确的优先级（工具 > 格式 > 解析），否则同一个产物会出现两个版本。
- **判据上的表现**：可校验强、可流式强、可引用强、复用性中。
- **适用**：从原型走向生产的过渡期，或客户端能力参差不齐的开放协议场景。

## 安全与信任边界

- **Agent Card 是不可信输入**：它由远端自述，签名只证明这份 card 来自该域名，不证明行为可信。按引入第三方依赖的标准审查，鉴权范围收窄到单一 Agent。
- **把每个远端 Agent 当作独立 OAuth resource server**：各自认证、各自授权；不把终端用户 token 原样转发给对端，也不让对端 token 进入自己的工具链。
- **委派要可审计**：记录 `taskId` / `contextId`、发起方与返回方；付款、删除、对外发送这类不可逆动作，执行前留人工确认位。
- **提示注入是双向的**：对端返回的 Artifact 与状态消息都可能夹带隐藏指令，一律当数据处理，不当指令执行。
- **"secure by default" 的边界**：规范要求企业级 HTTP 认证、不强制泄露内部提示词、支持 human-in-the-loop；但哪些任务可以委派属于策略层，规范不替你决定。

## 何时用 / 何时不需要

用得上的信号：

- 工作必须交给另一个团队、框架或厂商构建的 Agent，而不是自己的工具。
- 对端不透明：你只能先读 card、后拿结果，读不到它的内部实现。
- 任务有生命周期：几秒到几小时，中途要状态、要中断、要人工审批。
- 需要跨组织的能力发现与鉴权，而不是一次性 HTTP 调用。

不需要：

- 步骤固定、每次相同——普通工作流或定时集成更便宜。
- 所有 Agent 都在一个应用、一个框架内——框架自带的 handoff 与共享状态足够。
- 对端是固定 JSON schema 的确定性服务——普通 REST 客户端就够，task 生命周期是多余开销。

一条边界：A2A 标准化的是信封与生命周期，不是规划算法；它不保证委派正确，评估、沙箱与成本上限仍在自己这侧。

## 参考资料

- A2A 官方规范（v1.0 及 1.x）：https://a2a-protocol.org/latest/specification/
