---
description: "Agent to agent protocol"
描述: "智能体与智能体协议"
name: "Agent to Agent Protocol"
名称: "智能体与智能体协议"
---

# Agent to Agent Protocol
消息：JSON-RPC / gRPC / HTTP+JSON
发现：`Agent Card`（well-known URI）
长任务：Task + SSE 流式 + Webhook 推送

## A2A 核心概念

- **Agent Card**：Agent 的自描述清单——身份、能力、skills、服务端点、鉴权方式、输入输出模态，可带 JWS 签名。客户端先读 card 再决定是否委派。
- **Task**：有状态的工作单元，`submitted → working → completed / failed / canceled`，可中断为 `input-required` / `auth-required`；支持多轮续任务（`taskId` + `contextId`）。
- **Message / Part**：一轮通信，角色 `user` / `agent`；Part 是最小内容单元（text / raw / url / data 四选一）。
- **Artifact**：任务输出，**结果应放在 Artifact 而不是 Message 里**。
- **Context**：把相关任务与消息归到同一会话。
- **更新机制**：轮询 `Get Task`、SSE 流式、Webhook 推送三种。
- **设计要点**：Agent 保持不透明——不共享内部提示词、记忆与工具列表；跨组织委派时这是核心价值。

## 结构
### Interact layer
1. Inbound A2A Server
- SendMessage
- GetTask
- CancelTask
- SubscribeToTask
- ListTasks
- GetExtendedAgentCard
2. Outbount A2A Client
### Momory layer
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
id     text unique required,
status object required
    state required enum submitted → working → completed / failed / canceled | input-required / auth-required
    message
    timestamp
context_id
artifacts
history
metadata


3. Message
messageId
4. Part
kind: text / raw / url / data
5. Artifact
### Protocol layer


## Artifact范式
### 提示词格式约定
### 结构化输出
### 显式Artifact工具
### 运行时捕获
从工作区变更中提取并包装产物。
### 后处理解析
从整段对话抽取结果，容易把解释文字当数据。
### 混合模式
提示词引导+工具校验+解析兜底