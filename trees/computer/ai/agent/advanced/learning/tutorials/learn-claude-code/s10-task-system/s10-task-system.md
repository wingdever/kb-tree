---
description: "Task System：从清单到任务图 — lesson 10 of learn-claude-code"
描述: "Task System：从清单到任务图（learn-claude-code 第 10 节）"
name: "S10 Task System"
名称: "Task System：从清单到任务图"
---

# Task System：从清单到任务图

第 10 节，把清单升级为任务图。

## 问题

TodoWrite 只有内容和状态，不能表达“数据库表完成后才能写 API，API 定了才能补测试”，也不能记录谁负责、哪些任务被阻塞。

## 机制

每个任务是一个带 ID 的持久记录，包含主题、描述、状态、负责人和 `blockedBy` 依赖。创建、更新、列举、认领、完成都通过工具完成；只有依赖完成的任务才能被认领。

## 代码实现

`Task` dataclass 保存字段；`TaskStore` 在 `.tasks/` 下读写 JSON，ID 使用固定前缀加随机十六进制；`create_task()` 先建节点，`update_task(addBlockedBy=...)` 再用运行时 ID 建边；`can_start()` 检查依赖。

## 运行与观察

运行 `python s10_task_system/code.py`，创建三个有前后依赖的任务。观察依赖未完成时任务不可认领，前置完成后状态如何解锁。

## 边界

这是单机文件存储，缺少跨进程事务与锁；它表达依赖，但不会自动调度，也不会替你判断任务拆得对不对。任务图错了，执行越快错得越远。

## 一句话

任务图让目标跨会话存在，让依赖可计算。

## 参考资料

- 课程 README（第 10 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s10_task_system/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s10_task_system/code.py
