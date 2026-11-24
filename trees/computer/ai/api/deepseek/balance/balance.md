---
description: "DeepSeek Get User Balance API and balance deduction rules"
描述: "DeepSeek 余额查询接口与扣费顺序"
name: "DeepSeek Balance API"
名称: "余额 API"
---

# 余额 API（Get User Balance）

`GET https://api.deepseek.com/user/balance` 返回账户余额。

## 响应

- `is_available`：余额是否足够发起 API 调用。
- `balance_infos[]`：
  - `currency`：`CNY` 或 `USD`。
  - `total_balance`：可用总额，含赠送余额与充值余额。
  - `granted_balance`：未过期赠送余额。
  - `topped_up_balance`：充值余额。

## 工程用法

- 调用前可用 `is_available` 做前置检查，但不要依赖它替代错误处理：余额不足仍会返回 402。
- 扣费时**优先使用赠送余额**，其次充值余额；模型按 token 计费，Search/Fetch 按次、OCR 按页、ASR 按时长、TTS 按字符。
- 多币种账户可能返回多条 `balance_infos`，按 `currency` 区分，不要只取第一条。

## 一句话主线

**一个 GET 拿回可用性与分币种余额；赠送余额优先扣除，费用按各 API 的计费单位分别累计。**

## 参考资料

- DeepSeek 余额查询 API：https://api-docs.deepseek.com
