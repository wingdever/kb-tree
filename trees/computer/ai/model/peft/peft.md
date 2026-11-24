---
description: "SFT pipeline and LoRA/QLoRA/DoRA parameter-efficient tuning"
描述: "SFT 流程与 LoRA/QLoRA/DoRA 参数高效微调"
name: "Fine-Tuning and PEFT"
名称: "微调与 PEFT"
---

# M3 微调与 PEFT

## Prompt / RAG / SFT 决策

- 需要最新或海量外部事实 → **RAG**（推理时动态注入知识）。
- 需要改变输出风格、行为、格式（JSON/YAML/DSL、CoT、拒答边界）→ **SFT**。
- 两者都不是 → zero/few-shot prompt。

常见混合实践：**SFT 定格式规则与拒答边界，RAG 做动态知识注入**。

现代训练链路：预训练 → SFT（指令微调）→ RLHF/DPO（偏好对齐）→ 推理服务。

## 全参数微调 vs PEFT

- **全参数微调**：更新全部参数，拟合能力最强，但 70B FP16 约需 1TB 显存（AdamW 状态 + 梯度），且有灾难性遗忘风险。
- **PEFT**：冻结主干，只训练 0.1–1% 的额外参数，显存降 60–80%，产出几十 MB 的 adapter 权重。

## LoRA 原理

核心洞察（Hu et al. 2022）：适配新任务所需的权重更新 ΔW 本质低秩。对预训练权重 W₀ ∈ ℝ^(d×k)，不更新全矩阵，而是分解更新：

```
ΔW = (α/r) · B · A
A ∈ ℝ^(r×k)   Gaussian 初始化
B ∈ ℝ^(d×r)   零初始化
r ≪ min(d,k)  典型 8/16/32/64
α/r           缩放因子，稳定不同 r 下的训练动态
```

例：4096×4096 权重矩阵有 16.8M 参数；r=8 时 LoRA adapter 仅 65K，可训练参数减少 256×。

**2026 主流起点**：`r=16, α=16, target_modules="all-linear", use_dora=True`，4-bit NF4 量化。

### target modules 怎么选

- 早期只针对 q_proj、v_proj（2023 社区经验）。
- **2026 共识：`target_modules="all-linear"`**——对 7B–72B 模型，把 LoRA 用到所有线性层（q/k/v/o + gate/up/down）下游提升显著。
- 只做行为改变至少覆盖 attention 投影；要学新知识则包含 MLP 层（可训练参数与训练时间约翻倍）。

### 秩与 alpha 怎么选

- r=16 对多数任务（风格迁移、领域适配、输出格式化）足够。
- 学复杂新行为（如新工具集）用 r=32/64；>64 收益很小、接近全微调成本。
- 2026 有共识倾向 `alpha = r`（scale=1.0）；经典起点是 `alpha=2r`。训练不稳降 alpha，收敛太慢升 alpha。
- 挑选法：从 r=16 起，质量不够升到 r=32；若仍不够，问题多半在数据而非秩。

### LoRA dropout

数据集 >2000 条用 0.05；500–2000 用 0.1；<500 用 0.15。小数据集上简单有效的正则。Unsloth 优化路径下可设 0。

## QLoRA：消费级 GPU 微调大模型

QLoRA（Dettmers et al. 2023）三项创新：

1. **4-bit NormalFloat（NF4）**：针对正态分布权重优化的 4-bit 数据类型，最小化量化误差。
2. **双量化（Double Quantization）**：对量化常数再量化，省约 0.37 bit/参数。
3. **Paged Optimizers**：激活尖峰时用统一内存把 AdamW 状态卸载到 CPU RAM。

效果：8B 模型约需 6–8GB 显存（RTX 4090 24GB 可训）；70B 约 40–48GB（单张 A100 80GB 可训）。65B 模型全精度约 130GB → QLoRA 约 48GB。

## PEFT 家族（2024–2026 前沿）

| 变体 | 核心思想 | 何时用 |
|---|---|---|
| **LoRA** | 低秩矩阵注入冻结权重 | 基线，工具兼容性最好 |
| **QLoRA** | 4-bit NF4 量化基座上的 LoRA | 默认——单卡塞更大模型 |
| **DoRA** | 权重分解为幅度 + 方向，LoRA 只管方向 | 几乎总是——低秩下免费涨 1–4% |
| **rsLoRA** | 按 √rank 而非 rank 缩放 | 高秩（32–64）、复杂任务，修复梯度坍缩 |
| **PiSSA** | 用主奇异向量初始化 A/B | 收敛快 30%+，但对学习率更敏感 |
| **VeRA** | 冻结共享随机矩阵，只训缩放向量 | 多 adapter 大军团，参数更少 |
| **GaLore** | 把梯度投影到低秩子空间 | 全参数训练但优化器显存小 |
| **AdaLoRA** | 动态秩分配 | 不同层自适应重要性 |
| **LoftQ** | 量化感知初始化 | 量化 + LoRA 联合优化 |

**DoRA 要点**（NVIDIA）：把权重分解为幅度与方向，使更新与已有权重正交，改善条件数与稳定性，DoRA@r16 常追平 LoRA@r32–64。因幅度向量与低秩更新都能精确合并回基座，**零推理开销**。HF PEFT 用 `use_dora=True` 开启。

2026 默认推荐：**QLoRA + DoRA，r=16**；仅当留出集显示任务需要更多容量时升到 r=32 并配 rsLoRA。

## 实操代码（Unsloth + TRL）

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

model, tok = FastLanguageModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-8B-Instruct", max_seq_length=4096, load_in_4bit=True
)
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=16, lora_dropout=0,
    target_modules="all-linear", use_dora=True,
    use_gradient_checkpointing="unsloth",
)

# 关键：用基座模型的 chat template 格式化，否则静默产出坏 adapter
def fmt(ex):
    return tok.apply_chat_template(ex["messages"], tokenize=False)

trainer = SFTTrainer(
    model=model, tokenizer=tok,
    train_dataset=ds.map(lambda x: {"text": fmt(x)}),
    args=SFTConfig(
        per_device_train_batch_size=2, gradient_accumulation_steps=4,
        warmup_steps=20, max_steps=2000, learning_rate=2e-4,
        optim="paged_adamw_8bit", weight_decay=0.01,
        lr_scheduler_type="linear", eval_strategy="steps", eval_steps=200,
    ),
)
trainer.train()
model.save_pretrained_merged("merged", tok, save_method="lora")
```

## 训练配置要点

- 学习率：全微调 1e-5~2e-5；LoRA 1e-4~3e-4（比全微调高 5–10×）。
- epochs：1–3；<500 条最多 1–2 epoch，验证损失上升立即停。
- 优化器：`adamw_8bit` / `paged_adamw_8bit` 省优化器显存。
- bf16 优先于 fp16（Ampere+）。
- 梯度累积凑有效 batch。

## 评估与上线

- **永远和"好提示词下的基座模型"对比**——微调质量若只是略胜，则不值得。
- 两个决定上线的数字：留出集任务指标 + 通用能力 delta（MMLU/HellaSwag 前后对比，查灾难性遗忘）。任务涨分但 MMLU 掉 10 分 = 过拟合，需降 LR、减 epoch 或混入 5–10% 通用指令数据。
- **不要只看训练 loss**。
- vLLM 等可热插拔多 adapter：一个基座服务多租户/多任务，按请求路由到对应 adapter，还能做 A/B 测试——成本远低于托管多个全量模型。
- 权重合并：`save_pretrained_merged` 把 adapter 合回基座，推理零额外延迟。

## 常见坑

- **chat template 不匹配**：用 Llama token 训 Mistral 会静默破坏 adapter。务必打印 `tok.apply_chat_template(...)` 肉眼检查。
- 只针对 Q+V（过时做法）。
- epoch 过多。
- 不做 MMLU sanity check。
- LoRA 学到的是行为而非新知识时，误以为能注入事实——知识注入应交给 RAG。

## 参考资料

- LoRA: Low-Rank Adaptation of Large Language Models（arXiv:2106.09685）：https://arxiv.org/abs/2106.09685
- QLoRA（arXiv:2305.14314）：https://arxiv.org/abs/2305.14314
