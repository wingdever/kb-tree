---
description: "Intel AI hardware: Gaudi 2/3, Xeon 6 AMX, Arc Pro GPUs, oneAPI"
描述: "Intel AI 硬件：Gaudi 2/3、Xeon 6 AMX、Arc Pro GPU、oneAPI"
name: "Intel Gaudi and Xeon"
名称: "Intel Gaudi 与 Xeon"
---

# Intel Gaudi 与 Xeon

Intel 走三条线：Gaudi 专用加速器、Xeon CPU 的 AMX 矩阵扩展、Arc Pro 显卡；共同点是 oneAPI 与相对开放的以太网 scale-out。

## 家族与代表型号

Gaudi 2、Gaudi 3（HL-325L/HL-335/HL-338 PCIe/HLB-325 基板）、Xeon 6（AMX）、Arc Pro B 系列、Max 系列 GPU。Gaudi 3 内置大量以太网端口，强调标准以太网组网。

## 能跑什么

Gaudi 3 单卡 HBM 为一百多 GB 级；适合 LLM 推理与微调、企业 RAG；Xeon AMX 适合小模型与 CPU 侧推理/预处理；Arc Pro 适合工作站与边缘。

## 软件栈

oneAPI、Intel Gaudi Software、PyTorch、vLLM、Hugging Face Optimum、OpenVINO；Gaudi 支持主流 Transformer。

## 获取与适用

Dell 等 OEM 服务器、Intel AI Cloud、公有云实例、工作站显卡。

## 限制

Gaudi 软件生态与算子覆盖弱于 CUDA；部分模型需适配；Arc 显存与带宽不适合大模型训练。

## 适合谁

适合企业推理、成本敏感型微调、已有 Intel 服务器体系的团队。

## 参考资料

- https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi.html
- https://habana.ai/products/gaudi3/
- https://www.intel.com/content/www/us/en/developer/tools/oneapi/overview.html
