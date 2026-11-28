---
description: "CPU inference: Intel Xeon AMX, AMD EPYC, ARM Neoverse/Graviton, llama.cpp and OpenVINO"
描述: "CPU 跑大模型：Intel Xeon AMX、AMD EPYC、ARM Neoverse/Graviton、llama.cpp/OpenVINO"
name: "CPUs for LLMs"
名称: "CPU 运行大模型"
---

# CPU 运行大模型

CPU 不是大模型训练的主力，但能跑量化后的小中模型、做 CPU offload、承担预处理与低并发推理；优势是普遍可得、内存大、生态通用。

## 家族与代表型号

Intel Xeon 6（AMX）、AMD EPYC（AVX-512）、ARM Neoverse/Graviton、Apple/Ampere 等 ARM 服务器；桌面 x86 与 Apple Silicon 也可跑量化模型。

## 能跑什么

靠系统内存而不是显存，能装下比单卡更大的权重，但内存带宽远低于 HBM；适合中小模型、低并发、边缘与隐私场景。

## 软件栈

llama.cpp、OpenVINO、oneDNN、PyTorch CPU、ONNX Runtime、ggml；ARM 上可用 NEON/i8mm。

## 获取与适用

任何服务器/PC 都有；云上按 vCPU/内存计费。

## 限制

带宽低，decode 慢；多路 CPU 扩展性有限；大模型吞吐不适合；AMX/AVX 支持因型号而异。

## 适合谁

适合边缘、离线、隐私敏感、低并发场景；也适合做 GPU 推理的 host 与预处理。

## 参考资料

- https://www.intel.com/content/www/us/en/products/docs/accelerators/ai-accelerators.html
- https://github.com/ggml-org/llama.cpp
- https://docs.openvino.ai/
