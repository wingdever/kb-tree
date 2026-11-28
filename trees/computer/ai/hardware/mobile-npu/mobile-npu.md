---
description: "Smartphone NPUs: Apple A-series, Snapdragon 8 Elite, Dimensity 9500, Exynos"
描述: "手机 NPU：Apple A 系列、骁龙 8 Elite、天玑 9500、Exynos"
name: "Smartphone NPUs"
名称: "手机 NPU"
---

# 手机 NPU

手机 NPU 是出货量最大的 AI 硬件，但受内存、散热与功耗限制；能跑的是量化后的小中模型与端侧 Agent，不是数据中心级大模型。

## 家族与代表型号

Apple A19/A19 Pro、Qualcomm Snapdragon 8 Elite Gen 5、MediaTek Dimensity 9500、Samsung Exynos 2600 等；各家 NPU 架构与算力口径不同。

## 能跑什么

手机内存通常为数十 GB 级，适合参数量较小的量化模型、语音/视觉/摘要类任务；长上下文与大模型会触发内存与散热瓶颈。

## 软件栈

Apple Core ML、Qualcomm QNN、MediaTek NeuroPilot、Samsung ENN、Android LiteRT/NNAPI；模型需量化与算子适配。

## 获取与适用

随手机/平板出货，不能单独购买；开发者通过厂商 SDK 调用。

## 限制

内存带宽与容量小；持续推理会降频；算子覆盖有限；Android 碎片化严重；无法训练。

## 适合谁

适合端侧语音、视觉、输入法、个人助理与隐私推理；不适合通用大模型服务。

## 参考资料

- https://developer.apple.com/machine-learning/core-ml/
- https://www.qualcomm.com/products/mobile/snapdragon/smartphones
- https://developer.android.com/ai/hardware-acceleration
