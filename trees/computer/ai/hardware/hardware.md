---
description: "Hardware families that can run large models: data-center GPUs, TPUs, Trainium, Ascend, Chinese accelerators, ASICs, CPUs, Apple Silicon, consumer GPUs, edge SoCs, mobile NPUs and FPGAs"
描述: "可以运行大模型的硬件家族：数据中心 GPU、TPU、Trainium、昇腾、国产加速器、ASIC、CPU、Apple Silicon、消费卡、端侧 SoC、手机 NPU 与 FPGA"
name: "Hardware for Large Models"
名称: "可以运行大模型的硬件"
---

# 可以运行大模型的硬件

严格意义上的“所有 SKU”列不完，也没有稳定答案：同一代芯片有不同板卡、显存、互联与整机形态，新型号还在按月发布。可行的口径是**按能承载大模型的架构家族收口**。截至 2026 年 11 月，主流可核验的是 14 个家族，每个家族下再列代表型号。

## 清单

| 家族 | 代表型号 | 主要用途 | 软件栈 | 获取方式 |
|---|---|---|---|---|
| NVIDIA 数据中心 GPU | A100、H100、H200、B200/B300、GB200/GB300 NVL72 | 训练 + 推理全栈 | CUDA、TensorRT-LLM、vLLM、NCCL | 云、DGX/HGX、OEM |
| AMD Instinct | MI300X、MI325X、MI350X/MI355X、MI400 系列 | 大显存训练/推理 | ROCm、HIP、vLLM | OEM、云、超算 |
| Intel Gaudi 与 Xeon | Gaudi 2/3、Xeon 6 AMX、Arc Pro | 企业推理、微调、CPU 侧 | oneAPI、OpenVINO、Gaudi SW | OEM、云、工作站 |
| Google TPU | v4、v5e/v5p、v6e Trillium、v7 Ironwood | 大规模训练/推理 | JAX、XLA、PyTorch/XLA | 仅 Google Cloud |
| AWS Trainium/Inferentia | Inferentia2、Trainium1/2/3、Trn3 UltraServer | 低成本训练/推理 | Neuron SDK、NKI | 仅 AWS |
| 华为昇腾 | 910B/910C、950PR/950DT、Atlas 900/950 | 国产超节点训练/推理 | CANN、MindSpore | 中国区政企/云 |
| 国产 GPU/NPU | 寒武纪、壁仞、海光、摩尔线程、沐曦、燧原、昆仑芯、天数 | 信创与特定模型 | 各家私有栈 | 中国区云/整机 |
| 推理 ASIC/LPU | Cerebras、Groq、SambaNova、Tenstorrent、Etched、d-Matrix、Graphcore | 低延迟/高吞吐推理 | 厂商编译器/云 | 云为主，少数整机 |
| CPU | Xeon 6 AMX、EPYC、ARM Neoverse/Graviton | 小中模型、offload、边缘 | llama.cpp、OpenVINO、oneDNN | 任何服务器/PC |
| Apple Silicon | M5 Max/M5 Ultra、M6 路线 | 本地大模型、隐私推理 | MLX、llama.cpp、Core ML | 零售 Mac |
| 消费级 GPU | RTX 5090/4090/5080、Radeon RX 7900 XTX、Arc B580 | 本地量化模型、Agent | CUDA/ROCm/oneAPI、llama.cpp | 零售显卡/整机 |
| 端侧 SoC/迷你机 | Snapdragon X2 Elite、Ryzen AI Max+ 395、Jetson Orin/Thor、Lunar Lake | 本地 Agent、机器人、边缘 | QNN、OpenVINO、JetPack | 零售整机/开发板 |
| 手机 NPU | Apple A 系列、骁龙 8 Elite、天玑 9500、Exynos | 端侧语音/视觉/小模型 | Core ML、QNN、NeuroPilot、LiteRT | 随手机出货 |
| FPGA/自适应 SoC | Versal AI Edge/Prime、Agilex 7/9、Alveo | 特定算子、低延迟边缘 | Vitis、Quartus、HLS | 开发板/加速卡 |

## 判断标准

选硬件先看五个量，而不是先看 TOPS：

1. **显存/内存容量**：决定能不能装下权重、KV Cache 与激活；容量不够，算力再高也跑不起来。
2. **内存带宽**：decode 阶段逐 token 读权重与 KV Cache，带宽往往比峰值算力更决定速度。
3. **算力与精度**：prefill/训练看矩阵算力，FP8/FP4/INT8 支持决定能不能吃到低精度收益。
4. **互联**：多卡训练看 NVLink/Infinity Fabric/ICI/NeuronLink/UnifiedBus；没有高带宽互联，多卡等于多台孤岛。
5. **软件栈**：CUDA、ROCm、CANN、XLA、Neuron、oneAPI 决定模型能不能跑、算子要不要重写。

## 三条路线

- **数据中心 GPU**：NVIDIA、AMD、Intel。通用性最好，训练推理都能做，代价是功耗、价格与供应。
- **专用 ASIC/NPU**：TPU、Trainium、昇腾、Groq、Cerebras、Etched。单位成本/延迟更优，但模型覆盖窄、迁移成本高。
- **端侧/消费硬件**：Apple Silicon、RTX、端侧 SoC、手机 NPU、CPU、FPGA。能效与可获得性好，但内存、带宽、散热限制明显。

## 端侧边界

端侧能跑“大模型”，但通常是**量化后的中小模型**，不是数据中心级全参数训练。统一内存能解决“装得下”，不等于“跑得快”：带宽、散热、NPU 算子覆盖才是瓶颈。手机 NPU 更适合语音、视觉、摘要与个人助理，不适合长上下文通用推理。

## 选型顺序

1. 先定任务：训练、微调、离线推理、在线高并发，还是端侧 Agent。
2. 再定模型规模与精度：权重 + KV Cache 需要多少内存。
3. 再看带宽与互联：decode 是否带宽瓶颈，多卡是否需要高带宽域。
4. 再看软件：目标模型与框架是否在官方支持列表里。
5. 最后看供应、功耗、机房与总成本。

## 边界与“所有”

- 这张表是**架构家族清单**，不是 SKU 清单；同一家族内不同板卡的显存、带宽、互联可能差一倍。
- 没有列入并不等于不能跑：任何有足够内存和算力的 CPU/GPU/FPGA 都能跑某个量化模型；“能跑”与“跑得动、跑得省”是两件事。
- 新芯片发布很快，选型要用官方数据表与实测，不要拿本文当永久规格表。
- 供应与出口管制会改变可获取性，尤其是 NVIDIA 先进型号、华为昇腾与国产加速器。

## 一句话主线

能跑大模型的硬件分三层：**数据中心 GPU 做通用训练推理，专用 ASIC/NPU 做极致成本或延迟，端侧/消费硬件做本地与隐私**；选型先看内存与带宽，再看软件栈，最后才看峰值算力。

## 参考资料

- NVIDIA DGX B200：https://www.nvidia.com/en-us/data-center/dgx-b200/
- NVIDIA GB200 NVL72：https://www.nvidia.com/en-us/data-center/gb200-nvl72/
- AMD Instinct MI350：https://www.amd.com/en/products/accelerators/instinct/mi350.html
- Intel Gaudi 3：https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi.html
- Google Ironwood TPU：https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-google-tpu-things-to-know/
- AWS Trainium：https://aws.amazon.com/ai/machine-learning/trainium/
- 华为昇腾：https://www.hiascend.com/
- 摩尔线程：https://www.mthreads.com/
- Cerebras CS-4：https://www.cerebras.ai/blog/introducing-cerebras-cs-4
- Apple M5 Ultra：https://www.apple.com/newsroom/2026/08/apple-introduces-m6-and-m5-ultra-for-a-big-leap-in-performance-and-ai-compute/
- NVIDIA RTX 5090：https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/
- Qualcomm Snapdragon X2 Elite：https://www.qualcomm.com/snapdragon/laptops-and-tablets/consumer/ai
- AMD Versal：https://www.amd.com/en/products/adaptive-socs-and-fpgas/versal.html
