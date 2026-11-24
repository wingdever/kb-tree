---
description: "MDP, value methods, policy gradients, actor-critic and PPO/GAE"
描述: "MDP、值方法、策略梯度、Actor-Critic 与 PPO/GAE"
name: "Reinforcement Learning Foundations"
名称: "强化学习基础"
---

# M7 强化学习基础

> 与 advanced/A10（Agent 训练与 RL）衔接：A10 聚焦"如何训练工具使用 Agent"（RLVR/GRPO/多轮 rollout），本篇补上底层 RL 概念与经典算法——理解 GRPO/PPO 之前的必要基础。

## 什么是强化学习

RL 是智能体通过与环境试错交互、最大化累积奖励来学习序贯决策的范式。核心是**智能体—环境反馈循环**：观察状态 → 按策略选动作 → 获得奖励与新状态 → 更新策略。目标是学到使期望未来回报最大的策略 π（状态到动作的映射）。

## MDP（马尔可夫决策过程）

RL 问题形式化为元组 **(S, A, P, R, γ)**：

- S：状态空间；A：动作空间
- P(s'|s,a)：状态转移概率
- R(s,a,s')：奖励函数
- γ：折扣因子（0≤γ<1）

**马尔可夫性质**：未来只依赖当前状态，与之前的历史无关——`P(s_{t+1}|s_t,a_t,s_{t-1},...,s_0) = P(s_{t+1}|s_t,a_t)`。

回报（return）：`G_t = Σ_k γ^k r_{t+k}`。价值函数 V(s) 预测状态的长期价值；动作价值 Q(s,a) 预测状态-动作对的价值。

## 探索 vs 利用

- **利用（exploitation）**：选当前已知最优动作。
- **探索（exploration）**：尝试不确定动作以获取信息。

常见策略：ε-greedy（小概率随机）、乐观初始化（高估未试动作）、UCB（按估计不确定性平衡）、内在动机（好奇心奖励新颖状态）。训练初期 ε 高、逐步降低；评估时几乎不探索。

## 算法分类

| 维度 | 类别 |
|---|---|
| 是否学环境模型 | Model-Based（Dyna-Q、AlphaZero、MBPO）/ Model-Free（Q-learning、PPO） |
| 学什么 | Value-Based（Q-learning、DQN）/ Policy-Based（REINFORCE、PPO） |
| 数据来源 | On-Policy（SARSA、A2C）/ Off-Policy（Q-learning、DQN） |
| 状态表示 | Tabular / Function Approximation（深度 RL） |

## 值方法

### Q-Learning

model-free、off-policy，学最优动作价值函数。更新规则（TD learning）：

```
Q(s,a) ← Q(s,a) + α [ r + γ·max_{a'} Q(s',a') − Q(s,a) ]
```

括号里是 **TD 误差**：预测与实际（奖励 + 折扣的下状态最大 Q）之差。一定条件下概率 1 收敛到最优 Q。

### DQN（Deep Q-Network）

用深度网络近似高维状态（如图像）的 Q 值，输入状态、输出每个离散动作的 Q。两项稳定化创新：

1. **经验回放（Experience Replay）**：存转移 (s,a,r,s',done) 到 buffer，随机小批采样，打破连续样本的时间相关性、复用经验。
2. **目标网络（Target Network）**：周期性从在线网络复制的延迟副本，提供稳定的 TD 目标 `y = r + γ(1−done)·max_{a'} Q_{θ'}(s',a')`，避免"目标随参数移动"的反馈环。

DQN 仅用原始像素在 49 款 Atari 中的 29 款达人类水平。局限：replay 保留过时经验、目标网络更新慢、网络可能对未充分探索状态过度泛化——平滑 loss 曲线不证明策略安全。

## 策略梯度方法

直接参数化并优化策略 πθ(a|s)，对期望回报做梯度上升。REINFORCE 估计器：

```
∇θ J(θ) ≈ Σ_t ∇θ log πθ(a_t|s_t) · G_t
```

直观：高回报 episode 里的动作提高概率，低回报的降低。∇logπ 给方向，G_t 定功劳/责任。REINFORCE 简单但**方差大**——一次幸运结果会让之前所有动作都显得好。

**Baseline / 优势函数**：用 `A_t`（该动作比策略在该状态的通常期望好多少）替代 G_t 降方差。

## Actor-Critic

混合架构，现代复杂 RL 的主导范式：

- **Actor（策略网络）**：选动作。
- **Critic（价值网络）**：用 TD 误差评估动作、给 Actor 提供低方差信号。

代表：A2C/A3C（优势 Actor-Critic）、DDPG、SAC、TD3。Critic 作为 baseline 降策略梯度方差，比纯策略梯度更稳定、样本效率更高。

## PPO（近端策略优化）

实践中**最常用**的策略梯度算法：实现简单、样本效率与鲁棒性平衡好，是 RLHF 训练语言模型的默认算法。

用新旧策略概率比限制更新幅度：

```
r_t(θ) = πθ(a_t|s_t) / π_old(a_t|s_t)

L^CLIP(θ) = E[ min( r_t(θ)·Â_t,  clip(r_t(θ), 1−ε, 1+ε)·Â_t ) ]
```

ε 典型 0.2。正优势时提高概率只在 clip 范围内有用；负优势时 clip 限制进一步下降。这减少异常好/坏 batch 造成的破坏性更新。剪裁目标提供性能改进的下界保证。

> 注意：PPO 的 clip **不是安全保证**，也不证明两策略在所有意义下接近。rollout 长度、优势估计、奖励尺度、熵、环境都重要。

## GAE（广义优势估计）

PPO 常用 GAE 计算 Â_t，在偏差与方差间用参数 λ 权衡（多步 TD 残差的指数加权）。λ=0 低方差高偏差（一步 TD），λ=1 高方差无偏（Monte Carlo），常用 0.95。

## 其他家族

- **Model-Based RL**：学环境动态模型后规划（MPC、MCTS、AlphaZero），样本效率高但易被模型误差利用。
- **层次 RL（HRL）**：把长周期任务分解为选项（options），多时间尺度学习、利于迁移。
- **Offline RL**：从固定数据集学策略，挑战是分布偏移——策略可能遇到数据中没见过的状态动作对，需保守约束偏离。
- **逆向 RL（IRL）**：从专家示范反推奖励函数（最大熵 IRL、GAIL）。
- **多智能体 RL（MARL）**：CTDE（集中训练、分散执行）、MADDPG、QMIX、MAPPO。
- **进化策略**：CMA-ES 等黑盒优化，不需梯度、高度可并行。

## 常见问题与对策

- **稀疏奖励**：只有到达目标才有奖励，其余全 0，随机探索难见成功轨迹。对策：奖励塑形（须保持真实目标）、课程学习（从近目标开始）、示范、长周期探索方法。
- **奖励黑客 / Goodhart 定律**：Agent 优化被测量的代理指标而非真实目标（见 M6、advanced/A7）。
- **分布偏移**（离线 RL）：限制策略偏离行为数据太远。

## 与语言模型对齐的衔接

经典 RLHF 链路：SFT → 训练奖励模型（人类偏好对）→ PPO 优化策略。2026 年主流转向 **RLVR（可验证奖励）+ GRPO**：跳过奖励模型，用验证器（测试通过、数学答案正确、工具参数合规）当奖励，GRPO 用组内相对优势替代 PPO 的 value network，省内存、少超参、更适合推理与工具使用。DPO 则是离线偏好对优化，不做 rollout。详见 advanced/A10。
