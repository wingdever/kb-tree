---
description: "Full-parameter fine-tuning: when it is worth it, memory accounting, training strategy and risks"
描述: "全参数微调：适用条件、显存账、训练策略与风险"
name: "Full-Parameter Fine-Tuning"
名称: "全参数微调"
---

# 全参数微调

全参数微调更新模型全部权重，拟合能力最强，但显存、训练时间、服务副本与回滚成本也最高。它不是“比 PEFT 更高级”，而是另一种代价结构。

## 什么时候值得

- 任务与基座差异很大，PEFT 的容量不够，留出集长期上不去。
- 需要改变模型的知识或核心能力，而不只是输出风格与格式。
- 有足够数据、算力与评测能力，能承担多副本服务与回滚。
- 小数据、风格迁移、JSON 格式、拒答边界这类任务，优先 PEFT；全参更容易过拟合与遗忘。

## 显存账

全参数训练不只存权重，还要存梯度、优化器状态与激活：

- 混合精度下，权重与梯度占一份，AdamW 还要动量与方差两份。
- 激活与临时张量随 batch、序列长度与模型宽度增长，长上下文尤其明显。
- ZeRO 分片、FSDP、梯度检查点、CPU offload 能降低单卡压力，但会增加通信与实现复杂度。
- 先算“每卡能不能放下 + 能不能跑得动”，再谈训练速度；只算权重会低估显存。

## 训练策略

- 学习率通常比 PEFT 低一个量级，避免把预训练能力冲掉。
- 少 epoch、早停、保留通用指令数据做 replay，降低灾难性遗忘。
- 用 warmup 与稳定 decay；监控梯度范数、损失尖峰与验证集。
- 定期 checkpoint，记录数据版本、超参与评测结果，便于回滚与复现。

## 风险

- **灾难性遗忘**：任务指标涨，通用能力掉；必须做通用能力回归。
- **成本**：训练贵只是一部分，多副本服务、冷启动与扩容更贵。
- **迭代慢**：每次改数据都要重训全量，不适合快速试错。
- **回滚难**：全量权重体积大，版本管理与灰度切换成本高。

## 一句话主线

全参微调买的是容量，不是免费效果；先证明 PEFT 不够，再承担全量的成本。

## 参考资料

- ZeRO: Memory Optimizations Toward Training Trillion Parameter Models（arXiv:1910.02054）：https://arxiv.org/abs/1910.02054
- Hugging Face Transformers 训练文档（2026）：https://huggingface.co/docs/transformers/training
