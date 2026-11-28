---
description: "Agent Teams：团队运行时与协作协议 — lesson 13 of learn-claude-code"
描述: "Agent Teams：团队运行时与协作协议（learn-claude-code 第 13 节）"
name: "S13 Agent Teams"
名称: "Agent Teams：团队运行时与协作协议"
---

# Agent Teams：团队运行时与协作协议

第 13 节，从单 Agent 扩展到团队运行时。

## 问题

一个 Agent 顺序做配置、认证、测试，耗时长，早期细节还会离开上下文。用户通常只描述目标，不会替运行时设计谁并行、谁审批、结果怎么回来。

## 机制

Lead 负责用户对话与分工提案；队友有独立循环，在 WORK 与 IDLE 间切换；MessageBus 用文件收件箱传递消息、结果与控制事件；共享任务板让空闲队友认领 ready task；可选 worktree 隔离并行修改；计划闸门在批准前阻止修改型工具。

## 代码实现

任务存储加锁并维护分配版本；`advance_assignment_version()` 防止旧认领覆盖新状态；队友循环读取收件箱、认领任务、执行并回传结果；只有 Lead 能改任务图结构。

## 运行与观察

运行 `python s13_agent_teams/code.py`，给一个后端重构目标。观察 Lead 先提出团队并等待确认，队友如何认领任务、回传结果，以及 worktree 如何隔开并行修改。

## 边界

这不是分布式团队：消息与任务都在本机文件系统，进程崩溃与网络分区没有覆盖。并行会放大成本、冲突与权限风险；计划闸门是流程约束，不是安全沙箱。

## 一句话

团队运行时把分工、消息、任务认领和目录隔离变成协议。

## 参考资料

- 课程 README（第 13 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s13_agent_teams/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s13_agent_teams/code.py
