---
description: "FPGAs for LLMs: AMD Versal, Altera Agilex; custom dataflow for small quantized models"
描述: "FPGA 与自适应 SoC：AMD Versal、Altera Agilex；小模型定制数据流"
name: "FPGAs and Adaptive SoCs"
名称: "FPGA 与自适应 SoC"
---

# FPGA 与自适应 SoC

FPGA 不是大模型的主流硬件，但在低延迟、确定性、特定算子加速与边缘场景有位置；代价是开发周期长、算子要自己写。

## 家族与代表型号

AMD Versal AI Edge/AI Prime、Altera Agilex 7/9、Xilinx Alveo 加速卡；可用 DSP/BRAM/UltraRAM 做定制数据流。

## 能跑什么

片上存储与逻辑资源有限，适合小模型、量化模型、特定层（如 Attention/GEMM）加速；大模型通常做 CPU/GPU 的卸载加速，而非独立承载。

## 软件栈

Vitis、Vitis AI、Quartus、OpenCL/HLS、PYNQ；需要手写 RTL/HLS 或使用厂商 IP。

## 获取与适用

开发板、加速卡、嵌入式模块；云上 FPGA 实例较少。

## 限制

开发门槛高、迭代慢；大模型算子映射困难；工具链与模型格式支持弱；不适合快速换模型。

## 适合谁

适合确定性低延迟、功耗受限、批量固定的边缘推理；不适合通用大模型训练/服务。

## 参考资料

- https://www.amd.com/en/products/adaptive-socs-and-fpgas/versal.html
- https://www.altera.com/products/fpga/agilex
- https://www.xilinx.com/products/boards-and-kits/alveo.html
