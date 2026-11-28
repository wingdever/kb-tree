---
description: "Hooks：挂在循环上，不写进循环里 — lesson 04 of learn-claude-code"
描述: "Hooks：挂在循环上，不写进循环里（learn-claude-code 第 04 节）"
name: "S04 Hooks"
名称: "Hooks：挂在循环上，不写进循环里"
---

# Hooks：挂在循环上，不写进循环里

第 4 节，把边界与日志从循环里移到扩展点。

## 问题

权限检查、日志、自动 git add 每加一个，就往 `agent_loop` 里塞一行。扩展越来越多，核心循环越来越难读，最后认不出哪一段才是 Agent 的基本结构。

## 机制

引入四个生命周期事件：`UserPromptSubmit`、`PreToolUse`、`PostToolUse`、`Stop`。扩展通过注册表挂到事件上，循环只调用 `trigger_hooks()`；权限检查从循环体移到 `PreToolUse`。

## 代码实现

`HOOKS` 是事件到回调列表的字典，`register_hook()` 追加回调，`trigger_hooks()` 依次执行。循环保持稳定，扩展逻辑放在注册函数里，按事件顺序运行。

## 运行与观察

运行 `python s04_hooks/code.py`，触发一次工具调用。观察权限拒绝、操作日志和大文件提醒都在 hook 里发生，而 `agent_loop` 只负责触发事件。

## 边界

Hook 仍在同一进程内同步执行，异常、超时和顺序都会影响主循环；没有隔离，也没有权限分级。注册顺序本身就是行为的一部分。

## 一句话

扩展点挂在循环外，核心循环才保持稳定。

## 参考资料

- 课程 README（第 04 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s04_hooks/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s04_hooks/code.py
