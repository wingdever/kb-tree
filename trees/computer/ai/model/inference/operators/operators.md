---
description: "Hardware-level operators in large models: model graph ops, fused kernels, hardware mapping, memory hierarchy and performance"
描述: "大模型硬件算子：模型图算子、融合 kernel、硬件映射、存储层级与性能模型"
name: "Hardware Operators for Large Models"
名称: "大模型硬件算子"
---

# 大模型硬件算子

大模型在框架里表现为一张计算图：MatMul、Attention、Softmax、LayerNorm、激活、Embedding、RoPE、KV Cache 读写……这些节点最终都要翻译成硬件能执行的 **kernel（内核）**。所谓“硬件层面的算子”，就是**数学定义 → 融合策略 → 线程/瓦片/指令映射 → 实际吞吐**这一整条链路。

## 三个层次别混

| 层次 | 例子 | 谁负责 |
|---|---|---|
| 模型图算子 | MatMul、Attention、Softmax、RMSNorm、SwiGLU、Embedding | 框架/模型定义 |
| 融合算子 | FlashAttention、Fused MLP、RMSNorm+Residual、SwiGLU 融合 | 编译器/算子库/手写 kernel |
| 硬件 kernel / 指令 | CUDA kernel、Tensor Core MMA、SIMD、脉动阵列指令 | GPU/NPU/CPU 与底层库 |

同一个“Attention”在模型图里是一个节点，在 GPU 上可能是多个 kernel，也可能被 FlashAttention 融合成一个；在 NPU 上则可能被编译器切成一组矩阵乘与向量操作。**说“算子慢”要先说清是哪一层慢**。

## 大模型里的核心算子

- **GEMM / GEMV**：线性层、投影、MLP 的主体；训练与 prefill 多为 GEMM，decode 的 GEMV 更受内存带宽限制。
- **Grouped GEMM / MoE 算子**：专家路由后按组做矩阵乘；难点是负载不均、分组粒度与通信。
- **Attention**：QK^T、Softmax、PV 三步；朴素实现要物化注意力矩阵，FlashAttention 通过分块与在线 Softmax 避免往返 HBM。
- **归一化与激活**：LayerNorm、RMSNorm、GELU、SwiGLU；通常与前后算子融合，减少中间张量。
- **位置编码**：RoPE 的旋转与查表；常与 Q/K 投影融合。
- **KV Cache 读写**：PagedAttention 的块分配、gather/scatter；decode 阶段的主要内存流量之一。
- **采样**：Top-K、Top-P、温度、重复惩罚；小算子但延迟敏感，常被融合或放到 CPU/专用 kernel。
- **通信算子**：All-Reduce、All-Gather、Reduce-Scatter、All-to-All；多卡训练与 MoE 推理的关键路径。

## 硬件怎么执行

### GPU

- **SIMT + Tensor Core**：warp 内线程并行，矩阵乘交给 Tensor Core 的 MMA 指令；FP16/BF16/FP8/INT8 对应不同指令与吞吐。
- **存储层级**：HBM → L2 → Shared Memory → Register。算子性能通常由“能不能把数据复用在上层存储”决定，而不是由算力峰值决定。
- **切分（tiling）**：把大矩阵切成能放进 Shared Memory 的 tile，循环内复用；tile 太大寄存器溢出，太小则反复读 HBM。
- **合并访问（coalescing）**：相邻线程读相邻地址；布局转置、stride 不连续会让有效带宽骤降。
- **异步与流水**：TMA、cp.async、warp specialization 把“搬数据”和“算”重叠，隐藏内存延迟。
- **Occupancy**：寄存器、Shared Memory、线程块大小共同决定能同时驻留多少 warp；占用率低就藏不住延迟。

### NPU / TPU

- **脉动阵列/矩阵引擎**：数据在阵列中流动，适合规则的大矩阵乘；对 shape、对齐、算子融合更敏感。
- **片上 SRAM**：容量有限，编译器要做完整的数据流调度；不支持的算子会回退到 CPU 或拆成多个小算子。
- **编译器主导**：算子不是手写 kernel，而是由图编译器切分、融合、排布；性能更依赖编译器是否理解 shape 与布局。

### CPU

- **SIMD/向量指令**：AVX、NEON、AMX；矩阵乘靠分块、缓存友好布局与多线程。
- **小模型/边缘推理**：量化 + 算子融合（如 ggml/llama.cpp）比裸 FLOPs 更重要。

## 性能模型

- **Roofline**：性能上限由“算力峰值”和“带宽上限”共同决定；算术强度（FLOPs/Byte）落在哪个区域，决定是 compute-bound 还是 memory-bound。
- **Prefill vs Decode**：prefill 是大矩阵乘，通常 compute-bound；decode 逐 token 读权重与 KV Cache，通常 memory-bound。同一个模型、同一个算子，两个阶段的瓶颈不同。
- **融合的收益**：把多个逐元素算子合并，主要省的是 HBM 往返与 kernel launch 开销；如果融合后寄存器压力过大、占用率下降，反而可能变慢。
- **量化的收益**：INT8/FP8 降低带宽与指令成本，但是否加速取决于硬件是否有对应指令、是否 memory-bound、以及反量化开销。
- **实际吞吐 ≠ 峰值算力**：峰值是营销数字；有效吞吐要看 shape、batch、序列长度、布局、并行度与通信。

## 算子库与编译器

- **cuBLAS / cuDNN / CUTLASS**：NVIDIA 的矩阵乘与深度学习算子库；CUTLASS 提供可组合的 tile/warp 级模板。
- **Triton**：用类 Python DSL 写 GPU kernel，自动处理部分切分与调度；适合自定义融合算子。
- **TVM / XLA / torch.compile / Inductor**：图级优化、算子融合、布局转换、代码生成。
- **TensorRT / TensorRT-LLM**：推理图优化、层融合、精度校准、kernel 选择。
- **FlashAttention / FlashInfer / DeepGEMM**：面向注意力和 GEMM 的高性能专用 kernel。
- **vLLM / SGLang**：服务引擎里自带 PagedAttention、连续批处理等定制算子。

选择顺序通常是：先用成熟库/编译器 → 再看 profile 定位热点 → 最后才手写或生成专用 kernel。上来就手写 CUDA，往往优化了不是瓶颈的算子。

## 算子融合与图优化

常见融合：

- **MatMul + Bias + Activation**：一个 kernel 完成线性层与激活，省中间张量。
- **RMSNorm + Residual + Quant**：归一化、残差、量化融合，减少读写。
- **Attention 全链路**：QK^T、Softmax、PV 融合，避免物化注意力矩阵。
- **SwiGLU**：门控与乘法融合，减少一次中间写回。
- **KV Cache 更新 + 采样**：decode 尾部小算子融合，降低 launch 开销。

融合不是越多越好：寄存器压力、Shared Memory 容量、数值精度、可调试性、不同 shape 的泛化都要权衡。**融合的边界是硬件存储层级，不是算子数量**。

## 怎么定位算子瓶颈

1. 用 Nsight Systems / Nsight Compute、ROCm profiler、NPU 厂商工具抓时间线。
2. 看每个 kernel 的耗时、 achieved TFLOPS、achieved bandwidth、occupancy、cache 命中。
3. 判断是 compute-bound 还是 memory-bound；不要只看总 FLOPs。
4. 检查 layout 转换、不必要的 contiguous/copy、kernel launch 次数。
5. 对比融合前后、量化前后、不同 batch/序列长度下的曲线，而不是单点。

## 常见误解

- **“FLOPs 高就一定快”**：decode 阶段常常是带宽瓶颈，算力空转。
- **“算子数量越少越好”**：融合可能带来寄存器溢出、占用率下降；要看实际 profile。
- **“INT8 一定比 FP16 快”**：没有对应指令、反量化开销大、或仍受带宽限制时，收益有限。
- **“算子融合一定数值无损”**：浮点累加顺序、近似激活、量化舍入都会改变结果，需要评估。
- **“硬件峰值算力就是实际吞吐”**：shape 不匹配、并行度不足、通信等待都会让有效吞吐远低于峰值。
- **“手写 kernel 一定比库快”**：成熟库针对常见 shape 做了大量调优；手写通常只在特定场景赢。

## 一句话主线

算子是大模型计算图落到硬件的翻译层：**先分清模型图算子、融合算子与硬件 kernel，再看数据复用、切分、布局、精度与并行度**；性能优化的核心不是“多写算子”，而是让正确的数据在正确的存储层级被复用。

## 参考资料

- NVIDIA CUDA C++ Programming Guide：https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- CUTLASS: CUDA Templates for Linear Algebra Subroutines：https://github.com/NVIDIA/cutlass
- Triton: Open-source GPU programming：https://triton-lang.org/
- FlashAttention：https://arxiv.org/abs/2205.14135
- Roofline: An Insightful Visual Performance Model：https://dl.acm.org/doi/10.1145/1498765.1498785
- PyTorch torch.compile 文档：https://docs.pytorch.org/docs/stable/torch.compiler.html
- DeepGEMM：https://github.com/deepseek-ai/DeepGEMM
- FlashInfer：https://github.com/flashinfer-ai/flashinfer
