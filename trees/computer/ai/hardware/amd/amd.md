---
description: "AMD Instinct: MI300X, MI325X, MI350X/MI355X, MI350P, MI400/MI450X/MI455X"
描述: "AMD Instinct：MI300X、MI325X、MI350X/MI355X、MI350P、MI400/MI450X/MI455X"
name: "AMD Instinct"
名称: "AMD Instinct"
---

# AMD Instinct

AMD Instinct 是 NVIDIA 之外最成熟的数据中心 GPU 路线，核心卖点是单卡大显存、开放 ROCm 与较好的性价比。

## 家族与代表型号

MI300X、MI325X、MI350X/MI355X、MI350P PCIe 卡；2026 年继续推进 MI400/MI450X/MI455X（CDNA 5）。MI350 系列主打大显存与 MXFP4/FP8，MI350P 面向标准 PCIe 服务器。

## 能跑什么

单卡 HBM 从一百多 GB 到近三百 GB；8 卡 UBB 平台可提供数 TB 级 HBM，适合大模型训练与高吞吐推理。

## 软件栈

ROCm、HIP、vLLM、SGLang、PyTorch、Triton；算子覆盖在追赶 CUDA，主流模型基本可用，冷门算子仍需适配。

## 获取与适用

OEM 服务器、云厂商实例、超算中心；MI350P 可进现有 PCIe 机箱。

## 限制

ROCm 成熟度与算子覆盖不如 CUDA；部分框架/库要打补丁；多卡互联与整机生态仍在建设。

## 适合谁

适合希望避开 NVIDIA 单一供应、需要大显存与开放软件栈的团队。

## 参考资料

- https://www.amd.com/en/products/accelerators/instinct/mi350.html
- https://www.amd.com/en/blogs/2026/amd-delivers-its-broadest-mlperf-inference-6-1-submission.html
- https://www.amd.com/en/products/specifications/accelerators.html
