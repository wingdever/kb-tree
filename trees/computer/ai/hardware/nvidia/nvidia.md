---
description: "NVIDIA data-center GPUs: A100, H100, H200, B200/B300, GB200/GB300 NVL72"
描述: "NVIDIA 数据中心 GPU：A100、H100、H200、B200/B300、GB200/GB300 NVL72"
name: "NVIDIA Data Center GPUs"
名称: "NVIDIA 数据中心 GPU"
---

# NVIDIA 数据中心 GPU

NVIDIA 是当前大模型训练与推理最完整的一条栈：GPU、NVLink/NVSwitch、DGX/HGX 系统、CUDA 与 TensorRT-LLM 一起交付。

## 家族与代表型号

A100/A800、H100/H800、H200、B200/B300、GB200/GB300 NVL72、L40/L4/L20 推理卡，以及 RTX PRO 服务器版。A100/H100 是上一代主力，H200 提升 HBM 容量与带宽，B200/B300 进入 FP4 与更大 HBM 时代，GB200/GB300 把 Grace CPU 与 Blackwell GPU 组成机架级系统。

## 能跑什么

单卡显存从数十 GB 到数百 GB；NVL72 把 72 张 GPU 连成一个 NVLink 域，适合万亿参数 MoE、长上下文与高并发推理；消费级卡适合中小模型。

## 软件栈

CUDA、TensorRT-LLM、Triton、vLLM、SGLang、NIM、NCCL、Nsight。生态最成熟，模型与算子覆盖最广。

## 获取与适用

公有云、DGX/HGX 整机、OEM 服务器、工作站与消费卡；中国区有 H20/H800 等合规型号，供应与出口管制会变化。

## 限制

功耗与散热高，整机成本高；CUDA 绑定深，迁移到其他栈要重做算子与评估；先进型号供应受出口管制影响。

## 适合谁

适合从训练到推理的全栈需求，尤其是需要成熟软件、算子库和多卡互联的团队。

## 参考资料

- https://www.nvidia.com/en-us/data-center/dgx-b200/
- https://www.nvidia.com/en-us/data-center/gb200-nvl72/
- https://developer.nvidia.com/deep-learning-performance-training-inference
