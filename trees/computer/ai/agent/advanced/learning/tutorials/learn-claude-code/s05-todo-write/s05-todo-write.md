---
description: "TodoWrite：先有计划再执行 — lesson 05 of learn-claude-code"
描述: "TodoWrite：先有计划再执行（learn-claude-code 第 05 节）"
name: "S05 TodoWrite"
名称: "TodoWrite：先有计划再执行"
---

# TodoWrite：先有计划再执行

第 5 节，从执行转向规划。

## 问题

复杂任务做到一半，测试失败会把注意力全部吸走，最初的目标被挤出上下文。对话越长，系统提示的影响力越弱，Agent 容易即兴发挥、漏掉后面的步骤。

## 机制

给 Agent 一个 `todo_write` 工具，把计划变成显式状态：待办、进行中、已完成。连续几轮工具调用没有更新计划时，Harness 把提醒追加到工具结果里，让计划重新进入注意力。

## 代码实现

`TodoManager` 保存任务列表，校验内容非空、同一时间只有一个 `in_progress`，并把状态渲染成文本。`run_todo_write()` 更新后打印；循环里的 reminder 计数器在多次未更新时注入提醒。

## 运行与观察

运行 `python s05_todo_write/code.py`，给一个多步重构任务。观察 Agent 先列步骤，再逐项推进；当它长时间不更新计划时，提醒如何出现。

## 边界

计划不是调度器：它不表达依赖、不持久化，也不保证模型一定遵守。它解决的是注意力锚点，不是任务执行的正确性。

## 一句话

先列步骤再执行，长任务才有锚点。

## 参考资料

- 课程 README（第 05 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s05_todo_write/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s05_todo_write/code.py
