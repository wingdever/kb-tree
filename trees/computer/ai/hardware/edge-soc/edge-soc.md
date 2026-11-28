---
description: "Edge AI SoCs: Snapdragon X2 Elite, Ryzen AI Max+ 395, Jetson Orin/Thor, Intel Lunar Lake"
描述: "端侧 SoC 与迷你机：Snapdragon X2 Elite、Ryzen AI Max+ 395、Jetson Orin/Thor、Intel Lunar Lake"
name: "Edge SoCs and Mini PCs"
名称: "端侧 SoC 与迷你机"
---

# 端侧 SoC 与迷你机

端侧 SoC 把 CPU、GPU、NPU 和统一内存集成在一颗芯片里，适合笔记本、迷你机、机器人与边缘盒子；能效优先，绝对算力低于数据中心。

## 家族与代表型号

Qualcomm Snapdragon X2 Elite/X Elite、AMD Ryzen AI Max+ 395（Strix Halo，最高 128GB 统一内存）、NVIDIA Jetson Orin/Thor、Intel Lunar Lake、Apple M 系列也属于这一类。

## 能跑什么

统一内存可装下中大型量化模型；NPU 算力为数十到百 TOPS 级；适合本地 Agent、视觉、语音与中小模型推理。

## 软件栈

Qualcomm QNN/GenieX、AMD Ryzen AI/ROCm、NVIDIA JetPack/TensorRT、Intel OpenVINO、llama.cpp、ONNX Runtime。

## 获取与适用

零售笔记本/迷你机/开发板；Jetson 可单独买模块。

## 限制

内存带宽低于数据中心 GPU；NPU 算子覆盖有限；散热与持续功耗受限；不同 SoC 的软件栈差异大。

## 适合谁

适合端侧 AI、机器人、隐私本地推理、轻量 Agent；不适合大模型训练。

## 参考资料

- https://www.qualcomm.com/snapdragon/laptops-and-tablets/consumer/ai
- https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo/ryzen-ai-max-plus-395.html
- https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/
