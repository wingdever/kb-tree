---
description: "DeepSeek context caching, usage accounting and cost optimization"
描述: "DeepSeek 上下文缓存、用量统计与成本优化"
name: "Context Caching and Cost"
名称: "上下文缓存与成本"
---

# 上下文缓存与成本

长 system prompt、few-shot 示例与多轮历史会在每次请求里重复发送。上下文缓存把稳定前缀留在服务端，命中部分不再重复计算——对高频、长上下文的 Agent 是数量级的成本差异。

## 缓存什么

- **稳定前缀**：system prompt、角色设定、工具定义、few-shot 示例、长文档片段。
- **多轮历史**：历史消息天然构成增长的前缀；把最新用户输入放最后，前面各轮即可命中。
- **变动内容后置**：时间戳、当前请求、随机采样结果放最后。前缀一处变动，后续全部失效。

## 命中条件

- 按 token 前缀匹配，通常要求从第一条消息起逐 token 一致。中间插入或改写任一早前 token，后续缓存失效。
- 缓存写入与命中是两步：首次请求建立缓存，后续请求命中。间隔过长缓存可能过期。
- 短于服务端最小 token 阈值的请求通常不进入缓存；阈值与保留时长以官方文档为准。

## 用量统计

- OpenAI 兼容格式的 `usage` 区分缓存命中与未命中的输入 token：`prompt_cache_hit_tokens` / `prompt_cache_miss_tokens`，输出 token 单独统计。
- Anthropic 兼容格式在最终 `message_delta.usage` 中给出 `input_tokens`、`cache_read_input_tokens`、`cache_creation_input_tokens`。
- 流式请求以最终 usage 为准，不要累加中间增量。

## 成本构成

一次请求的账单通常由**缓存命中输入 + 未命中输入 + 输出 token**相加；思考模式还可能计入推理 token；启用服务端 Web 工具另有搜索调用计费。价格按模型与通道不同且变化快，本页不展开数值。

## 省钱清单

- 稳定内容前置、变动内容后置，不要每轮重写 system prompt。
- 同一会话保持消息顺序追加；Chat Completions 不支持在中间插入工具调用。
- 用 `reasoning_effort` 控制思考强度；简单任务关思考或选低档。
- 把命中率纳入监控：缓存命中输入 token / 总输入 token。
- 输出是单价最高的部分，用 `stop`、`max_tokens` 与简洁提示控制长度。
- 图片与文件输入会增加输入 token，传入前先裁剪与压缩。

## 一句话主线

**把不变的内容固定在最前面，让重复请求只付新增部分的钱；命中率是可观测、可优化的工程指标，不是黑盒。**

## 参考资料

- DeepSeek API 文档：https://api-docs.deepseek.com
