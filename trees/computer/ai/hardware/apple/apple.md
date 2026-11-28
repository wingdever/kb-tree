---
description: "Apple Silicon: M5 Max/M5 Ultra, unified memory up to 512GB, MLX"
描述: "Apple Silicon：M5 Max/M5 Ultra，统一内存最高 512GB，MLX"
name: "Apple Silicon"
名称: "Apple Silicon"
---

# Apple Silicon

Apple Silicon 用统一内存把 CPU/GPU/NPU 共享在同一块高带宽内存上，适合在本地跑中大型量化模型；优势是能效与隐私，不是峰值算力。

## 家族与代表型号

M5 Max、M5 Ultra（最高 512GB 统一内存、1.2TB/s 带宽）、M6 路线；Mac Studio/MacBook Pro 是主要载体。

## 能跑什么

统一内存可装下数百 GB 级模型；带宽远高于普通 PC，但低于数据中心 HBM；适合单机本地推理、微调与小规模服务。

## 软件栈

MLX、llama.cpp、Ollama、Core ML、PyTorch MPS；MLX 对 Apple GPU 优化较好。

## 获取与适用

零售 Mac/Mac Studio；按整机购买，不能单独买芯片。

## 限制

无 CUDA，部分算子/框架不支持；多机扩展弱；散热与持续负载受限；不适合大规模训练。

## 适合谁

适合个人/团队本地跑大模型、隐私敏感推理、轻量微调与开发。

## 参考资料

- https://www.apple.com/newsroom/2026/08/apple-introduces-m6-and-m5-ultra-for-a-big-leap-in-performance-and-ai-compute/
- https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/
- https://ml-explore.github.io/mlx/
