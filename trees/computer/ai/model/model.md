---
description: "Knowledge tree for the model engineering lifecycle"
描述: "模型工程全链路知识树导航"
name: "Model Engineering"
名称: "模型工程"
---

# 模型工程知识树

本目录覆盖模型本身的全链路：从分词、预训练、并行训练、微调对齐、distill压缩，到推理部署与eval，以及multimodal与rl。每个知识点自成一个目录。

## 知识点目录

| 目录 | 内容 |
|---|---|
| `tokenizer/` | BPE/WordPiece/Unigram/SentencePiece 原理、对比、从零实现、词表设计 |
| `pretrain/` | 数据管道与语料混合、课程、Scaling Law 与 Chinchilla、预训练评估 |
| `distributed/` | DP/TP/PP/SP/EP 五维并行、ZeRO/FSDP、3D/4D/5D、DualPipe、训练稳定性 |
| `peft/` | SFT 流程、LoRA/QLoRA/DoRA/rsLoRA 族、超参、adapter 服务 |
| `distill/` | logit/response/feature/on-policy distill、DeepSeek-R1-Distill、叠加效应 |
| `inference/` | KV Cache/PagedAttention/连续批处理/FlashAttention/投机解码/量化/服务引擎 |
| `eval/` | 能力维度矩阵、主流基准、四种failure、eval方法论 |
| `rl/` | MDP、值方法、策略梯度、Actor-Critic、PPO/GAE、RLHF 衔接 |
| `multimodal/` | 视觉编码器、桥接方式（投影/交叉注意力/早融合）、训练阶段、eval |

## 建议顺序

造模型全链路：tokenizer → pretrain → distributed → peft → distill → inference。选型与eval：eval → inference。理论基础：rl → peft 的偏好对齐部分。multimodal独立成篇。

## 与其他领域的关系

- Agent 训练（RLVR/GRPO 等更偏应用的rl）见 `../agent/rl/`。
- 模型能力eval与 Agent 行为评估是两个层次：这里评模型，Agent 评估见 `../agent/eval/`。
- 调用模型的 API 字段规范见 `../api/`。
