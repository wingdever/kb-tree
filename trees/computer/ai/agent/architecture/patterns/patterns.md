---
description: "Vocabulary of core agent architectures and design patterns"
描述: "Agent 架构模式词汇表：ReAct、Plan-Execute、Reflexion 等"
name: "Core Architectures and Design Patterns"
名称: "核心架构与设计模式"
---

# 核心架构与设计模式

这一章是 Agent 设计的「词汇表」。少数几种模式覆盖了绝大多数真实系统，不必发明新架构；有共识的名字才能讨论「你这个 Agent 到底是怎么转的」。

## 两条主线

**循环与规划**：`ReAct`（交错推理与行动）→ `Plan-and-Execute`（先规划后执行）→ `ReWOO`（规划与观察彻底解耦）→ `树搜索`（多路径探索与回溯）。

**组合与质量**：`Anthropic 工作流模式`（五种可组合的工作流 + 自主 Agent）→ `状态机与 DAG`（用显式图管关键控制流）→ `ACI 与三原则`（工具接口与简洁性）→ `自我修正族`（让输出更可靠）。

## 按任务结构选模式

模式的选择依据是**任务结构**，不是流行度：

| 任务特征 | 优先考虑 | 理由 |
|---|---|---|
| 一步能答、工具明确 | 单次工具调用或提示链 | 循环是纯开销 |
| 要边看边改（搜资料、调外部系统） | ReAct | 观察能修正下一步 |
| 步骤可预判、希望省 token | Plan-and-Execute、ReWOO | 规划一次，执行阶段少带上下文 |
| 答案不唯一、需要比较 | 树搜索（ToT / LATS） | 允许回溯与剪枝 |
| 输出质量要求高、可反复改 | 自我修正族（Reflexion / Self-Refine / CRITIC） | 用外部反馈替代一次成型 |
| 控制流固定且有不可逆动作 | 状态机与 DAG | 可恢复、可审批、可回放 |

## 三条组合规律

- **规划越早，执行越省**：把探索放在规划阶段，执行阶段就不必反复带全量上下文，这是 Plan-and-Execute 与 ReWOO 省 token 的真正来源。
- **反思要外部化**：让同一个模型「再检查一遍」收益有限；接测试、接编译器、接检索验证才有稳定提升。
- **搜索换质量，代价是延迟与成本**：树搜索的收益随分支质量变化，盲目加宽分支只会放大方差。

## 一句要记住的前提

**先建评估器，再加复杂度。** 没有评测就加模式，等于在没有刻度的秤上调味——看起来更精细，实际无法判断是否变好。

## 一句话主线

从最简单的 ReAct 循环起步，按任务结构用 Plan-and-Execute / ReWOO 降本、用工作流模式组合，关键处用状态机接管控制流，用 ACI 原则设计工具，用自我修正与树搜索提质；但每加一层复杂度，都要有评测证明它挡掉了具体的失败。

## 参考资料

- Anthropic《Building effective agents》（五种工作流模式与自主 Agent 的原始划分）：https://www.anthropic.com/engineering/building-effective-agents
- ReAct 论文：https://arxiv.org/abs/2210.03629
- Tree of Thoughts 论文：https://arxiv.org/abs/2305.10601
