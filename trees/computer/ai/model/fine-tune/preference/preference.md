---
description: "Preference alignment after SFT: RLHF vs DPO, preference data, algorithms and risks"
描述: "偏好对齐：SFT 之后的对齐、RLHF 与 DPO、偏好数据、算法与风险"
name: "Preference Alignment"
名称: "偏好对齐"
---

# 偏好对齐

SFT 教模型“怎么答”，偏好对齐教它“哪种答法更好”。当任务存在多个正确风格、需要权衡有用性、安全性与简洁性时，只做 SFT 往往不够。

## SFT 之后为什么还要偏好

- SFT 的样本是“标准答案”，但真实场景常有多条合理路径。
- 模型可能学会冗长、讨好或过度拒答；偏好数据能直接表达取舍。
- 安全边界、语气、引用习惯等细微行为，用成对比较比用单条示范更好教。

## RLHF 与 DPO

- **RLHF**：先训奖励模型，再用 PPO 等算法优化策略；流程长、成本高，但可控性强。
- **DPO**：直接用“选中 / 拒绝”成对数据优化，跳过奖励模型，工程简单，是当前常用起点。
- **ORPO / KTO**：把 SFT 与偏好或单点反馈结合，减少对成对数据的依赖；选型要看数据形态。
- 没有偏好数据时，先不要硬上 RLHF；先把 SFT 与评测做扎实。

## 偏好数据

- 每条样本要有 chosen 与 rejected，差异要具体：事实、引用、语气、长度或安全边界。
- 标注指南要写清“为什么更好”，否则标注者各按各的偏好。
- 要防止长度偏见：更长的答案常被误判为更好；评估时控制长度。
- 保留难例与边界样本；只收简单对比，模型学不到细微差别。

## 风险

- **奖励黑客**：模型学会讨好评分器，而不是真正变好。
- **过度优化**：偏好指标涨，通用能力与多样性掉。
- **长度与风格偏见**：评分器偏好长答案，模型只会变啰嗦。
- **数据不可复现**：标注口径变了，前后版本无法比较。

## 一句话主线

偏好对齐优化的是“取舍”，不是“知识”；没有清晰偏好定义，RLHF 与 DPO 都只会放大标注偏见。

## 参考资料

- Direct Preference Optimization（DPO，arXiv:2305.18290）：https://arxiv.org/abs/2305.18290
- Training language models to follow instructions with human feedback（InstructGPT，arXiv:2203.02155）：https://arxiv.org/abs/2203.02155
