---
description: "MCP Tools：发现并调用外部工具 — lesson 14 of learn-claude-code"
描述: "MCP Tools：发现并调用外部工具（learn-claude-code 第 14 节）"
name: "S14 MCP Tools"
名称: "MCP Tools：发现并调用外部工具"
---

# MCP Tools：发现并调用外部工具

第 14 节，从本地工具扩展到外部工具协议。

## 问题

接入文档系统、部署平台，每加一个服务就要手写工具定义、参数格式和调用代码。工具越多，宿主越像一堆重复的适配器。

## 机制

MCP 把能力拆成 server 与 client：server 提供 `tools/list` 与 `tools/call`，Harness 负责连接、命名、权限检查，并把发现的工具组装进当前工具池。新 server 接入后，下一轮模型就能看到新工具。

## 代码实现

`MCPClient` 保存工具定义与 handler；`connect_mcp()` 连接并注册；`assemble_tool_pool()` 把基础工具与 MCP 工具合并；`normalize_mcp_name()` 处理命名冲突；课程用进程内 `docs`、`deploy` 模拟 server。

## 运行与观察

运行 `python s14_mcp_plugin/code.py`，连接文档 server，再要求搜索文档。观察工具在连接后的下一轮出现，调用结果仍以普通 `tool_result` 回到循环。

## 边界

课程只实现进程内模拟，没有真实 transport、鉴权与网络错误处理。外部 server 是新的信任边界：工具描述可能被恶意篡改，权限不能只靠 server 自觉。

## 一句话

MCP 把外部能力变成可发现、可调用的工具池。

## 参考资料

- 课程 README（第 14 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s14_mcp_plugin/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s14_mcp_plugin/code.py
