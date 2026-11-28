---
description: "Supervised fine-tuning: chat templates, loss masking, packing, hyperparameters and common errors"
描述: "SFT 流程：对话模板、损失掩码、packing、超参与常见错误"
name: "Supervised Fine-Tuning (SFT)"
名称: "SFT 监督微调"
---

# SFT 监督微调

SFT 用“输入 → 期望输出”的样本，把基座模型拉到任务格式与行为上。它的核心不是模型结构，而是数据格式、损失掩码与训练目标是否一致。

## 数据格式

- 用基座模型自带的 chat template 渲染 system/user/assistant 消息；不要手写另一套格式。
- 工具调用样本要保留工具名、参数与结果的结构；把工具输出当普通文本会教坏模型。
- 多轮样本要保留角色顺序与终止标记；截断时不要切断 assistant 的完整回答。
- 训练前打印几条渲染后的文本，肉眼检查特殊 token、换行与结束符。

## 损失掩码

- 只对 assistant 回答计算 loss，system 与 user 部分通常 mask 掉；否则模型会学习复述用户输入。
- 多轮对话中，每一轮 assistant 回答都应计算 loss，而不是只算最后一轮。
- 工具调用与工具结果的角色要按模板处理；哪些 token 参与 loss 要明确。
- 如果任务是指令跟随，输入部分的 loss 权重过高会稀释输出学习。

## 超参与 packing

- 学习率通常高于全参微调、低于预训练；从小值起，观察验证损失。
- epoch 不宜多，小数据尤其容易过拟合；验证损失上升就停。
- packing 能把多条短样本拼进一个序列，提高吞吐；但要防止跨样本注意力污染，使用正确的 attention mask。
- 梯度累积可以凑有效 batch；显存不够时优先加累积，不要盲目拉长序列。

## 常见错误

- chat template 不匹配：用错模板会静默产出坏 adapter，训练 loss 还可能看起来正常。
- 忘记 EOS：模型学会不收尾，推理时停不下来。
- padding 侧与 mask 不匹配，导致 loss 计算错位。
- 训练集与评测集泄漏：同一问题换个说法出现在两边，指标虚高。
- 只调格式却期待注入新事实；事实注入应先考虑 RAG。

## 一句话主线

SFT 教的是“怎么答”，不是“知道什么”；格式、掩码与终止符错一个，训练就会安静地失败。

## 参考资料

- Training language models to follow instructions with human feedback（InstructGPT，arXiv:2203.02155）：https://arxiv.org/abs/2203.02155
- Hugging Face TRL 文档（2026）：https://huggingface.co/docs/trl
