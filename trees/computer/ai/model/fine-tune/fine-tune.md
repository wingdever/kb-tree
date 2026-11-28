---
description: "Fine-tuning umbrella: full tuning vs PEFT, SFT vs preference alignment, data, evaluation, serving and governance"
描述: "微调总览：全参与 PEFT、SFT 与偏好对齐、数据、评估、部署与治理"
name: "Fine-Tuning"
名称: "微调"
---

# 微调

微调是用领域或任务数据继续训练基座模型的总称。它有两个轴：改多少参数，以及用什么训练目标。

## 两个轴

- **参数范围**：全参数微调更新全部权重；PEFT 只训练少量新增或选择的参数。PEFT 是微调的一种，不是微调的同义词。
- **训练目标**：SFT 教“怎么答”；偏好对齐教“哪种答法更好”。两者可以叠加，也可以只做其中一种。

## 判断顺序

1. 先判断需不需要微调：能用提示词、RAG 或工具解决，就先不要微调。
2. 需要改行为与格式，先做 SFT；需要改取舍与语气，再考虑偏好对齐。
3. 数据与算力有限，优先 PEFT；PEFT 容量不够，再评估全参数微调。
4. 训练前就想清楚怎么评估、怎么部署、怎么回滚；否则不要开训。

## 常见误解

- **PEFT 不是微调的全部**：LoRA、QLoRA 只是参数高效方法，不能覆盖全参数微调、数据工程与偏好对齐。
- **微调不等于注入知识**：事实型知识优先 RAG；微调更适合行为、格式与决策边界。
- **训练 loss 低不等于上线**：必须和好提示词下的基座比，并检查通用能力回归。

## 一句话主线

微调是一条工程链：数据、参数范围、训练目标、评估、部署与治理；PEFT 只是其中一种参数策略。

## 参考资料

- LoRA: Low-Rank Adaptation of Large Language Models（arXiv:2106.09685）：https://arxiv.org/abs/2106.09685
- Training language models to follow instructions with human feedback（InstructGPT，arXiv:2203.02155）：https://arxiv.org/abs/2203.02155
