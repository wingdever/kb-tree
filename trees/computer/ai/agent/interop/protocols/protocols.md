---
description: "Agent interoperability protocols: MCP for tools, A2A for agent-to-agent, ACP name collisions and AG-UI/AP2"
描述: "Agent 互操作协议：MCP 连工具、A2A 连 Agent、ACP 同名消歧与 AG-UI/AP2"
name: "Agent Interoperability Protocols"
名称: "Agent 互操作协议"
---

# Agent 互操作协议

协议按「对面是谁」分层，不是为了追新。**工具走 MCP，Agent 走 A2A，前端走 AG-UI，支付走 AP2**。本节点讲协议地图与同名消歧。

## 官方入口

| 协议 | 规范 / 官网 |
|---|---|
| MCP | `https://modelcontextprotocol.io` |
| A2A | `https://a2a-protocol.org/latest/specification/`；仓库 `github.com/a2aproject/A2A` |
| ACP（Agent Client Protocol） | `https://zed.dev/acp`；注册表 `https://zed.dev/acp` |
| AG-UI | `https://docs.ag-ui.com/` |
| AP2 | `https://github.com/google-agentic-commerce/AP2` |
| ANP | `https://github.com/agent-network-protocol/AgentNetworkProtocol` |

## 三协议对照

| | **MCP** | **A2A** | **ACP（Zed）** |
|---|---|---|---|
| 连什么 | Agent ↔ 工具 / 数据 | Agent ↔ Agent | 编辑器 ↔ 编码 Agent |
| 提出方 | Anthropic | Google → Linux Foundation | Zed |
| 治理 | Agentic AI Foundation（LF） | Linux Foundation / Agentic AI Foundation | Zed 主导，社区共建 |
| 消息 | JSON-RPC 2.0 | JSON-RPC / gRPC / HTTP+JSON | JSON-RPC over stdio |
| 发现 | 配置 server 后列能力 | `Agent Card`（well-known URI） | 编辑器内注册 / Registry |
| 长任务 | 有限 | Task + SSE 流式 + Webhook 推送 | 随会话 |
| 状态 | 活跃，规范 2026-07-28 | 活跃，稳定 v1.0 | 活跃 |

官方口径：**MCP 纵向深入一个 Agent，A2A 横向连接 Agent 之间**——互补，不是替代。只碰自有工具就只需 MCP；出现「别的团队 / 厂商的 Agent 参与」才加 A2A。

## ACP 同名消歧

`ACP` 指三个不同的东西，写设计文档时必须写全称：

| 全称 | 来源 | 现状 |
|---|---|---|
| **Agent Communication Protocol** | IBM Research / BeeAI，REST-first、async-first | **2025-08 并入 A2A，仓库归档**——不要再按它设计，已有部署走迁移路径 |
| **Agent Client Protocol** | Zed，JSON-RPC over stdio，思路接近 LSP | **活跃**：编辑器 ↔ 编码 Agent；JetBrains、VS Code、Emacs、Neovim 等接入；CodeBuddy、Qoder、Claude Code、Codex、Gemini CLI 等在册 |
| **Agentic Commerce Protocol** | Stripe / OpenAI / Meta | Agent 驱动的结账与支付，与互操作无关 |

你上一条提到的「用 CodeBuddy / QoderCN 当客户端」，对应的是**第二个**——Agent Client Protocol 解决「编辑器里换 Agent」，不是「Agent 之间对话」。

## 周边协议：界面、支付与网络

MCP / A2A / ACP 解决「连谁」，下面这圈解决另外三件事：**界面怎么呈现、钱怎么付、跨组织怎么发现**。三者正交，可同时出现在一个系统里。

### 界面层：AG-UI 与 A2UI

- **AG-UI**（Agent–User Interaction Protocol）：**事件驱动**的双向协议，连接 Agent 后端与用户界面。建在 HTTP / WebSocket 之上，标准化状态、UI 意图与用户交互的流动。能力包括 token 流式、typed attachments、生成式 UI、共享状态（带事件源 diff 与冲突解决）、思考步骤可视化、前端工具调用、中断/审批/编辑/重试、子 Agent 编排与 steer。客户端**不一定是网页**——终端、移动 App、Slack / Teams 都可作 client。
- **A2UI** 是另一个东西：生成式 UI 规范，让 Agent 交付 UI 组件树；AG-UI 负责把事件传过去。两者互补，**不要混淆名称**。

### 支付层：授权 / 结算 / 结账三条线

Agent 支付按「谁负责哪一段」分化为多个协议，不是互斥关系：

| 协议 | 层次 | 解决什么 | 维护方 / 状态 |
|---|---|---|---|
| **AP2**（Agent Payments Protocol） | 授权 | 把预算、商户、时间、退款条件转成**防篡改的数字授权书（mandate）**，可追溯、可审计；建在 A2A / MCP 之上 | Google 提出，2026-04 移交 FIDO Alliance 标准化 |
| **x402** | 结算 | 复活 HTTP `402 Payment Required`，一次 HTTP 请求周期内完成链上微支付，适合按次买 API / 数据 | Coinbase / Cloudflare，x402 基金会 |
| **MPP** | 结算 | 把支付嵌进 HTTP 请求的机器支付协议 | Stripe |
| **ACP**（Agentic Commerce Protocol） | 结账 | 标准化 Agent 与商户的对话式购物车 / 结账流程 | OpenAI + Stripe（**又一个 ACP 同名**） |
| **UCP**（Universal Commerce Protocol） | 商业通用 | Agent 电商的通用购物规则，被称为「Agent 电商的 HTTP」 | Google 开源，多家零售商与技术委员会 |
| **TAP / AMP** | 身份 / 区域方案 | Visa 可信 Agent 协议证明「代表用户行事」；蚂蚁 AMP 做钱包侧身份互认与微结算 | 卡组织 / 区域生态 |

实际一笔交易可能串起多条线：AP2 授权 → TAP 证明身份 → x402 / MPP 买即时数据 → ACP 组织结账 → 卡网络完成大额结算。**跨协议的责任划分与争议处置仍未统一**，治理碎片化是当前主要风险。

### 网络层：ANP

- **ANP**（Agent Network Protocol）：目标是「Agentic Web 的 HTTP」——让 Agent 跨平台发现、认证、通信、协作，而不是困在各家平台 API 里。
- **不重建网络栈**：复用 HTTP / DNS / TLS / CDN，在其上加 DID 身份层与应用协议层。
- **身份用 W3C DID**：`did:wba` 与原生 `did:web` 兼容；ANP-02 认证、ANP-03 DID 方法、ANP-04 命名（WNS Handle）。
- **发现分两段**：ANP-07 Agent Description 声明能力与接口，ANP-08 Discovery 用 `.well-known` 主动发现或向搜索 Agent 注册。
- **消息模块化**：ANP-09 定义 P1–P9 九个 Profile（直连/群聊/E2EE/附件/联邦等）。
- **状态**：规范集 **ANP 1.2**；ANP-05 授权、ANP-06 元协议、ANP-10 支付适配仍是草案，别当稳定能力用。实现参考 AgentConnect SDK。
- 明确声明**不发任何数字货币**——这点常被误传。

### 协议分层速查

```
界面   AG-UI（事件流） / A2UI（生成式 UI 规范）
工具   MCP
Agent  A2A（跨组织） / 同团队内置编排
编辑器 ACP（Agent Client Protocol）
支付   AP2（授权） / x402·MPP（结算） / ACP·UCP（结账）
网络   ANP（身份·发现·消息）
```

## 选择规则

按顺序问「对面是谁」：

1. 对面是**函数 / API / 数据源** → MCP。
2. 对面是**另一个 Agent**，且在同代码库同团队 → 内置编排就够，不必上 A2A。
3. 对面是**别的团队 / 厂商的 Agent** → A2A（需要发现、鉴权、长任务与结果回传）。
4. 对面是**人的编辑器** → Agent Client Protocol。
5. 对面是**用户界面** → AG-UI（事件流）或 A2UI（生成式 UI 组件）。
6. 要让 Agent **付钱** → 按环节选：授权 AP2、微支付 x402 / MPP、结账 ACP / UCP；跨协议责任仍需人工兜底。
7. 要跨组织**发现并认证** Agent → A2A 的 Agent Card 够用；要去中心化身份 / 大规模网络才上 ANP（1.2，部分草案）。

> 协议标准化的是线路格式，不是语义：两个 MCP server 可能暴露不同的工具名。切换成本积累在运行时与界面之上，不在协议本身。

## 安全边界

- **A2A 的 Agent Card 是不可信输入**：别因为 card 在网上找到就相信它；按依赖审查，scope token 到单一 Agent。
- **MCP 的风险在工具权限与工具输出里的提示注入**。
- 委派任务与工具调用都要可审计：谁发起、返回了什么；不可逆动作必须人工确认。

## 一句话主线

**协议按「对面是谁」分工：MCP 连工具、A2A 连 Agent、ACP（Client）连编辑器、AG-UI 连前端、AP2 连支付；ACP 另有已并入 A2A 的同名协议——写全称才不会选错。**

