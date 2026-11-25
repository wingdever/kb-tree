---
description: "Agent Client Protocol: the editor-to-coding-agent interface used by Zed and other clients"
描述: "智能体客户端协议：编辑器与编码 Agent 之间的会话接口"
name: "Agent Client Protocol"
名称: "智能体客户端协议"
---

# Agent Client Protocol

ACP 定义的是**编辑器与编码 Agent 之间**的接口：编辑器是客户端，Agent 作为子进程被拉起，双方用 JSON-RPC over stdio 通信。它不解决工具调用，也不解决 Agent 之间的协作，只管「宿主界面 ↔ 编码 Agent」这一段。

## 它规定了什么

- **会话生命周期**：初始化协商能力、创建会话、加载历史、取消当前轮次、关闭会话。
- **输入与输出**：客户端把用户消息、文件上下文、图片等多模态内容发给 Agent；Agent 以流式事件回传文本片段、思考片段、工具调用与完成状态。
- **权限请求**：Agent 执行写文件或跑命令前，向客户端发起权限询问，由编辑器弹出确认；这是 ACP 与「静默执行」类协议的关键差别。
- **文件系统与终端**：读写文件、列目录、执行命令都经由客户端转发，因此权限边界由宿主掌握，而不是 Agent 自己。

## 与另外两个协议的分工

MCP 连的是 Agent 与工具、数据源；A2A 连的是 Agent 与 Agent；ACP 连的是编辑器与单个编码 Agent。三者可以叠加：编辑器用 ACP 驱动 Agent，Agent 再用 MCP 取工具，遇到其他团队的 Agent 才引入 A2A。

## 同名消歧

`ACP` 在 2025 年前后指过三个不同的事物：Zed 的 Agent Client Protocol、IBM Research 的 Agent Communication Protocol（已并入 A2A）、以及若干厂商自用的内部协议名。写设计文档时应写全称，不要只写缩写。

## 采用现状

Zed 发起并主导，Apache 许可，社区共建。Gemini CLI 是最早的参考实现，Claude Code、Codex、GitHub Copilot 等也在 ACP 生态内；JetBrains 侧已接入。2026 年 7 月发布 v2 草案，重点是把更多会话状态表达出来、统一此前分散的模式。

它是「把 Agent 嵌进 IDE」这一层的事实标准候选，但版本迭代快、能力协商依赖双方实现，跨客户端行为不完全一致；v1 与 v2 的能力差异要按客户端实际支持情况核对。

## 参考资料

- ACP 规范与协议仓库（Apache 许可）：https://agentclientprotocol.com
- 协议实现仓库：https://github.com/agentclientprotocol/agent-client-protocol
- Zed Agent Client Protocol 文档：https://zed.dev/acp
