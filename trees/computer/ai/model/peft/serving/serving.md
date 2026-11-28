---
description: "Fine-tuning serving: merge vs adapter, quantization, inference engines, rollout and rollback"
描述: "微调部署：合并与 adapter、量化、推理引擎、灰度与回滚"
name: "Fine-Tuning Serving"
名称: "微调部署"
---

# 微调部署

训练出权重不等于能上线。部署要决定权重怎么组织、显存怎么省、请求怎么路由、出问题怎么回滚。

## 合并还是 adapter

- **合并**：把 LoRA 权重合回基座，推理零额外层，延迟最低；每个任务一份全量权重，存储与切换成本高。
- **Adapter 热插拔**：一个基座服务多个 adapter，按请求路由；节省显存，适合多租户、多任务与 A/B。
- 合并后难以多任务共存；adapter 路由增加框架复杂度与版本管理成本。
- 选择标准是“任务数量、延迟预算、显存预算、回滚频率”，不是哪个更时髦。

## 量化

- 部署量化与训练量化不是一回事；QLoRA 的 4-bit 是训练省显存，不自动等于推理最优。
- GPTQ、AWQ、GGUF 等格式各有生态与精度差异；上线前用真实任务评测。
- 量化会放大长尾错误；安全拒答、工具调用与结构化输出要单独回归。
- 先量化再合并、还是先合并再量化，要按框架支持与精度实测决定。

## 推理服务

- vLLM、TGI、SGLang 等引擎支持连续批处理、PagedAttention 与多 adapter；按吞吐、延迟与功能选。
- 多 adapter 路由要固定命名与版本，避免请求打到错的任务。
- 监控首 token 延迟、吞吐、显存、错误率与超时；量化后尤其要看长输出。
- 结构化输出、工具调用与停止符要在服务层再验一遍。

## 灰度与回滚

- 先小流量灰度，对比基线模型的采纳率、追问率、投诉率与任务完成率。
- 保留基座与旧 adapter 的版本，出问题能一键切回。
- 记录模型版本、数据版本、量化配置与评测结果，保证可追溯。
- 回滚演练要真做，不要只写在文档里。

## 一句话主线

部署的目标不是“把模型跑起来”，而是“在延迟、成本与质量之间可监控、可灰度、可回滚”。

## 参考资料

- vLLM 文档（2026）：https://docs.vllm.ai/
- Hugging Face PEFT 文档（2026）：https://huggingface.co/docs/peft
- GPTQ（arXiv:2210.17323）：https://arxiv.org/abs/2210.17323
- AWQ（arXiv:2306.00978）：https://arxiv.org/abs/2306.00978
