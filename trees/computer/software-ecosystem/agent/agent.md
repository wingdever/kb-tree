---
description: "Agent sub-ecosystem: vendors, harnesses, frameworks, protocols, distribution and governance"
描述: "Agent 子生态：厂商、harness、框架、协议、分发与治理"
name: "Agent Sub-ecosystem"
名称: "Agent 子生态"
---

# Agent 子生态

> 来源：AAIF 官网、各厂商文档与 2026 年生态盘点。版本与项目清单变化快，以官方页面为准。

Agent 已成形为一个软件品类：有厂商、有运行时、有协议栈、有分发渠道、有中立治理机构。本页是**生态视角**——讲这个品类怎么组织起来；本页不重复。

## 生态版图

| 类别 | 代表 | 形态 |
|---|---|---|
| 编码 Agent | Claude Code、OpenAI Codex、Cursor、Cline、OpenCode、Gemini CLI、Qoder CN、CodeBuddy | IDE 插件 / CLI / 云任务；事实上的主战场 |
| 通用 Agent | ChatGPT Work、Claude Cowork、Gemini 的 agent 模式 | 跨文件、桌面与云应用完成交付物 |
| 知识 Agent | 腾讯 ima ||
| 渠道型 | OpenClaw、Hermes、nanobot | 常驻 + 消息渠道（29+ 渠道、 skills、持久会话） |
| 开放栈 | AAIF 治理下的 MCP / A2A / goose / AGENTS.md / agentgateway | 指令 → 运行时 → 工具 → Agent 间 → 流量 |
| 基础设施 | LangGraph、LangSmith、Agent Router、OpenEnv / OpenSandbox | 编排、可观测、路由、沙箱 |

## 共有维度

| 维度 | 生态层的问题 | 机制入口 |
|---|---|---|
| 身份与凭证 | 谁的账号、什么权限、如何审批 ||
| 工具与协议 | MCP 接工具、A2A 接 Agent、ACP 接编辑器 ||
| 上下文与技能 | AGENTS.md / SKILL.md / Hooks / 记忆文件 ||
| 运行与沙箱 | 本地 CLI、容器、云任务、工作树隔离 ||
| 评估与可观测 | 轨迹、黄金集、成本与延迟 ||
| 分发 | IDE 市场、npm / skills.sh、消息渠道、云 Runner ||

## 治理与收敛

- **协议战争以中立治理收场**：MCP、A2A、AGENTS.md、goose 等同处 Linux Foundation 下的 Agentic AI Foundation，八家竞争公司共同资助。
- **标准化不等于互操作**：线路格式统一了，语义与实现质量仍归各团队；厂商差异上移到运行时与界面，那里才是真正的切换成本。
- **技能成为新包形态**：skills.sh 一类注册表让能力可安装、可排行、跨 Agent 复用。
- **切换成本从重写降为迁移**：基于开放标准构建，不要把架构绑在某家专有集成格式上。

## 与其他子生态的关系

- IM / 协作办公是 Agent 的**入口渠道**：人在这里下达目标与审批。
- 开发工具与代码托管是 Agent 的**工作现场**：编辑器、终端、仓库、PR 构成执行面。
- 浏览器与桌面是**无 API 系统的兜底行动面**。

## 一句话主线

**Agent 子生态由「编码 Agent 主战场 + 开放协议栈 + 中立治理 + 多渠道分发」构成；机制看 `ai/agent/`，生态看本页。**

