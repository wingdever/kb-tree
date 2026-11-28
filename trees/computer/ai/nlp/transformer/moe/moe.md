---
description: "Mixture of Experts: sparse conditional activation, routing, load balancing, fine-grained experts and expert parallelism"
描述: "混合专家：稀疏条件激活、路由策略、负载均衡、细粒度专家与专家并行"
name: "Mixture of Experts"
名称: "混合专家（MoE）"
---

# 混合专家（MoE）

MoE 把 Transformer 的密集 FFN 换成**许多并行的专家 FFN + 一个轻量 router**。对每个 token，router 只选 top-k 个专家执行（通常 k=1/2/8），其余不参与计算。核心收益是**解耦总容量与每 token 算力**：600B 参数的 MoE 可以像 30B 密集模型一样便宜地推理。

## 核心机制

每个 MoE 层 = N 个专家 FFN + gating network：

1. token 隐状态乘 router 权重 → N 个标量 logits（每专家一个）。
2. 选 logit 最高的 top-k 专家（k 典型 1/2/8）。
3. token 只经过这 k 个专家。
4. 输出按归一化 gate 分数加权求和。

其余 N−k 专家**消耗内存（权重已加载）但零计算**。

**参数量是错误分析单位**（Sparse Is Not Small）：Mixtral 8x7B 有 47B 参数、每 token 激活 13B；DeepSeek-V3 有 671B、每 token 激活约 37B。每 token FLOPs 由路由决定，不由总参数决定。经验法则：**总参数定内存下限，激活参数定算力上限**。

## 路由策略

| 策略 | 做法 | 特点 |
|---|---|---|
| **Top-k**（经典） | softmax 选最高 k 专家 | Mixtral、Qwen3；需辅助损失做负载均衡 |
| **Top-1 Switch** | 每 token 只送一个专家 | Switch Transformer、Llama 4 Maverick；路由开销极低，用 capacity factor 处理溢出 |
| **Sigmoid + 无损失偏置**（2026 共识） | 每专家动态偏置 b_i 加到 gate logits 再 top-k；过载降偏置、闲置升偏置 | DeepSeek-V3/V4；不引入冲突梯度，1B 规模最大失衡从 0.72 降到 0.04 且困惑度改善 |
| **Expert choice** | 专家选 token 而非 token 选专家 | 完美负载均衡，但因果 LM 中有因果泄漏（用未来信息路由，约 10% 异常 loss 下降）——**无前沿生产模型采用** |
| **Hash / 动态 top-k** | 哈希或动态 k | 更低成本，但 learned specialization 减弱 |

## 负载均衡

router 是学出来的，无约束会**坍塌**：少数专家吃下大多数 token，其余欠训，得到"大而无用"的模型。两种对策：

- **辅助损失**（Mixtral、Switch）：给训练损失加可微惩罚奖励均衡——有效但需细调，过大则模型学会均匀路由而非正确路由。
- **无辅助损失 + 偏置**（DeepSeek-V3）：每专家 bias 在 top-k 选择时动态调整，不污染主损失，将主目标 100% 聚焦语言建模质量。
- **专家容量上限**：每专家每 batch 有 token 硬上限，溢出路由到次优专家；结构性约束而非学习。

## 细粒度 + 共享专家（DeepSeekMoE）

- **细粒度专家**：不用少数大专家，用很多小专家（V2 160、V3 256、V4 512）——router 粒度更细，专精度更高。
- **共享专家**：部分专家对所有 token 永久激活，捕获通用知识；其余路由专家专攻领域模式。降低路由不稳定性。DeepSeek-V3 = 1 共享 + 256 路由（每 token 选 8）。

## 生产挑战

- **显存**：所有专家权重都必须在显存中（或被换页），即便每 token 只激活少数。400B MoE 比 50B 密集模型更吃 VRAM（尽管推理 FLOPs 相近）。MoE 是**访存受限**而非算力受限。
- **专家并行**：专家分布到多 GPU，token 要跨设备路由——**all-to-all 通信**取代 TP 的 all-reduce，成为多节点推理瓶颈。高带宽互联（NVLink Switch、InfiniBand）可直接加速。
- **微调复杂度**：LoRA/QLoRA 要决定适配 router、专家还是两者。
- **量化**：每专家权重分布差异大，需分别处理。
- **冷专家**：少被路由的专家会退化，多数现代 MoE 保留小幅均衡惩罚让所有专家保持参与。
- **batch 形状**：MoE 偏好大批次（更多 token 让 router 激活更多专家、摊薄 all-to-all）；单用户推理效率低于密集模型。

## 生产部署（2026）

MoE 已成为前沿标配：Mixtral 8x22B（176B/44B/8 专家）、DeepSeek-V3（671B/37B/256）、Qwen 2.5-MoE、DBRX（132B/36B/16），以及据称的 GPT-4、Gemini Ultra。趋势是**更多更小专家 + 共享专家 + 无辅助损失均衡**。

## 参考资料

- Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer：https://arxiv.org/abs/1701.06538
- Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity：https://arxiv.org/abs/2101.03961
- Mixtral of Experts：https://arxiv.org/abs/2401.04088
