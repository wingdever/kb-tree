---
description: "Model Context Protocol architecture, primitives, transports and security"
描述: "MCP 协议的架构、原语、传输与安全机制"
name: "Model Context Protocol In Depth"
名称: "MCP 深度"
---

# A4 MCP 深度

MCP（Model Context Protocol）是把 AI 应用连接到外部系统的开源标准。类比：**AI 应用的 USB-C 接口**——标准化连接方式，而非设备本身。

- 它是**薄的、模型无关的协议**：让 Agent 通过标准接口发现并调用工具、获取资源、调用提示词模板。
- 它**不是框架、不是编排引擎**，对模型选择不持立场。
- 2024 年 11 月由 Anthropic 发布；2025 年 12 月捐给 Linux Foundation，由 Agentic AI Foundation 治理。Claude、ChatGPT、Gemini、Copilot、Cursor、VS Code、Replit 等原生支持。
- 解决 M×N 集成问题：一个 MCP server 可被组织内所有 Agent 复用，而非每个 Agent 写一套集成代码。

## 架构：Host–Client–Server

MCP 遵循 client-host-server 架构，每个 host 可运行多个 client 实例。**MCP 是无状态协议**：每个请求自包含，携带自己的协议版本和能力。基于 JSON-RPC。

### Host（宿主进程）

容器与协调者：

- 创建并管理多个 client 实例
- 控制 client 的连接权限与生命周期
- 执行安全策略与同意（consent）要求
- 处理用户授权决策
- 协调 AI/LLM 集成
- 管理跨 client 的上下文聚合

### Client

由 host 创建，**与且仅与一个 server 通信**：

- 与恰好一个 server 通信（1:1 关系）
- 给每个请求附上协议版本和能力
- 双向路由协议消息
- 管理订阅与通知
- 维护 server 间的安全边界

### Server

提供专门上下文与能力：

- 通过 MCP 原语暴露 resources、tools、prompts
- 独立运行、职责聚焦
- 可在回复中通过 `InputRequiredResult` 请求 client 输入（elicitation）
- 必须遵守安全约束
- 可以是本地进程或远程服务

## 设计原则

1. **Server 必须极易构建**：host 承担复杂编排；server 聚焦明确能力；简单接口降低实现开销。
2. **Server 必须高度可组合**：每个 server 隔离提供聚焦功能；多 server 无缝组合；共享协议实现互操作；模块化支持扩展。
3. **Server 不能读完整对话，也不能"看见"其他 server**：server 只收到必要的上下文；完整对话历史留在 host；每个 server 保持隔离；跨 server 交互由 host 控制；host 进程执行安全边界。
4. **特性可渐进添加**：核心协议提供最小必需功能，额外能力按需协商；client/server 独立演进；保持向后兼容。

## 能力协商（Capability Negotiation）

基于能力的协商系统：

- Client 在**每个请求**的 `_meta.io.modelcontextprotocol/clientCapabilities` 中携带自身能力。
- Server 在响应 `server/discover` 时宣告能力；client 可在任何请求前先调用它做能力发现。
- Server 声明的能力示例：工具支持、资源订阅、提示模板。
- Client 声明的能力示例：elicitation 处理。
- 双方在整个交互中必须遵守已声明的能力；额外能力可通过协议扩展协商。

每项能力按请求解锁特定协议特性：实现的 server 特性必须在其能力中宣告；接收资源更新通知需要打开 `subscriptions/listen` 流；工具调用要求 server 声明工具能力。

## 三个原语

| 原语 | 是什么 | 控制方 | 方法 |
|---|---|---|---|
| **Tools（工具）** | 模型调用以采取行动的可执行函数；输入参数用 JSON Schema 的 `inputSchema` 声明 | **模型控制**（model-controlled） | `tools/list`、`tools/call` |
| **Resources（资源）** | 提供上下文的只读数据源：文件内容、数据库 schema、文档；每个资源有 URI | **应用控制**（application-controlled），host 决定怎么用 | `resources/list`、`resources/read`；更新通知走 `subscriptions/listen` |
| **Prompts（提示）** | 可复用的交互模板，如斜杠命令、工作流起点 | **用户控制**（user-controlled），用户显式选择 | `prompts/list`、`prompts/get` |

**Tools 是风险最高的原语**，因为它代表真实世界的副作用。

### Client 特性

- **Elicitation**：让 server 通过 client 向用户请求更多信息。Form 模式请求结构化数据（可用 JSON schema 校验）；URL 模式把用户送到外部 URL 做敏感交互。
- **Sampling**（已弃用）：让 server 通过 client 请求 LLM 补全，client 保持对模型访问的控制，server 无需自己的 API key。2026-07-28 起弃用，建议直接集成 LLM provider API。
- **Roots**（已弃用）：告诉 server client 认为相关的目录和文件；规范明确这是"信息性指引而非访问控制机制"，协议不强制 server 留在其中。已弃用，建议通过工具参数、资源 URI 或 server 配置传递目录/文件。

## 传输（Transport）

- **Stdio**：本地 server，与 host 同机运行；快、无网络开销、进程隔离。
- **Streamable HTTP**：远程 server，配合 OAuth 2.0。取代旧的 HTTP+SSE（2024-11-05 版用双端点，2025-03-26 版被 Streamable HTTP 取代）。2026-07-28 版进一步移除了 GET stream 端点和协议级会话（`Mcp-Session-Id` 头）。
- 旧 SSE 传输在 2025-06-18 规范中已弃用，应迁移。

**长运行/异步操作**：工具调用立即返回 job ID，另暴露 `get_job_status` 让 Agent 轮询；用 `notifications/progress` 推送增量进度；极长操作可用 webhook 回调。

## 有状态 vs 无状态

- **有状态**（2026 默认推荐）：对运行多步任务的自主 Agent，提供原生会话连续性和中断恢复。多数生产 Agent 工作流受益于有状态连接 + Redis 热层。
- **无状态**（2026 RC 提供）：适合简单离散工具调用、横向扩展比会话连续性更重要的场景。

> 注：协议层"无状态"指每个请求自包含；server 实现仍可有状态以支持会话。

## 安全与同意

规范原则：

- MCP "通过任意数据访问和代码执行路径启用强大能力"。
- 用户必须显式同意并理解所有数据访问与操作。
- Host 在向 server 暴露用户数据前、在调用任何工具前，必须获得用户显式同意。
- 工具行为描述（如 annotations）应视为**不可信**，除非来自可信 server。
- 规范明确局限："MCP 本身无法在协议层强制这些安全原则"——实现者须在应用中构建同意与授权流程。工具页面补充：始终有能拒绝工具调用的人在回路。
- 远程 server 的授权层基于 OAuth。

### 五大安全风险（2025–2026 均在野出现）

1. **工具投毒（Tool poisoning）**：恶意指令藏在工具描述深处——AI 读完整 JSON schema，人只看简化 UI 标签。研究显示对主流 Agent 成功率可达 72.8%。
2. **资源提示注入**：工具输出中的恶意数据劫持 Agent 行为。
3. **Rug pull**：建立信任后，合法工具被悄悄更新为恶意逻辑 → 固定并审查工具定义，重新验证 server。
4. **过度授权工具**：违反最小权限。
5. **未验证第三方 server 的供应链风险**。

### 分层防线

- OAuth 2.0 + 细粒度 scope + RFC 8707 audience restriction
- 两阶段输入校验（模式匹配 + 语义）用于每次工具调用
- 每工具速率限制 + `retry_after` 响应
- 用 elicitation 要求高风险工具执行前人工批准
- 输出清洗作为最后一道门——绝不把原始敏感数据返回给 Agent

## 企业架构

- **MCP 网关**：所有 agent→server 流量的单一入口，处理认证、限流、审计日志、脱敏。
- **Server 注册表**：内部已批准 server 目录，带数据分类、scope、owner 元数据。
- **SSO 集成认证**：用 IdP（Okta/Entra/Ping），Agent 调用继承调用者权限并产生可审计轨迹。
- **策略层**：按工具、按 scope 的策略（谁能调用什么、何时、用什么数据分类）；ABAC 在此发挥价值。
- **可观测性**：追踪每次 agent→gateway→server→backend 调用。

**构建 vs 采用**：通用 SaaS（Slack、GitHub、Jira、Salesforce、Notion）采用现成 server（9,400+ 公开 server）；公开 server 不错但 auth/策略需收紧的，采用后加固（Snowflake、Postgres）；内部系统、专有数据层、需领域塑造 agent-tool 契约的，自建。

常见错误：每个系统一个巨型 server（难授权难审计，应小而按能力划分）；跳过网关（POC 可以，生产是安全审查噩梦）；把 MCP 当编排层（它不是）；未审查的公开 server 接私有数据；工具调用无回归测试（小模型改动一夜之间破坏工具调用契约）。

## 参考资料

- MCP 官网与规范索引：https://modelcontextprotocol.io
- MCP 规范（2025-06-18 版本）：https://modelcontextprotocol.io/specification/2025-06-18
- Anthropic 发布公告《Introducing MCP》：https://www.anthropic.com/news/model-context-protocol
