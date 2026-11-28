---
description: "Agent Harness 集成：多种机制，一个循环 — lesson 15 of learn-claude-code"
描述: "Agent Harness 集成：多种机制，一个循环（learn-claude-code 第 15 节）"
name: "S15 Integrated Harness"
名称: "Agent Harness 集成：多种机制，一个循环"
---

# Agent Harness 集成：多种机制，一个循环

第 15 节，把前面机制装进一个循环。

## 问题

前十几节把机制拆开讲，每一节都能单独运行；但真实 Agent 需要工具、权限、hook、计划、技能、记忆、压缩、后台、Cron、团队与 MCP 同时存在，还要处理 API 错误。

## 机制

不引入新机制，而是规定每个组件在循环中的位置：LLM 前做通知注入、压缩与 system prompt 组装；工具前后跑 hook 与权限；失败时做重试、token 升级与补救压缩。所有事件仍回到同一段 `messages`。

## 代码实现

`agent_loop()` 串起 `UserPromptSubmit`、cron/background 通知、压缩管线、memory/skills/MCP 状态、模型调用、权限与工具分发、`PostToolUse`；错误恢复处理限流、过载、输出截断和上下文超限。

## 运行与观察

运行 `python s15_integrated_harness/code.py`，依次触发工具、记忆、技能、后台任务和一次失败重试。观察多条机制如何在同一轮对话里协作，而不是各自开一条循环。

## 边界

这是集成参考实现，不是生产产品：状态多在内存，MCP 是模拟的，多租户、持久化、审计与真实沙箱都没有覆盖。组件越多，顺序与相互影响越难排查。

## 一句话

Harness 的复杂度在循环外，循环本身仍然只有几行。

## 参考资料

- 课程 README（第 15 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s15_integrated_harness/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s15_integrated_harness/code.py
