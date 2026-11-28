---
description: "Inference-specialized hardware: Cerebras, Groq, SambaNova, Tenstorrent, Etched, d-Matrix, Graphcore"
描述: "推理专用 ASIC/LPU：Cerebras、Groq、SambaNova、Tenstorrent、Etched、d-Matrix、Graphcore"
name: "Inference ASICs and LPUs"
名称: "推理专用 ASIC 与 LPU"
---

# 推理专用 ASIC 与 LPU

这类硬件的共同点是“为推理/Transformer 定制”，用牺牲通用性换取低延迟、高吞吐或能效；多数以云服务而非零售卡交付。

## 家族与代表型号

Cerebras CS-4/WSE-3 Turbo（晶圆级）、Groq LPU、SambaNova SN40L/SN50（RDU）、Tenstorrent Wormhole/Blackhole（RISC-V Tensix）、Etched Sohu（Transformer ASIC）、d-Matrix Corsair、Graphcore IPU。

## 能跑什么

单机/单 rack 可承载大模型推理；Cerebras 以整片晶圆提供超大片上 SRAM，Groq 以确定性片上 SRAM 换低延迟，Etched 只支持 Transformer 类模型。

## 软件栈

厂商专属编译器/运行时；Cerebras、Groq、SambaNova 主要走云 API；Tenstorrent 强调开源栈；Etched 绑定 Transformer。

## 获取与适用

多数通过厂商云/Neocloud 提供，少数可买整机；零售与自建门槛高。

## 限制

模型覆盖窄，新架构/新算子可能不支持；迁移成本高；供应商集中；不适合频繁换模型或多模态实验。

## 适合谁

适合固定模型、追求极低延迟或极低 token 成本的推理服务；不适合通用训练与快速实验。

## 参考资料

- https://www.cerebras.ai/blog/introducing-cerebras-cs-4
- https://groq.com/
- https://sambanova.ai/
- https://tenstorrent.com/
