---
description: "Transformer block anatomy: residuals, LayerNorm/RMSNorm, FFN/SwiGLU, pre-norm vs post-norm and parameter count"
描述: "Transformer Block 结构：残差、归一化、FFN/SwiGLU、pre-norm 与参数量"
name: "Transformer Block Anatomy"
名称: "Transformer Block 结构"
---

# Transformer Block 结构

注意力是主角，其余（残差、归一化、前馈、交叉注意力）是让你能把它堆深的脚手架。一个 Transformer 就是同一个 Block 重复 N 次——学会 Block 就等于学会架构。

## 两个子层

Block 做两件事，分工清晰：

1. **多头注意力（MHA）**：在 token 之间搬运信息——Block 里唯一让位置互相看见的部分。
2. **前馈网络（FFN）**：逐 token 独立处理，各处共享权重。通常是两层线性 + 非线性，扩展到 4× 宽度再压回——**大部分参数与事实知识住在这里**（约 2/3 参数）。

一句话：注意力决定"看什么"，FFN 决定"怎么处理"。两者都不能替代对方。

## 残差连接：梯度高速路

每个子层包在残差里：不是 `x = Sublayer(x)`，而是 `x = x + Sublayer(x)`。子层只需学习对输入的**修正**，而 `+x` 给梯度一条跳过子层乘法的直达路径——正是这条 identity path 让梯度能在几十上百层里存活。没有残差，深层 Transformer 根本训不动。

## 归一化：控制尺度

归一化把激活重新缩放，防止逐层漂移。位置比初学者以为的更重要：

- **Post-norm（2017 原论文）**：`Norm(x + Sublayer(x))`——归一化落在残差主流上。能训，但深层不稳定，需要小心学习率 warmup。
- **Pre-norm（GPT-2 起，2026 标准）**：`x + Sublayer(Norm(x))`——归一化移到残差支路内，输入输出高速路保持干净。**深层稳定得多**，无需 warmup。Llama、Qwen、GPT-3+、Mistral 全用 pre-norm；80+ 层时 post-norm 即便精心初始化也会梯度爆炸，pre-norm 保持各层梯度范数稳定。微调 pre-norm 模型可用更高学习率（通常 2–5×）。

### RMSNorm（2026 主流归一化）

LayerNorm 减去均值、除以方差，再乘可学习 γ、加 β。RMSNorm 去掉均值中心化与偏置，只按均方根缩放：

```python
class RMSNorm(nn.Module):
    def forward(self, x):
        rms = x.pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
        return x * rms * self.weight
```

更简单、快约 10–20%、稳定性相当。Llama 等广泛采用。

### SwiGLU（FFN 激活）

2017 用 ReLU，2026 用 SwiGLU：`Swish(W1 x) ⊙ W3 x`，在 Llama、PaLM、Qwen 论文中一致优于 ReLU/GELU 约 0.5 ppl。SwiGLU 用三个矩阵，扩展比降到约 2.6× 以保持总参数相当。

## 完整的 pre-norm Block（代码）

```python
class Block(nn.Module):
    def __init__(self, dim, heads, mlp_ratio=4):
        self.norm1 = RMSNorm(dim)
        self.attn = MultiHeadAttention(dim, heads)
        self.norm2 = RMSNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, mlp_ratio * dim), nn.GELU(),
            nn.Linear(mlp_ratio * dim, dim),
        )
    def forward(self, x):
        x = x + self.attn(self.norm1(x))   # pre-norm 注意力子层
        x = x + self.mlp(self.norm2(x))    # pre-norm 前馈子层
        return x
```

四行公式：`h = x + MHA(LN(x))`；`y = h + FFN(LN(h))`。堆 N 个就是 GPT。

## 参数量

单个 Block：`4·d_model² + 8·d_model² = 12·d_model²`（注意力 4，FFN 8）。d_model=4096 时约 2 亿参数/Block；70B 模型约 80 个 Block + embeddings。估算 `N ≈ 12·L·d_model²`，对多数 decoder-only 模型误差几个百分点内，值得心算。

## 2017 → 2026 的 Block 演进

| 部件 | 2017 | 2026 |
|---|---|---|
| 归一化 | LayerNorm | RMSNorm |
| FFN 激活 | ReLU | SwiGLU |
| FFN 扩展 | 4× | 2.6×（SwiGLU 三矩阵） |
| 位置编码 | 正弦绝对 | RoPE |
| 注意力 | 全 MHA | GQA / MLA |
| 偏置项 | 有 | 无 |

骨架自 2017 未变，改进集中在这些替换。

> 相关：注意力的数学与变体见 `../internals/`；三种架构形态里 Block 如何组装见 `../families/`；MoE 把 FFN 换成专家池见 `../moe/`；推理时的归一化与量化见 `../../../model/inference/`。
