---
description: "Transformer internals: self-attention, positional encoding, prefill/decode, KV cache and attention variants"
描述: "Transformer 内部机制：自注意力、位置编码、Prefill/Decode、KV Cache 与注意力变体"
name: "Transformer Internals"
名称: "Transformer 内部机制"
---

# Transformer 内部机制

Transformer 是现代 NLP 与大模型的基石架构。本页讲清注意力的数学、Prefill/Decode 两阶段、KV Cache 与复杂度。

## 核心要素

模型的关键配置：层数、注意力头数、损失函数、超参数。

## Transformer Input：词嵌入 + 位置编码

Token 表示 = `embedding_word + embedding_position`。

- 词嵌入来源：Word2Vec、GloVe、Transformer 预训练。
- 位置编码（正弦，原论文）：

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^((2i+1)/d_model))
```

pos 是 token 在句中的位序，d_model 是嵌入维度。

**RoPE（旋转位置嵌入，现代标准）**：不像绝对编码那样加静态向量，而是在复数平面按位置角旋转 Q、K。两个旋转向量的点积只依赖相对距离 (m−n)，天然捕捉相对位置（"not good" vs "good not"），支持 NTK/YaRN 外推扩展上下文。RoPE 在 Q/K 线性投影**之后**施加——若在投影前旋转，线性变换会扭曲精确几何角度。被 Llama、PaLM、Qwen 采用。

## Self-Attention 自注意力

每个 token 有 Q（Query，想了解上下文）、K（Key，什么样的内容相关）、V（Value，想取的信息）：

```
Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V
```

d_k 是 Q/K 向量的维度（列数）。

### 矩阵视角（六步）

设输入 X (n×d，n token、d 维)，d 维是语义表示空间的自由度。

1. **投影**：`Q = X·W_Q`（W_Q: d→q 维），`K = X·W_K`，`V = X·W_V`。逐 token：`q_i = x_i · W_Q`。
2. **相似度分数**：`S = Q·Kᵀ`，`S_ij = q_i · k_j = Σ_d Q_i,d · K_j,d`。S 是未归一化注意力 logits 矩阵——第 i 个 query 对所有 key 的分数。
3. **缩放与掩码**：`A = softmax(S / √d_k)`，按行 softmax，每个 query 对所有 key 权重和为 1。缩放防 softmax 饱和。
4. **加权聚合**：`o_i = Σ_j A_ij · v_j`，即 `Attention = A·V`，输出形状 n×d_v。
5. **多头**：`head_h = Attention(Q·W_Q^h, K·W_K^h, V·W_V^h)`，每头有自己的投影与注意力权重 A^h，可关注不同关系/子空间/模式；拼接 `o = Concat(head_1,...,head_H)·W_O`。
6. 单头注意力中每个维度共享同一组权重——决定"从哪些 token 聚合"，但对所有 value 维度用相同权重；多头打破这一限制。

复杂度：标准自注意力 O(n²)，随序列长度平方增长。

## Prefill 与 Decode（推理两阶段）

Transformer 自回归生成分两阶段，计算特征截然不同：

| | Prefill（预填充） | Decode（解码） |
|---|---|---|
| 每次前向输入 | 整段 prompt（P token） | 1 token |
| Cache 动作 | 填充全部 P 位置 | 追加 1 位置 |
| 矩阵形态 | 矩阵×矩阵（高 Q） | 矩阵×向量（单行 Q） |
| 瓶颈 | **计算密集**（GEMM，受 FLOPs 限） | **访存密集**（GEMV，受内存带宽限） |
| 并行 | 全部 prompt 位置并行 | 天然串行 |
| 决定延迟 | TTFT（首 token 时间） | TPOT（每 token 时间，倒数即吞吐） |

因果掩码让 Prefill 的并行计算在数学上等价于逐 token 串行（每个位置只能看自己和之前的 token）。

### Prefill 的 KV Cache

某层输入 X ∈ R^(n×d)，投影 W_Q/W_K/W_V：Q=XW_Q、K=XW_K、V=XW_V。因果注意力 `softmax(QKᵀ/√d_k + M)V`，M 是因果掩码（j≤i 为 0，否则 −∞）。

Prefill 结束每层保留 `C_K^(l)=K^(l)`、`C_V^(l)=V^(l)` 即该层 KV Cache。要点：只缓存 K/V 不缓存 Q；每层、每头分别缓存；用最后位置输出取 logits 采样第一个 token y₁。

### Decode 单步数学

已生成 t−1 个 token，Cache 有 C_K ∈ R^((n+t−1)×d_k)、C_V 同理。输入上一 token 表示 `x_t = Embed(y_{t−1}) + PE(t)`（单行）：

```
q_t = x_t·W_Q,  k_t = x_t·W_K,  v_t = x_t·W_V      （1×d_k / 1×d_v）
C_K ← [C_K; k_t],  C_V ← [C_V; v_t]                （追加，不重算历史）
s_t = q_t·C_Kᵀ / √d_k  ∈ R^(1×(n+t))               （单 query 对所有历史 key）
a_t = softmax(s_t)
o_t = a_t·C_V        ∈ R^(1×d_v)                   （加权聚合所有缓存 value）
y_t ~ softmax(LMHead(o_t'))
```

关键点：Decode 每步只算当前 token 的 q/k/v；历史 K/V 从 Cache 读，不重算；当前 k/v 追加进 cache；单 query 看全部历史 key，**不需要因果掩码**（本来就只能看到历史）；位置编码用 pos = n+t。Q 不缓存。

### 复杂度

- Prefill：O(n²·d_k)（n 个 query 对 n 个 key）。
- Decode 单步：O((n+t)·d_k)（1 个 query 对 n+t 个历史 key）。生成 T 个 token 总注意力成本 O(T(n+T)d_k)。
- KV Cache 显存：O(L·(n+T)·d_k·2)，L 层数，系数 2 是 K/V，多头、batch 再乘相应维度。

长上下文下 KV Cache 可超过权重本身，成为主要显存约束——这催生 GQA/MQA、PagedAttention、KV 量化。

## 注意力变体（2026）

- **MHA**：Q/K/V 头数相同，KV Cache 最大。
- **MQA**：所有 Q 头共享单个 K/V 头，Cache 缩小 H 倍，有质量损失。
- **GQA**（分组查询）：Q 头分组共享 K/V 头，Cache 按分组因子缩小，质量接近 MHA——**现代大模型标准**（Llama 2 70B、Llama 3）。Llama 3-8B 有 32 个 Q 头、8 个 KV 头，Cache 压到 1/4。
- **FlashAttention**：IO 感知精确注意力，分块（tiling）+ 在线 softmax + 重计算，不把 N×N 矩阵写回 HBM，内存 O(n²)→O(n)，2–4× 加速。因果注意力可跳过未来 key 块，计算再降近半。**输出与标准注意力数学等价**，各代改进只影响速度/内存。
- **滑动窗口注意力**：每 token 只看最近 W 个 token，成本 O(N×W)，KV Cache 以 W 为上限（Mistral 采用）。深层窗口重叠让远处信息间接传播。
- **全局+局部混合**：多数 token 看局部窗口，少数全局 token 看全部，保证远处信息通路。
- **位置编码外推**：RoPE 的 NTK/YaRN 修正，扩展超训练长度的上下文。

