---
description: "Vision encoders, projection vs cross-attention bridges and VLM training"
描述: "视觉编码器、投影与交叉注意力桥接及 VLM 训练"
name: "Multimodal Models"
名称: "多模态模型"
---

# M8 多模态模型（视觉-语言）

多模态模型跨文本、图像、音频、视频处理与生成。核心工程问题不是"能不能做"，而是**视觉特征以什么方式、在什么层级进入语言模型**——这决定能力、效率与能做的视觉推理类型。

## 三种融合架构

| 架构 | 做法 | 优点 | 缺点 | 代表 |
|---|---|---|---|---|
| **Late Fusion（后融合）** | 各模态独立编码成向量，末端 concat/pooling | 模块化、可独立换编码器 | 模态交互弱、细粒度接地难 | CLIP 式嵌入模型 |
| **Early Fusion（早融合）** | 图像 patch token 与文本 token 拼成一个序列，送单一 transformer | 第 1 层起强交叉注意力、随数据扩展好 | 图像 token 吃上下文预算（1024×1024 图 ≈ 256–1024 token） | GPT-4o（推测）、Chameleon、Fuyu |
| **Cross-Attention / Projector（桥接）** | 视觉编码器出特征，小 projector 映射到 LLM embedding 空间，作为"伪 token"喂入 | 复用预训练 LLM（训练便宜）、实现简单 | projector 容量成瓶颈、细节受 token 预算限 | LLaVA、Qwen-VL、Llama 3.2-Vision |

第四种：**Attention-gated（Flamingo 式）**——把交叉注意力层插入 LLM 特定深度，冻结主干、只训 adapter。优点是不增长 token 预算的多点交互；缺点是自定义架构、复用标准栈难。代表：Flamingo、IDEFICS、Kosmos。

**2026 共识**：开源 VLM 以 projector + adapter（LLaVA 式）胜在易用；前沿闭源模型推测为早融合；研究方向四种都活跃。

## 视觉编码器

主流是 **ViT**（Vision Transformer）——把图切成固定 patch，每 patch 投影为 embedding，再用 transformer attention 处理序列。预训练方式：

- **对比学习**（CLIP、SigLIP）：图文配对拉近、不匹配推远，与语言特征语义对齐好，**桥接到 LLM embedding 空间更容易**。
- **掩码图像建模**（MAE）。

CLIP 的历史地位：证明图文语义可对齐到同一向量空间。今天几乎所有开源 VLM **直接借用 CLIP/ViT 预训练权重**而非从零训。分辨率-能力权衡：高分辨率需更多 patch、更长序列、更多算力，但 OCR、图表、文档理解必须。

## 桥接方式细节

以 LLaVA 为例（224×224 图）：ViT 切成 14×14=196 个 patch → 每个 patch 一个 token → MLP projector 映射到文本 embedding 维度 → 拼在文本指令前喂 LLM。

常见桥接：

- **MLP Projector**：一两层全连接，简单高效，LLaVA 用。
- **Q-Former（BLIP-2）**：一组可学习 Query 通过交叉注意力从视觉特征"查询"紧凑信息，把几百视觉 token 压到几十，计算开销小。
- **Resampler**：类似 Q-Former，可学习 Query 池化，兼顾压缩与细节。

Higher-res 方案：InternVL 用**动态分块（dynamic tiling）**——把图切成若干 448×448 tile（最多几十块，支持到 4K），各自编码后经 PixelShuffle 降采样再拼文本，实现细粒度 OCR 与文档理解。Qwen-VL 用交叉注意力 adapter 把密集视觉 token 压成定长序列，配精细 2D 位置编码保空间布局，支持 grounding 与多语言文字读取。DeepSeek-VL2 结合动态分块 + MoE 效率。

## 训练阶段

1. **阶段一：特征对齐预训练**。只训桥接层（projector / 交叉注意力），冻结视觉编码器与 LLM，在大规模图文描述数据上建立基础视觉接地，不破坏已有能力。
2. **阶段二：端到端指令微调**。训全模型或 LoRA adapter，用高质量"图像+问题/描述/推理"指令数据。阶段二数据的质量与多样性决定视觉指令跟随的上限。

视觉指令数据比文本更难规模化：当前靠 GPT-4V 等自动标注流水线，但引入教师模型的质量天花板。LLaVA 用纯语言 GPT-4 基于 COCO 生成 158K 条图文指令（58K 对话、23K 详细描述、77K 复杂推理）。LLaVA-1.5 仅用公开数据、单 8×A100 节点约 1 天训完，在 11 个基准达 SOTA。

## 音频与视频扩展

- **音频**：同样的桥接模式——预训练音频编码器（语音用 Whisper、通用音频用 EnCodec）产出序列表示，projector 映射到 LLM embedding。挑战是模态特有的 tokenization 效率：16kHz 原始音频每秒帧数远超 LLM 上下文能承受，需大幅压缩。
- **视频**：在高清空间维上加时间维，token 预算成核心工程约束。做法：稀疏帧采样、编码器内时间压缩、基于查询的视频摘要（多帧压成固定数量可学习 query token）。

## 评测 VLM：采用前必测七项

1. OCR 准确率（MMBench-OCR）
2. 图表理解（ChartQA）
3. 文档推理（DocVQA）
4. 接地/指称（RefCOCO）
5. 细粒度计数（多数模型的弱点）
6. 空间推理（GQA）
7. 你自己的领域图片

> 大基准可被 gaming。**一定用你自己的图片测**。MMMU/MMMU-Pro 顶部 ~86–87%，尚未饱和。

## 构建建议

- 开源组件快速起步：**projector 式 VLM 是务实默认**，Qwen-VL、Llama 3.2-Vision 是强默认选择。
- 服务：projector 式图片增加固定 ~300–1000 token，易与 vLLM 集成；早融合图片可能主导上下文，吞吐强依赖图片 batch 大小；交叉注意力式推理路径定制、运行时支持较薄。
- 统一多模态是方向——2026 仍早期，研究侧四种架构都活。
