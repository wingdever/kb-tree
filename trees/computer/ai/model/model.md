---
description: "Knowledge tree for the model engineering lifecycle"
描述: "模型工程全链路知识树导航"
name: "Model Engineering"
名称: "模型工程"
---

# 模型工程知识树

本目录覆盖模型本身的全链路：从分词、预训练、并行训练、微调对齐、distill压缩，到推理部署与eval，以及multimodal与rl。每个知识点自成一个目录。

## 建议顺序

造模型全链路：tokenizer → pretrain → distributed → peft → distill → inference。选型与eval：eval → inference。理论基础：rl → peft 的偏好对齐部分。multimodal独立成篇。

## 与其他领域的关系

- 模型能力eval与 Agent 行为评估是两个层次：这里评模型。
