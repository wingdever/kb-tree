---
description: "Chinese AI accelerators: Cambricon, Biren, Hygon, Moore Threads, MetaX, Enflame, Kunlunxin, Iluvatar"
描述: "国产 GPU/NPU：寒武纪、壁仞、海光、摩尔线程、沐曦、燧原、昆仑芯、天数智芯"
name: "Chinese GPUs and NPUs"
名称: "国产 GPU 与 NPU"
---

# 国产 GPU 与 NPU

国产 AI 芯片不是单一产品，而是一批架构与软件栈各异的厂商；共同目标是替代 NVIDIA/AMD 的通用 GPU 与专用 NPU。

## 家族与代表型号

寒武纪 MLU/思元、壁仞 BR100/BR104、海光 DCU、摩尔线程 MTT S4000/S5000、沐曦 C500/C600、燧原、昆仑芯、天数智芯等；各自有训练卡与推理卡。

## 能跑什么

单卡显存从数十 GB 到数百 GB；可组万卡集群，但实际可用规模取决于软件栈与互联。

## 软件栈

寒武纪 BANG、壁仞 BIRENSUPA、海光 ROCm 兼容栈、摩尔线程 MUSA、沐曦 MXMACA、燧原 TopsRider、昆仑芯 PaddlePaddle 适配、天数 Iluvatar CoreX。

## 获取与适用

中国区云厂商、智算中心、信创项目、部分零售卡；海外获取困难。

## 限制

生态高度碎片化，框架/算子适配参差；部分厂商软件成熟度不足；供应与制程受限；选型要按具体模型验证。

## 适合谁

适合中国区信创、自主可控、特定模型已适配的团队；不适合要求开箱即用 CUDA 生态的场景。

## 参考资料

- https://www.cambricon.com/
- https://www.birentech.com/
- https://www.mthreads.com/
- https://www.metax-tech.com/
