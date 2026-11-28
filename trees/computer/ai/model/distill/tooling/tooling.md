---
description: "Distillation tooling by maturity: open-source trainers, synthetic data pipelines and managed cloud services"
描述: "蒸馏工具套件：按成熟度分开源训练器、数据合成与云托管"
name: "Distillation Tooling"
名称: "蒸馏工具套件"
---

# 蒸馏工具套件

有成熟工具，但没有一套通吃。先看你要哪种教师信号：黑盒响应、白盒 logit、推理链、Agent 轨迹；不同信号的成熟度差一个量级。

## 成熟度分层

- **响应 / 推理蒸馏**：最成熟。教师生成答案或推理链，学生做 SFT；任何好用的 SFT 工具都能承接。
- **Logit / 特征蒸馏**：中等成熟。需要教师权重或 logits，训练器要支持双模型前向与 KL/JSD 损失。
- **On-policy 蒸馏**：快速演进。学生自己生成，教师逐 token 打分；需要 teacher server 与 rollout 基础设施。
- **Agent 轨迹蒸馏**：还不成熟。需要环境、工具沙箱与多轮轨迹记录，通常要自己写 harness。
- **剪枝后再蒸馏**：生产优化工具较成熟，但和纯蒸馏不是同一类产品。

## 开源训练器

| 工具 | 强项 | 适合 |
| --- | --- | --- |
| Hugging Face TRL | GKD、Distillation、GOLD、MiniLLM 等训练器；与 Transformers 生态贴合 | 第一套要跑通的 logit 或 on-policy 蒸馏 |
| Arcee DistillKit | Logit 蒸馏与 hidden states 蒸馏；支持跨架构 | 白盒蒸馏、跨模型家族迁移 |
| torchtune | 原生 KD recipe；单机与 FSDP 分布式 | Llama 系单机/多卡教学与实验 |
| ms-swift | GKD、OPD-RL、OPSD；Megatron 并行；中文生态 | ModelScope / 国产模型、多机训练 |
| EasyDistill | 黑盒与白盒蒸馏；数据合成、SFT、排序与 RL | 想用一套流水线做数据与训练 |
| KDFlow | 教师走 SGLang、学生走 FSDP2；支持 off-policy/on-policy 与跨分词器 | 大教师、多机、性能敏感的实验 |
| MiniLLM | 反向 KL、on-policy 研究实现 | 研究 reverse KL 与生成式蒸馏 |
| NVIDIA ModelOpt / NeMo | 剪枝 + 蒸馏 + 部署链路 | 生产压缩、TensorRT-LLM 部署 |

TRL 的优势是生态与可组合性，不是唯一选择；DistillKit 的强项是白盒与跨架构；KDFlow 更适合把教师推理与学生学习解耦。NVIDIA NeMo 当前主要支持 logit-pair 蒸馏与特定模型族，选前先看限制。

## 数据合成

- **distilabel**：用 DAG 组织生成、评判、改写与去重，产出 SFT/偏好数据；它不是训练器，常与 TRL、ms-swift 搭配。
- **EasyDistill**：把数据合成、教师生成、质量评估与导出串成流水线，适合黑盒蒸馏的数据生产。
- **自建脚本**：当任务有专用验证器（单元测试、SQL、工具沙箱）时，自建采样与拒绝逻辑通常比通用工具更贴任务。

合成数据只解决“有数据”，不解决“数据对不对”；验证器与留出集仍要自己建。

## 云托管

- **Amazon Bedrock Model Distillation**：自动用教师生成响应、做数据合成、切分训练/验证并微调学生；适合已经在 AWS 上的团队。
- 其他云厂商的蒸馏/微调产品在快速变化，选前确认三件事：支持哪些教师与学生、是否允许跨模型族、数据与输出归谁。
- 托管方案通常只做响应蒸馏，不暴露 logit；要白盒蒸馏仍然要自建或用开源训练器。

## 选型建议

- **第一次做**：先用 TRL 的 GKD 或“教师数据 + SFT”跑通基线，再决定要不要上 on-policy。
- **中文 / ModelScope 生态**：ms-swift 或 EasyDistill 更顺手，模型与数据链路更近。
- **大教师、多机、长轨迹**：看 KDFlow、ms-swift Megatron、NVIDIA NeMo；先把教师推理与学生学习解耦。
- **跨架构**：DistillKit 的 hidden states 或 TRL GOLD 的跨分词器方案。
- **只要响应蒸馏**：普通 SFT 工具就够，不必上双模型训练器。
- **Axolotl / LLaMA-Factory**：做响应蒸馏可以，但不是开箱即用的 logit 蒸馏；真白盒蒸馏要自己改损失与双模型前向。

## 一句话主线

蒸馏工具的选择顺序是“先定教师信号，再定训练范式，最后选工具”；黑盒响应蒸馏已经很成熟，白盒 logit 与 Agent 轨迹蒸馏仍要承担基础设施成本。

## 参考资料

- How to Distill an LLM: Tools, Recipes and Costs（2026-09）：https://global-distillation.com/developer
- Hugging Face TRL 文档（2026）：https://huggingface.co/docs/trl
- Arcee AI DistillKit：https://arcee-ai-distillkit.my.canva.site/
- torchtune 知识蒸馏教程（Llama3.1 8B → Llama3.2 1B）：https://pytorch.org/torchtune/stable/tutorials/llama_kd_tutorial.html
- ms-swift 知识蒸馏文档（GKD / OPD-RL / OPSD）：https://swift.readthedocs.io/en/latest/Instruction/Distillation.html
- EasyDistill（EMNLP 2025 Demo）：https://aclanthology.org/2025.emnlp-demos.60/
- KDFlow：A User-Friendly and Efficient Knowledge Distillation Framework（2026）：https://arxiv.org/html/2603.01875
- Amazon Bedrock Model Distillation 文档（2026）：https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/model-distillation.html
- Distilabel 文档（2026）：http://distilabel.argilla.io/1.1.1/
- NVIDIA：Pruning and Distilling LLMs Using TensorRT Model Optimizer（2025-10）：https://developer.nvidia.com/blog/pruning-and-distilling-llms-using-nvidia-tensorrt-model-optimizer
