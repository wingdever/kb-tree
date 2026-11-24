---
description: "Agent2Agent protocol: agent cards, tasks and MCP comparison"
描述: "A2A 协议：Agent Card、任务生命周期及与 MCP 的区别"
name: "A2A Protocol"
名称: "A2A 协议"
---

# A2A 协议（Agent2Agent）

A2A 让不同框架、不同团队、不同公司构建的 Agent 能发现彼此、委派任务、拿回结果——任何一方都不必暴露自己的内部工具、记忆或提示词。

## 定位：与 MCP 的关系

> MCP is vertical（纵向），A2A is horizontal（横向）。MCP inside agents, A2A between agents.

| 维度 | MCP | A2A |
|---|---|---|
| 连接 | Agent ↔ 工具/数据/提示 | Agent ↔ Agent |
| 对端是什么 | 有明确输入输出的工具 | 会推理、规划、保持自身状态的自主 Agent |
| 谁控制 | MCP 客户端逐次指挥每次调用 | 收到任务的 Agent 自己决定怎么完成 |
| 可见性 | Agent 看到工具的全部接口/schema | Agent 彼此不透明，只宣告技能、返回结果 |
| 发现方式 | 客户端列出 server 的工具 | 读取 Agent Card |
| 工作单元 | 一次工具调用（带参数与结果） | 一个带生命周期的 task（status/messages/artifacts） |
| 典型延迟 | 毫秒~秒 | 秒~天（可能含人工审批） |

两者不是竞争关系，严肃系统通常都用：用 MCP 给每个 Agent 装备能力，用 A2A 让跨团队/跨厂商的 Agent 协作。例子：采购 Agent 用 MCP 读库存数据库，用 A2A 找供应商的销售 Agent 下单，供应商 Agent 又用 MCP 查自己的仓库和定价系统。

## 历史与治理

- Google 2025 年 4 月发布，50+ 技术伙伴；6 月捐给 Linux Foundation。
- IBM 的 ACP（Agent Communication Protocol）2025 年 8 月并入 A2A。
- **v1.0 于 2026 年 3 月发布**：加入密码学签名的 Agent Card（接收方可验证卡片确实来自域名所有者）、多租户、若干协议绑定。
- 2026 年 8 月 A2A 加入 Agentic AI Foundation（与 MCP 同一 HOME）。150+ 组织支持。

## 核心构件

### Agent Card

JSON 文档，宣告"我是谁、能做什么、怎么联系我、如何认证"。标准位置 `/.well-known/agent-card.json`。签名卡片可验证来源真实性。

### Task

工作以带生命周期的 task 发送：状态 `submitted → working → input-required → completed`，可数秒完成也可跑数小时并持续状态更新。最终输出称为 **artifact**。

### Messages 与 Parts

Agent 之间交换由类型化 parts（text、file、结构化数据）构成的 messages，并可协商格式。

### Updates

客户端可通过轮询、流式（SSE）或 webhook 获取结果。

## 常用操作（JSON-RPC 绑定）

A2A 规范定义抽象操作，实现映射到 JSON-RPC / gRPC / REST。常见 JSON-RPC 方法：

- `SendMessage` / `SendStreamingMessage`：开启或继续任务（流式变体对长任务发 SSE 更新）。
- `GetTask` / `ListTasks`：轮询或审计跨会话的任务状态。
- `CancelTask`：用户中止工作流时的协作式关闭。
- `GetAgentCard`：委派前的能力发现。

多数集成者从 JSON-RPC over HTTPS + SSE 起步，因为契合现有 API 网关与可观测栈。

## 安全

设计原则"secure by default"：企业级 HTTP 认证方案、不要求泄露内部提示词、任务在工作态支持 human-in-the-loop。

- A2A 安全聚焦"你在和谁对话"：验证 Agent Card、认证远端 Agent、决定可接受/可委派哪些任务。
- 把每个远端 Agent 当作独立的 OAuth resource server，记录 task ID，绝不盲目转发终端用户 token。
- A2A 与 MCP 都面临提示注入（工具或另一 Agent 的内容可能携带隐藏指令）。

## 何时用 A2A

- Agent 必须把工作交给另一个团队/框架/厂商构建的 Agent。
- 多个平台的 Agent 需要协作而非各自为政。
- 客户或伙伴的 Agent 要与你的 Agent 协作（供应商、订单、服务请求跨公司边界）。
- 任务运行时间长、需要跟踪状态而非单次快速调用。

**何时都不需要**：步骤固定且每次相同（普通自动化/集成更便宜）；所有 Agent 都在一个应用、一个框架里（框架自带 handoff 足够）；对端是固定 JSON schema 的确定性微服务（普通 REST 客户端即可）。

> 重要：A2A 标准化的是"信封"，不是规划算法。它不保证正确委派——你仍需要评估、沙箱与成本控制。

> 相关：框架内的交接与通信见 `../handoff/`；MCP 协议细节见 `../../../api/mcp-tools/mcp-tools.md`。
