---
description: "Workflow Runtime：脚本编排，模型决策 — lesson 16 of learn-claude-code"
描述: "Workflow Runtime：脚本编排，模型决策（learn-claude-code 第 16 节）"
name: "S16 Workflow Runtime"
名称: "Workflow Runtime：脚本编排，模型决策"
---

# Workflow Runtime：脚本编排，模型决策

第 16 节，从模型逐步决策扩展到脚本编排。

## 问题

代码审查这类固定流程要并行检查多个维度、逐条验证、去重、按严重度排序。把步骤只存在对话历史里，顺序、检查点和断点恢复都不可靠。

## 机制

把固定编排写成宿主注册的可信脚本，模型只提供 workflow 名称、参数和可选 runId；脚本用 `agent()`、`parallel()`、`pipeline()`、`phase()` 编排多次 Agent 调用。journal 记录已完成的调用，resume 时未改步骤直接复用缓存。

## 代码实现

`Workflow` 工具进入工具池；`validate_meta()` 校验名称、阶段与权限；`SimpleJsonSchema` 约束结构化输出；运行器把每一步写入磁盘 journal，`resume_from_run_id` 恢复；模型不能提交可执行代码。

## 运行与观察

运行 `python s16_workflow_runtime/code.py`，执行 `review-changes` 或类似 workflow。观察并行分支、阶段事件、结构化结果，以及中断后用 runId 续跑时哪些调用直接命中缓存。

## 边界

脚本是宿主可信代码，不是模型生成代码；journal 在本地磁盘，跨机器恢复要额外设计。并发有上限，子 Agent 仍有成本与权限边界，固定编排也不适合高度探索的任务。

## 一句话

模型决定单步，脚本决定编排，journal 决定可恢复。

## 参考资料

- 课程 README（第 16 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s16_workflow_runtime/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s16_workflow_runtime/code.py
