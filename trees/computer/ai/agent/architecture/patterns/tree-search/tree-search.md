---
description: "Tree-of-Thoughts, GoT, MCTS and LATS deliberate search scaffolds"
描述: "ToT、GoT、MCTS 与 LATS 等审慎搜索脚手架"
name: "Tree Search: ToT, GoT, MCTS, LATS"
名称: "树搜索"
---

# 树搜索：ToT / GoT / MCTS / LATS

当单条推理链不够——多个路径看似都合理、第一个看似合理的路径并非最佳、走进死胡同时——把 Agent 循环提升为搜索树，配合价值函数与回溯。

## Tree of Thoughts（ToT，Yao et al., NeurIPS 2023）

把线性 CoT 推广为对多个推理路径的显式探索：每步生成多个候选思路，对部分状态打分，剪掉弱分支，扩展有希望的分支，直到停止条件。

- 推理变成**有向导引的搜索**：回溯显式、分支质量可测、最终答案从竞争候选中选而非第一个轨迹。
- 关键依赖：**评估函数质量**决定性能。外部验证器（代码执行、测试）优于自我反思打分。
- 变体：BFS（穷举）、DFS（深度、内存有限）、Beam search（内存受限 + 好启发式）。
- 数字：Game of 24 上 CoT 4% vs ToT 74%；Game of 24 论文未发布 token 倍数，但显式树比 CoT 贵得多。
- 2026 语境：o1 等推理模型已在推理时内化大量这种审慎搜索，显式 ToT scaffold 更多留给"验证器引导"工作与非前沿模型。

## Graph of Thoughts（GoT，Besta et al., AAAI 2024）

树只允许分支与回溯（每个思路一个父节点）；图增加**聚合**——一个节点可有多个父节点（N 对 1 合并）与循环（精炼回路），部分解可以组合与改进。在可组合任务（如排序）上，AAAI-24 论文报告 GoT 比 ToT 质量 +62%、成本降 31%+。若子结果不能组合，图的额外机制买不到收益。

## MCTS 与 LATS

**MCTS（Monte Carlo Tree Search）**：用模拟 rollout 与价值反向传播。不只是"有分数的 ToT"——它保存多次访问的统计，以树策略决定下一份搜索算力投向哪里。

**LATS（Language Agent Tree Search，Zhou et al., ICML 2024）**：统一 ReAct + Reflexion + MCTS。LLM 同时充当 agent、价值函数（给状态打分）、优化器（选最佳轨迹）。

- 节点保存：环境状态、动作历史、观察、反思、价值估计、访问统计。
- 迭代：Select → Generate candidate actions → Execute/Simulate → Observe → Evaluate & Reflect → Update statistics → Expand/Revisit/Backtrack。
- 环境反馈是核心：代码修复的"候选补丁→跑测试→观察失败→更新分支价值"，浏览器交互的"候选点击→新 DOM→衡量进展"。
- 数字：HumanEval 上 GPT-4 达 94.4% pass@1，优于 ReAct、Reflexion、CoT、ToT。成本高——约 71 次 LLM 调用/请求，而标准 ReAct 约 9 次。
- 前提：有廉价可靠的价值函数。

## 何时用 / 何时不用

**用**：复杂规划、数学、代码任务且第一条路径常失败；有好的评估函数或外部验证器；任务真正分支多；需要显式回溯。

**不用**：简单线性任务；延迟或 token 预算紧张（显式树显著贵于 CoT）。

## 最重要的前提

任何审慎搜索方法（ToT/GoT/MCTS）都依赖能廉价可靠地给部分状态打分。若无法用验证器、单元测试、启发式或价值函数产出该信号，搜索就是"在黑暗中探索"。**先建评估器，再建树**。

研究还发现：生成器比判别器重要得多——提升模型提出好思路的能力帮助大，提升其判断能力帮助有限。

## 参考资料

- Tree of Thoughts（arXiv:2305.10601）：https://arxiv.org/abs/2305.10601
- Graph of Thoughts（arXiv:2308.09687）：https://arxiv.org/abs/2308.09687
- Language Agent Tree Search（LATS，arXiv:2310.04406）：https://arxiv.org/abs/2310.04406
