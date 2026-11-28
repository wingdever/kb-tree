---
description: "Memory：跨会话保留重要信息 — lesson 09 of learn-claude-code"
描述: "Memory：跨会话保留重要信息（learn-claude-code 第 09 节）"
name: "S09 Memory"
名称: "Memory：跨会话保留重要信息"
---

# Memory：跨会话保留重要信息

第 9 节，把上下文延伸到会话之外。

## 问题

新会话的 `messages` 是空的。用户之前说过的偏好、项目背景和排查线索，下次还要重新说；完整 transcript 又不适合每次都塞给模型，旧事实还可能过期。

## 机制

一条记忆一个 Markdown 文件，frontmatter 记录名称、描述和类型；`MEMORY.md` 是索引。召回时先让模型看索引并选择相关条目，再加载正文；回合结束后提取可复用信息，定期合并重复与过期内容。

## 代码实现

`MEMORY_TYPES` 分为 user、feedback、project、reference；`write_memory_file()` 写文件并重建索引；召回按描述选择，正文按需读取； consolidation 在条目或体量超阈值时触发。

## 运行与观察

运行 `python s09_memory/code.py`，先告诉它一个长期偏好，结束会话再开新会话。观察它先看索引再召回正文；再写入重复偏好，观察整理阶段如何合并。

## 边界

存什么由模型判断，可能漏记、错记或把临时信息写成长期事实。文件存储适合单机与可读性，不适合多租户并发；隐私、保留期和删除策略都要宿主负责。

## 一句话

记忆是索引加按需召回，不是把历史全塞进 prompt。

## 参考资料

- 课程 README（第 09 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s09_memory/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s09_memory/code.py
