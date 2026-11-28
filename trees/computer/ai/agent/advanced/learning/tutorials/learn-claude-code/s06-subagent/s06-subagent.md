---
description: "Subagent：给子任务独立上下文 — lesson 06 of learn-claude-code"
描述: "Subagent：给子任务独立上下文（learn-claude-code 第 06 节）"
name: "S06 Subagent"
名称: "Subagent：给子任务独立上下文"
---

# Subagent：给子任务独立上下文

第 6 节，从单上下文转向委派。

## 问题

为了追踪一条调用链，Agent 读了很多文件；调用链弄清后，这些中间细节仍留在父对话的 `messages` 里，继续占用上下文，干扰后续决策。

## 机制

调用 `task` 时启动一个嵌套 Agent Loop，用全新的 `messages` 处理明确的子任务；子循环结束后，只把最终文本作为父对话的工具结果返回。父上下文看不到子循环的中间工具调用。

## 代码实现

`run_subagent()` 新建消息列表，使用不含 `task` 的五个基础工具，循环最多若干轮；每轮执行工具并把结果回填，最后提取文本。父子共享工作目录和权限 hook，但消息隔离。

## 运行与观察

运行 `python s06_subagent/code.py`，要求“先追调用链，再改代码”。观察父对话只拿到子 Agent 的摘要，而大量读文件过程留在子上下文里。

## 边界

隔离的是消息，不是进程或文件系统；子 Agent 仍会改同一个工作区，也可能与父任务冲突。这里是同步调用，没有并行，也没有独立的预算与审批。

## 一句话

委派隔离的是上下文，不是工作区。

## 参考资料

- 课程 README（第 06 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s06_subagent/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s06_subagent/code.py
