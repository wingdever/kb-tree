---
description: "Context Compact：先整理，再总结 — lesson 08 of learn-claude-code"
描述: "Context Compact：先整理，再总结（learn-claude-code 第 08 节）"
name: "S08 Context Compact"
名称: "Context Compact：先整理，再总结"
---

# Context Compact：先整理，再总结

第 8 节，处理长任务的上限。

## 问题

读过的文件、命令输出和模型回复都留在 `messages` 里。任务越长，上下文越满，最后 API 直接返回 `prompt is too long`；工具结果通常是占用最大的部分。

## 机制

四步压缩管线，按信息损失和调用成本排序：先给工具结果做预算并转存大输出，再裁掉旧历史，再把旧工具结果替换成摘要，最后才让模型总结整段历史。这是本课的**上下文压缩**主线：能恢复的优先整理，不可恢复的才总结。

## 代码实现

`tool_result_budget` 在总字符超限时从最大结果开始转存到 `.task_outputs/tool-results/`，上下文只留路径和预览；`snip_compact`、`micro_compact`、`compact_history` 逐级处理；API 拒绝时再触发补救压缩。

## 运行与观察

运行 `python s08_context_compact/code.py`，让它连续读多个长文件。观察大结果被转存、上下文只留预览，以及空间仍不足时摘要如何接管。

## 边界

摘要一定丢细节；阈值是课程设定，不是通用最优值。压缩不是无限记忆，反复压缩会让早期约束变模糊，关键状态应外置到文件或任务系统。

## 一句话

先整理可恢复的，再总结不可恢复的。

## 参考资料

- 课程 README（第 08 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s08_context_compact/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s08_context_compact/code.py
