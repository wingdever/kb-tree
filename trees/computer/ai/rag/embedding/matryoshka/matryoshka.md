---
description: "Matryoshka representation learning and dimension reduction"
描述: "Matryoshka 表示学习与向量降维"
name: "Matryoshka and Dimension Reduction"
名称: "Matryoshka 与降维"
---

# Matryoshka 与降维

## Matryoshka Representation Learning（MRL）

Kusupati et al. 2022 提出。把对比训练扩展为**同时优化多个嵌套子向量维度** M = {64, 128, 256, 512, 1024, 2048}：

```
L_MRL = Σ_{m∈M} λ_m · L(f_{1:m}(x), y)
```

`f_{1:m}` 表示截断到前 m 维。结果是：前 64 维捕获最显著的语义区分，后续维度逐步精化。

**2026 年 MRL 已是所有主流嵌入 API 的标配**：OpenAI text-embedding-3、Google Gemini Embedding、Voyage 4、Cohere Embed v4。它让部署时可在存储/精度间自适应权衡，无需重训模型。

## 降维操作

嵌入时指定维度：

```python
client.embeddings.create(model="text-embedding-3-large", input=[d], dimensions=1024)
```

或截断已存的全维向量并重新归一化：

```python
v = np.asarray(vec[:1024], dtype="float32")
v = (v / np.linalg.norm(v)).tolist()
```

## 存储账

float32 每维 4 字节：

- 3072 维 = 12 KB/向量
- 1024 维 = 4 KB/向量

1000 万文档下：~120 GB vs ~40 GB 的差别。

**操作顺序**：先砍维度 → 测黄金集召回 → 保住才保留。别为了改维度从头重嵌语料（Matryoshka 模型可直接截断）。

## 与其他压缩手段的配合

- **量化**（PQ/OPQ/标量量化）：把向量缩小 4–32×。
- **int8/binary 输出**：Cohere Embed v4、Voyage 支持原生低精度输出。
- **分层存储**：热/温/冷分区。

> 降维直接关系向量库成本。

## 参考资料

- Matryoshka Representation Learning：https://arxiv.org/abs/2205.13147
- MTEB: Massive Text Embedding Benchmark：https://arxiv.org/abs/2210.07316
