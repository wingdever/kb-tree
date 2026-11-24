---
description: "Five parallelism dimensions, ZeRO/FSDP, 3D/5D and stability"
描述: "五维并行、ZeRO/FSDP、3D/5D 并行与训练稳定性"
name: "Distributed Training"
名称: "分布式训练"
---

# M2 分布式训练

单卡放不下大模型：一张 80GB HBM 理论只放约 40B 个 FP16 参数，70B 光权重就约 140GB。训练还要存梯度、优化器状态和激活——以 Adam 混合精度训 70B 为例，参数 2N + 梯度 2N + 优化器 12N = 16×70B ≈ 1120GB，单卡连一角都放不下。分布式训练就是把模型切到几千张卡上、让它们像一台机器一样工作。

## 显存四项开销（N = 参数量）

| 组成 | 大小 | 说明 |
|---|---|---|
| 参数（FP16） | 2N | 前向、反向都要用 |
| 梯度（FP16） | 2N | 反向累积 |
| 优化器状态 | 12N | Adam FP32 的 m、v、master 权重 |
| 激活 | 与 batch、seq、depth 成正比 | recompute 时需 |

## 五种并行维度

| 策略 | 切什么 | 通信模式 | 典型边界 | 特点 |
|---|---|---|---|---|
| **DP（数据并行）** | 切数据，模型复制 | 梯度 AllReduce | 节点内/跨节点 | 简单，但不省模型状态显存 |
| **FSDP / ZeRO-3** | 切参数、梯度、优化器 | 参数 AllGather + 梯度 ReduceScatter | 节点内/跨节点 | 省显存，通信增加 |
| **TP（张量并行）** | 切单层内的算子/矩阵 | 每层多次 AllReduce | 单节点 NVLink 域内 | 通信频繁，强依赖高速互联 |
| **PP（流水线并行）** | 按层切 | stage 间 P2P 传激活 | 跨节点友好 | 有 pipeline bubble |
| **EP（专家并行）** | 切 MoE 专家 | all-to-all dispatch/combine | 节点内/跨节点 | MoE 专用 |
| **SP/CP（序列/上下文并行）** | 切序列维度 | ReduceScatter/AllGather、Ring | 长上下文 | 解决激活爆炸 |

### 四种集合通信原语

- `AllReduce(x_i)` → 每个 rank 拿 Σx_i；流量 ≈ 2(N-1)/N·|x|
- `ReduceScatter(x_i)` → 每个 rank 拿 Σx_i 的 1/P 片；流量 ≈ (N-1)/N·|x|
- `AllGather(s_i)` → 每个 rank 拿全部拼接；流量 ≈ (N-1)/N·|s|·P
- `All-to-All(x_i[j])` → rank i 的第 j 片发给 rank j

恒等式：**AllReduce = ReduceScatter + AllGather**。真正省流量的是只需分片结果的场景（如 ZeRO-2 梯度的 ReduceScatter）。

## 数据并行与 ZeRO / FSDP

**DDP（DistributedDataParallel）**：每卡完整模型副本，反向后梯度 AllReduce。梯度分桶（bucket）让异步 AllReduce 与反向计算重叠。注意：DDP 是吞吐手段，**不解决模型超出显存的问题**。

**ZeRO（Zero Redundancy Optimizer，Microsoft DeepSpeed）** 把 DP 中冗余的三份状态切分：

| 阶段 | 切分内容 | 显存缩减 | 额外通信 |
|---|---|---|---|
| ZeRO-1 | 优化器状态 | 最高 4× | 与标准 DP 同 |
| ZeRO-2 | + 梯度 | 最高 8× | 梯度用 ReduceScatter 替 AllReduce |
| ZeRO-3 | + 参数 | 随 GPU 数线性 | 前向/反向前 AllGather 参数（约 1.5×） |

**FSDP（Fully Sharded Data Parallel，PyTorch 原生）** ≈ ZeRO-3：

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy
model = FSDP(model, sharding_strategy=ShardingStrategy.FULL_SHARD)
```

- 以 Transformer Block 为粒度 wrap，进 block 时 AllGather、退出时释放。
- 下一个 block 的 AllGather 与当前 block 计算重叠（prefetch）。
- **FSDP2（PyTorch 2.4+）**：基于 DTensor，取消 FlatParameter，与 TP/PP 组合更干净。
- **HSDP**：节点内 FullShard + 节点间 Replicate，减少跨节点 AllGather。

**Offload**：ZeRO-Offload 把优化器状态放 CPU；ZeRO-Infinity 参数也能下放 NVMe。工业预训练一般不用（吞吐骤降），SFT/LoRA 常用。

## 张量并行（TP）

Megatron-LM 定型，把单个大矩阵乘法切到多卡：

- **列切**：Y = XA，A 按列切 [A1, A2]，每卡算 Yi = X·Ai。
- **行切**：A 按行切、X 按列切，每卡算 Yi = Xi·Ai，最后 AllReduce。

MLP（Linear→GELU→Linear）用"列切 + 行切"配对；Attention 的 QKV Linear 列切（切 head），Output Linear 行切。每层约 2 次 AllReduce（forward）+ 2 次（backward）。通信频繁强依赖 NVLink，**一般 TP ≤ 8、只在节点内**。更高 TP 会缩小矩阵乘法、降低利用率。

## 流水线并行（PP）

按层切，stage 间只传激活与激活梯度（P2P），跨节点友好。经典问题是**气泡（bubble）**——头尾 stage 的 GPU 空闲。微批（micro-batch，GPipe）把 mini-batch 拆小以流水化，仍浪费约 20–30% GPU 时间。

## 序列/上下文并行（SP/CP）

seq_len 到 32K/128K/1M 时，激活 B×S×H 本身爆显存，TP 切不动。沿序列维度切：

- **Megatron-SP**：把 LayerNorm/Dropout 等"行无关"算子的激活按 seq 切，TP 通信由 AllReduce 换成 ReduceScatter + AllGather。
- **Ring Attention**：KV 在环形拓扑上传递，每卡算局部 attention，几乎线性扩展到任意长序列。
- **Ulysses**：在 attention 内部 all-to-all，把 (B, S/P, H) 换为 (B, S, H/P)。head 数须能被并行度整除。
- **Context Parallel（CP）**：Megatron 术语，通常指 Ring Attention 风格。

实操：Ulysses 与已切 head 的 TP 不好叠加；Ring/CP 与 TP 正交性更好。

## 专家并行（EP，MoE 专用）

每层几十到几百 expert，token 只路由到 top-k。EP 把 expert 分散到 N 张卡：token routing → all-to-all dispatch → local experts → all-to-all combine。通信量 = 激活 × 2 × top-k × (1−1/EP)。痛点是路由抖动（负载不均）、all-to-all 拖尾、drop-token vs capacity factor。

## 3D / 4D / 5D 并行

- **3D**：DP + TP + PP。Megatron-LM v2 在 3072 张 A100 上达 502 PFLOPS、52% 峰值吞吐。典型 175B/1024 GPU 配置：TP=8、PP=16、DP=8。
- **4D**：Llama 3 405B 在 16384 张 H100 上加 **CP**（TP=8、PP=16、CP=16、剩余 FSDP），8K 序列约 400 TFLOPs/GPU。
- **5D**：MoE 再加 **EP**。DeepSeek-V3（671B、256 experts）用 16-way PP + DualPipe、64-way EP（跨 8 节点）、ZeRO-1 DP，**无 TP**。DualPipe 把前向、反向、all-to-all 通信重叠，"both all-to-all and PP communication can be fully hidden"，在约 1:1 的计算通信比下仍达高硬件利用率。

## 训练稳定性：万卡集群的日常

Llama 3 报告：16384 张 H100 训练时平均每 3 小时有一张卡硬故障，停机占总时间 9%+。工业级必须：

- 高频 Checkpoint（每 30 min 全量，节省约 70% 损失）
- 5–10% 热备卡、故障检测（温度/功耗/ECC）、自动恢复（切卡→加载 ckpt→续训）
- Loss spike 处理：自动 rollback 到稳定点、调小 LR 重试

> 能不能把万卡稳定跑下来，本身就是核心竞争力。

## MFU 与前沿集群

显存之外还有内存带宽墙和集合通信墙。并行化目标不是"能装下"，而是在通信代价与 MFU（模型算力利用率）间平衡。工业预训练目标：密集模型 40%+、MoE 30%+、稳到 50% 算优秀。前沿规模：Google PaLM 用 6144 TPUv4；xAI Colossus 达 10 万 H100。DeepSeek-V3 用 2048 H100、FP8、DualPipe 把成本压到约 557 万美元，说明工程可部分抵消硬件劣势。
