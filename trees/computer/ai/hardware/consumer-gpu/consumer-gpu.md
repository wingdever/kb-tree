---
description: "Consumer GPUs for local LLMs: RTX 5090/4090/5080, Radeon RX 7900 XTX, Arc B580"
描述: "消费级 GPU：RTX 5090/4090/5080、Radeon RX 7900 XTX、Arc B580"
name: "Consumer GPUs"
名称: "消费级 GPU"
---

# 消费级 GPU

消费级 GPU 是本地跑大模型性价比最高的一类：单卡显存有限，但带宽高、软件成熟，适合量化模型与个人 Agent。

## 家族与代表型号

NVIDIA RTX 5090/4090/5080/5070 Ti、RTX 6000 Ada/Blackwell 工作站卡；AMD Radeon RX 7900 XTX、RX 9070 系列；Intel Arc B580/B 系列。

## 能跑什么

单卡显存从十几 GB 到数十 GB；适合量化后的中小模型、单机 Agent、图像/视频生成；大模型需多卡或 CPU offload。

## 软件栈

CUDA（NVIDIA）、ROCm（AMD）、oneAPI/SYCL（Intel）、llama.cpp、Ollama、vLLM、TensorRT-LLM。

## 获取与适用

零售显卡、整机、云游戏/工作站租赁；价格随供需波动。

## 限制

显存是硬上限；多卡互联弱；功耗与散热高；游戏卡不适合长时间满载；专业卡驱动/显存更大但更贵。

## 适合谁

适合个人开发者、小团队本地实验、隐私敏感与离线场景。

## 参考资料

- https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/
- https://www.amd.com/en/products/graphics/desktops/radeon.html
- https://www.intel.com/content/www/us/en/products/details/discrete-gpus/arc.html
