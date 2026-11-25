---
description: "Agent Client Protocol: the editor-to-coding-agent interface used by Zed and other clients"
描述: "智能体客户端协议：编辑器与编码 Agent 之间的会话接口"
name: "Agent Client Protocol"
名称: "智能体客户端协议"
---

# Agent Client Protocol

ACP 定义的是**编辑器与编码 Agent 之间**的接口：编辑器是客户端，Agent 通常作为子进程被拉起，双方用 JSON-RPC 通信。它不解决工具调用，也不解决 Agent 之间的协作，只管「宿主界面 ↔ 编码 Agent」这一段。

## 它规定了什么

- **会话生命周期**：初始化协商能力、新建或恢复会话、加载历史、取消当前轮次、关闭会话。
- **输入与输出**：客户端把用户消息、文件上下文、图片等多模态内容发给 Agent；Agent 以流式通知回传文本片段、思考片段、工具调用与完成状态。
- **权限请求**：Agent 执行写文件或跑命令前，向客户端发起权限询问，由编辑器弹出确认。这是 ACP 与「静默执行」类协议的关键差别。
- **文件系统与终端**：读写文件、列目录、执行命令都经由客户端转发，权限边界由宿主掌握，而不是 Agent 自己。

## 通信模型

JSON-RPC 2.0，两种消息：**method**（请求—响应，带 result 或 error）与**notification**（单向，不期待响应）。四条与基础 JSON-RPC 的差异值得记住：

- request id 必须是字符串或整数，不能是 `null`；只有无法确定 id 时才回 `id: null` 的错误。
- 双向都能发请求，两侧各自分配 id，同一个 id 可以在两个方向同时存在。
- **不支持 batch**，一条消息一个对象。
- 除初始化响应外，Agent 可以在任意时刻主动发请求或通知，客户端不能假设「我发了请求就只会收到响应」。

## 方法地图

| 阶段 | 方法 | 谁发起 | 要点 |
|---|---|---|---|
| 初始化 | `initialize` | Client | 协商版本与能力；`info` 是自报的，不可用于安全决策 |
| 鉴权 | `auth/login`、`auth/logout` | Client | 只在 Agent 声明了鉴权方式时可用 |
| 会话 | `session/new`、`session/resume` | Client | 创建或恢复；恢复可要求重放历史 |
| 会话管理 | `session/list`、`session/delete`、`session/close` | Client | 列出、删除、关闭 |
| 提示 | `session/prompt`、`session/cancel` | Client | 提交用户回合；取消前台工作 |
| 事件 | `session/update` | Agent | 所有流式内容与状态变化都走这一条通道 |
| 权限 | 权限请求（`session/request_permission` 一类） | Agent | 由 Agent 发起，客户端给选项，Agent 必须遵守结果 |
| 反问 | elicitation | Agent | 向用户请求结构化信息，区别于自由文本追问 |
| 宿主能力 | `fs/*`、`terminal/*` | Agent 请求 Client | 受限方法，作用域限于会话根目录 |
| 子会话 | `subagent_update` + 受限方法 | Agent | Agent 声明的子会话，Client 不创建也不关闭 |

## 提示生命周期：响应不等于完成

这是接入时最容易搞错的一点。`session/prompt` 的响应只表示**用户消息已被插入会话**，不是任务完成。之后的一切都通过 `session/update` 通知推送：

- 前台工作可能跨多次模型调用与多次工具调用，结束时发一个 `idle` 状态与 stop reason。
- 前台与后台是两个概念：Agent 报告 `idle` 时，后台任务可能仍在跑。
- 断线重连后，即使带同一个幂等键重发，也不保证不会二次插入——重试语义由 Agent 实现决定，不能当成事务。

`session/update` 的事件族按对象分：用户消息块、Agent 消息块、思考块、工具调用及其内容流、终端输出、计划（`plan_update` / `plan_removed`）、可用命令、配置项、用量、上下文压缩、子会话、以及历史重放结束标记。客户端遇到不认识的事件应**原样保留并忽略**，不要丢弃，否则历史回放会缺块。

实体 id 只在**同类型内唯一**：消息、工具调用、终端、计划各有自己的 id 空间，同一个字符串可以同时是消息 id 和工具调用 id。

## 会话生命周期

- 会话从 `session/new` 或 `session/resume` 起变为**活跃**，到 `session/close` 或连接结束为止。
- 活跃会话上的会话级请求（prompt、改配置）才合法，否则返回 `-32002`（未知会话）；`session/cancel` 对不活跃会话被忽略，不报错。
- 会话被关闭不代表被删除：是否还能 `list` 出来、还能否 `resume`，取决于 Agent 的保留策略。
- 同一个会话能否同时活跃在多个连接上，由 Agent 决定；不允许时可以在新连接 resume 时踢掉旧连接。

## 传输

目前正式定义的只有 **stdio**：客户端拉起子进程，逐行 NDJSON，Agent 的 stdout **只能**输出合法 ACP 消息，日志一律走 stderr。结束连接的方式是关闭 stdin；Agent 应当收尾后自行退出，超时才由客户端 `SIGTERM` / `SIGKILL`。

基于 Streamable HTTP 的远程传输仍在 RFD 阶段，尚未成为正式传输。所以把 ACP Agent 放到云端，需要一层桥接：由服务端进程扮演「客户端」，把 stdio 会话接进自己的事件流。

## 权限与信任模型

ACP 自己**不做沙箱**：Agent 以它被赋予的进程权限运行。协议能做的只有三件事：

1. 让 Agent 在关键动作前请求许可，并**必须**遵守 `reject_once` / `reject_always` 的结果。
2. 把文件与命令能力放到客户端一侧，用会话根目录限制作用域。
3. 要求客户端把 Agent 产出的内容当**不可信内容**渲染：不执行脚本、不自动打开链接、不自动抓取 Agent 给的远程 URI、在路径与命令里显示双向控制字符。

反过来，客户端也拦不住一个恶意 Agent——协议层没有强制力。真正的隔离要靠进程权限、容器与网络策略，这一点和「工具沙箱」是两件事。

## 与另外两个协议的分工

MCP 连的是 Agent 与工具、数据源；A2A 连的是 Agent 与 Agent；ACP 连的是编辑器与单个编码 Agent。三者可以叠加：编辑器用 ACP 驱动 Agent，Agent 再用 MCP 取工具，遇到其他团队的 Agent 才引入 A2A。

## 同名消歧

`ACP` 在 2025 年前后指过三个不同的事物：Zed 的 Agent Client Protocol、IBM Research 的 Agent Communication Protocol（已并入 A2A）、以及若干厂商自用的内部协议名。写设计文档时应写全称，不要只写缩写。

## 采用现状

Zed 发起并主导，Apache 许可，社区共建。Gemini CLI 是最早的参考实现，Claude Code、Codex、GitHub Copilot 等也在 ACP 生态内；JetBrains 侧已接入。协议已从 v1 演进到 v2：v2 补齐了提示生命周期、会话恢复与重放、子会话、反问、用量与压缩等此前分散或缺失的语义，并提供了迁移指南。

它是「把 Agent 嵌进 IDE」这一层的事实标准候选，但版本迭代快、能力协商依赖双方实现，跨客户端行为不完全一致；v1 与 v2 的能力差异要按客户端实际支持情况核对。

## 实现清单

1. stdout 只写协议消息，日志走 stderr——否则解析器在第一条日志处就崩。
2. 把 `session/prompt` 的响应当「已接收」，最终结果等 `idle`。
3. 处理 `-32002`：会话不存在或已失效时，重新 `session/resume` 或 `session/new`，不要重试 prompt。
4. 权限被拒后不得执行，并把这个决定写进会话历史。
5. 未知事件原样保留，重放时按 id 拼回。
6. 恢复会话时要求重放历史，直到收到重放结束标记再渲染当前状态。
7. 云端部署先解决 stdio 桥接与进程生命周期，不要假设有远程传输。

## 常见失败

- 把「收到 prompt 响应」当成任务完成，界面提前显示结束。
- Agent 往 stdout 打调试日志，客户端 JSON 解析失败。
- 权限请求被当成建议，用户点了拒绝仍然执行。
- resume 后直接渲染新事件，历史与当前状态错位。
- 假设会话只能在单连接活跃，多端接入时互相踢掉。
- 把 Agent 自报的 `info`（名称、版本）用于鉴权或安全判断。

## 参考资料

- ACP v2 协议总览（通信模型、双向方法、方法基线）：https://agentclientprotocol.com/protocol/v2/overview
- ACP v2 提示生命周期（accepted 语义、`session/update` 事件族、实体 id）：https://agentclientprotocol.com/protocol/v2/prompt-lifecycle
- ACP v2 会话建立与恢复（活跃会话、重放、`-32002`）：https://agentclientprotocol.com/protocol/v2/session-setup
- ACP v2 传输（stdio 细则、日志与关闭、HTTP 传输仍在 RFD）：https://agentclientprotocol.com/protocol/v2/transports
- ACP v2 安全考量（信任模型、渲染与 URI 规则、提示注入）：https://agentclientprotocol.com/protocol/v2/security
- ACP 文档总索引（v1/v2 全部分页与迁移指南）：https://agentclientprotocol.com/llms.txt
- 协议实现仓库（Apache 许可）：https://github.com/agentclientprotocol/agent-client-protocol
