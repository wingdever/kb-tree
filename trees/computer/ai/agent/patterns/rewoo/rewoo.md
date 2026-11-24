---
description: "Plan once with placeholder variables, then execute without observations"
描述: "先规划占位变量 DAG 再执行、不让规划器看观察结果的模式"
name: "ReWOO: Reasoning Without Observation"
名称: "ReWOO 无观察推理"
---

# ReWOO：无观察推理（Reasoning WithOut Observation）

ReWOO 把规划集中在一次前置调用中完成：规划器生成带占位变量的完整 DAG， worker 执行工具并代入观察， solver 读一次最终轨迹产出答案。**规划器永不看工具输出**。

## 要解决的问题：ReAct 的规划税

在 ReAct 循环里，每次工具观察都会回灌到规划器提示，供下一轮推理——token 成本随步数近似**平方增长**，因为每轮都携带此前所有轮次的轨迹。八步任务里，规划器把自己的草稿和所有先前观察重读七次，而多数重读并不改变计划（结构本可事先知道）。

## 三个角色

1. **Planner（LLM 调用 1）**：输出完整计划 DAG，步骤用变量引用，如 `t1 = Search(x); t2 = Summarise(#t1)`。`#E1`、`#E2` 是尚未知道的工具结果占位符。
2. **Worker（无 LLM）**：按依赖顺序执行工具，把观察代入证据变量。
3. **Solver（LLM 调用 2）**：读取解析后的轨迹（任务 + 紧凑的证据列表），产出最终答案。

模型总共只调用约 **2 次**，且从不读原始观察。

## 效果数字

- 论文报告：多步基准上 token 减少约 **5×**，准确率相当或更好。
- HotpotQA：ReWOO 用 2000 token 达 42.4% 准确率，ReAct 用 10000 token 达 40.8%（IBM）。
- HotpotQA 上少用 64% token、准确率提升 4.4%。
- 六步任务的演示计算：ReAct ~9300 token vs ReWOO ~2800 token，约 3.3×；节省随步数增长（ReAct 近似平方，ReWOO 近似平坦）。

## 禁忌与权衡

- **放弃适应性**：计划在任何结果看到之前就固定。如果第三个工具返回意外数据（歧义实体、错误、空结果），僵化的计划无法察觉与改道。
- 占位符替换需要**类型化变量约定**。
- 计划正确率必须高；中途重规划会抵消节省。
- 适合：结构由任务决定而非由前一步返回决定的任务、高吞吐量批处理和（如数千文档做相同多步处理）。
- 不适合：探索性任务（每个观察真正改变策略）——用 ReAct/Reflexion 或混合。

## 在模式图谱中的位置

- **特化 Plan-and-Execute**：用占位变量 DAG 把规划与观察彻底解耦，比一般 Plan-and-Execute 更省。
- **被 LLMCompiler 泛化**：把 ReWOO 的 plan-as-DAG 用任务分发器并行执行独立步骤，原论文声称比顺序执行快 3.6×。

> 相关：Plan-and-Execute 见 `../plan-exec/`；ReAct 见 `../react/`。
