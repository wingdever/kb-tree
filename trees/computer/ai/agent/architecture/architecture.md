---
description: "Agent architectures: reasoning loops, orchestration and action surfaces"
描述: "Agent 架构：推理循环、编排与行动面"
name: "Agent Architecture and Orchestration"
名称: "Agent 架构与编排"
---

# Agent 架构与编排

这一组回答"Agent 内部怎么组织"。少数几种循环与编排模式覆盖了绝大多数真实系统；单 Agent 不够时再按协作模式扩成多 Agent，关键控制流交给状态图，横切关注点用 hooks 拦截。

## 一句话主线

用少数几种循环与编排模式搭起推理骨架，单 Agent 不够时再扩成多 Agent，关键控制流交给状态图，横切关注点用 hooks 拦截。
