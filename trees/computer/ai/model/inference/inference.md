---
description: "KV cache, PagedAttention, batching, quantization and serving engines"
描述: "KV 缓存、PagedAttention、批处理、量化与服务引擎"
name: "Inference Optimization and Deployment"
名称: "推理加速与部署"
---

# M5 推理加速与部署

LLM 推理的三大挑战：内存限制（模型常超单卡）、延迟与吞吐的平衡（单用户延迟 vs 多用户吞吐）、注意力二次复杂度。优化技术分模型级、运行时/系统级、服务级三层，多数可叠加。

## 两阶段本质

- **Prefill（预填充）**：计算密集（compute-bound），处理输入 prompt、并行算所有 token。
- **Decode（解码）**：内存带宽密集（memory-bound），逐 token 生成、反复读权重与 KV Cache。

两者需不同优化、可用不同硬件。**Prefill/Decode 解耦**：分别用计算优化型和带宽优化型硬件，长输入场景典型 decode:prefill 实例比 2:1~4:1，KV 通过 NVLink 传输的开销相对收益可接受。

## 模型级优化

### 量化

降低数值精度（FP16 → INT8/FP8/INT4）：

| 精度 | 加速 | 质量影响 | 适用 |
|---|---|---|---|
| INT8 | 2–4× | 校准后几乎无损 | 全硬件部署 |
| FP8 | 接近 INT8 速度，精度更好 | 小 | Hopper/Blackwell 硬件加速 |
| INT4/AWQ/GGUF | 4–8× | 中等，可能需 QAT | 边缘、LLM 服务 |

- 量化是**最通用**的模型级优化；INT8 常近乎无损，INT4 需谨慎（校准、混合精度、部署前质量评估）。
- FP8 激活 + INT4 权重可减 8× 内存；多数 LLM 容量在注意力模式而非单个权重值。
- PTQ（训练后量化）vs QAT（量化感知训练）。

### 算子融合 / FlashAttention

- **算子融合**：合并顺序操作，消除冗余显存搬运，1.2–2×，数学等价。
- **FlashAttention**：硬件感知的 IO 优化 kernel，重排注意力计算、在 GPU SRAM 内做内层循环、不物化完整注意力矩阵，把 HBM 往返降到最少。O(N²)→O(N) 内存，2–4×（v1）、5–9× FP16（v2）、H100 上 FP8 再 1.5–2×（v3）。长上下文推理关键。

### KV Cache 与注意力变体

KV Cache 缓存已生成 token 的 Key/Value，避免重复计算；但随 batch 和序列长度线性增长，是大 batch 下的显存主导者。

- **PagedAttention（vLLM）**：受操作系统虚拟内存启发，把 KV Cache 存到非连续块，消除内部碎片，多个序列可共享物理块（共享 system prompt、并行 beam search）。配合 vLLM 吞吐最高提升约 24×（相对 HF Transformers）。
- **GQA（分组查询注意力）**：多组 query head 共享 K/V head，介于 MHA 与 MQA 之间，大幅减小 KV Cache 而无严重质量损失。
- **MQA**：所有 head 共享 K/V，KV Cache 最小但精度可能下降。Character.AI 通过激进注意力优化实现 >20× KV Cache 缩减。
- 注意力优化可组合：GQA、跨层共享 KV、局部/窗口注意力避免 O(n²) 增长。

## 运行时/系统级优化

### 批处理策略

| 策略 | 做法 | 权衡 |
|---|---|---|
| 静态批处理 | 等凑满 batch | 简单；填充浪费，短请求被长请求拖住 |
| 动态批处理 | 时间窗内凑批 | 较实用；仍按最长填充 |
| **连续批处理（in-flight）** | 每步调度，slot 空出即插新请求（Orca 论文） | 消除填充浪费，短响应立即返回；生产 SOTA |

连续批处理吞吐相对简单批处理可 >20×。

连续批处理本质是**请求级并发调度**——通用的并发模型、排队、限流与背压属于后端工程，这里聚焦 GPU slot 与 KV cache 层面的特化。

### 投机解码（Speculative Decoding）

小 draft 模型一次生成多个候选 token，大 verifier 模型一次前向并行验证；接受匹配前缀，否则回退。(token 级别并行打破自回归串行瓶颈)

- 典型 2–3× 延迟下降；代码生成（重复度高）可达 2.5×，创意写作仅 1.3×。
- 关键在 draft 与 target 对齐度（接受率）、draft 长度。
- EAGLE-3 等改进是 2026 生产热点。

### Prompt / Prefix 缓存

system prompt 跨请求相同 → 处理一次、复用 KV Cache。Anthropic：命中最高降 90% 成本、75% 延迟；Gemini：缓存 token 75% 折扣 + 少量存储费。前缀缓存对长 system prompt 可降 50–80% TTFT。

实现要点：把稳定前缀（system prompt、工具定义、规则）放前面缓存，**动态工具结果放尾部**——否则一个变化就使后面缓存全失效。

### 并行策略（服务侧）

- TP：切权重矩阵，节点内多卡，高带宽。
- PP：按层切，跨节点，decode 时有 bubble。
- DP：复制模型，多副本服务不同请求。
- SP：prefill 时长序列切分。

## 服务引擎

| 引擎 | 特点 |
|---|---|
| **vLLM** | PagedAttention + 连续批处理，默认的高吞吐多租户选择，相对 HF 最高 24× 吞吐 |
| **TensorRT-LLM** | NVIDIA,图优化、层融合、精度校准，针对 NVIDIA GPU |
| **SGLang** | RadixAttention/Radix 缓存、复杂控制流、Token Healing；与 vLLM 在执行上各有侧重 |
| **TGI** | HuggingFace, Rust/Python |
| **llama.cpp** | C/C++, ggml, 本地/边缘 |
| **Triton Inference Server** | 多框架综合服务 |

选择逻辑：匹配引擎到硬件与规模；>100 万次/月可考虑自建 OTel+ClickHouse 观测栈以控成本。

## 关键指标

- **TTFT**（Time to First Token）：首 token 延迟 → 受 prefill、前缀缓存影响。
- **TPOT / ITL**：每输出 token 时间 / token 间延迟 → 受 decode、量化影响。
- **吞吐**（tokens/s）、**Goodput**、**P95/P99 尾延迟**（均值会骗人）。
- 成本：按 token、按请求、按用户/功能归因；关注每小时消费速率（循环 Agent 一下午烧光预算）。

## 推荐优化顺序

1. 量化（最简单、影响最大）
2. vLLM + 连续批处理（换服务引擎）
3. FlashAttention（通常默认开启）
4. 前缀缓存（复用 system prompt）
5. 投机解码（大模型加速）
6. TP（超大模型）

多数技术可叠加：量化 + PagedAttention + 连续批处理 + 前缀缓存一起用效果最大。

## 生产化要点

- 渐进发布、A/B 测试、fallback 机制（保留未优化版本）、负载均衡、自动扩缩。
- 监控延迟分位数、吞吐、显存、GPU 利用率，发现回归。
- 渐进式优化逐步验证，困惑度/质量不达标就回退。
- Spot 实例可省 60–80% GPU 成本（容错负载）。
- 自托管模型还要监控 GPU 利用率、队列深度、TTFT、显存。
