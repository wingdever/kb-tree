---
description: "AWS purpose-built AI chips: Inferentia2, Trainium1/2/3 and Trn3 UltraServer"
描述: "AWS 自研 AI 芯片：Inferentia2、Trainium1/2/3 与 Trn3 UltraServer"
name: "AWS Trainium and Inferentia"
名称: "AWS Trainium 与 Inferentia"
---

# AWS Trainium 与 Inferentia

AWS 的专用芯片只在 AWS 云上提供，用 Neuron SDK 把 PyTorch/JAX 模型编译到 Trainium/Inferentia，目标是把 token 成本压到最低。

## 家族与代表型号

Inferentia2（Inf2，推理）、Trainium1/Trn1、Trainium2/Trn2、Trainium3/Trn3；Trn3 UltraServer 可扩展到 144 颗芯片，主打训练、推理、MoE 与长上下文。

## 能跑什么

Trainium3 单芯片 HBM 为一百多 GB 级；UltraServer 级联后可覆盖万亿参数模型；Inferentia2 适合高吞吐推理。

## 软件栈

AWS Neuron SDK、NKI、PyTorch（torch-neuronx/TorchNeuron）、JAX、Hugging Face Optimum Neuron、SageMaker/EKS。

## 获取与适用

Amazon EC2 Trn/Inf 实例、SageMaker、EKS；只能在 AWS 内使用。

## 限制

绑定 AWS；算子覆盖与动态 shape 支持有限；迁移出 AWS 成本高；部分新模型需等 Neuron 适配。

## 适合谁

适合已经在 AWS 上跑训练/推理、追求单位 token 成本的团队。

## 参考资料

- https://aws.amazon.com/ai/machine-learning/trainium/
- https://awsdocs-neuron.readthedocs-hosted.com/en/v2.31.0/about-neuron/whats-new.html
- https://aws.amazon.com/ec2/instance-types/trn3/
