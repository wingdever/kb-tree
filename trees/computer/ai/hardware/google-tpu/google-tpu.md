---
description: "Google TPU: v4, v5e/v5p, v6e Trillium, v7 Ironwood and v8 roadmap"
描述: "Google TPU：v4、v5e/v5p、v6e Trillium、v7 Ironwood 与 v8 路线"
name: "Google TPU"
名称: "Google TPU"
---

# Google TPU

TPU 是 Google 自研的矩阵加速器，只在 Google Cloud 以 Pod/SuperPod 形态提供；优势是 JAX/XLA 协同设计和大规模互联。

## 家族与代表型号

TPU v4、v5e、v5p、v6e（Trillium）、v7（Ironwood）；Ironwood 支持 9,216 芯片 SuperPod，主打推理与训练；v8t/v8i 已进入路线图。

## 能跑什么

单芯片 HBM 为数十到一百多 GB 级；Pod 可扩展到数千到近万芯片，适合超大模型预训练与高吞吐推理。

## 软件栈

JAX、XLA、PyTorch/XLA、TensorFlow、vLLM TPU 后端；编译器主导，算子由 XLA 融合与调度。

## 获取与适用

Google Cloud 专属，按 TPU 小时/订阅计费；不在公有云之外零售。

## 限制

只能在 Google Cloud 用；框架绑定 JAX/XLA；自定义算子与调试门槛高；供应受 Google 容量分配影响。

## 适合谁

适合已在 GCP/JAX 体系、需要大规模训练或低成本推理的团队。

## 参考资料

- https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-google-tpu-things-to-know/
- https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/training-performance-benchmarks-tpus/
- https://cloud.google.com/tpu/docs
