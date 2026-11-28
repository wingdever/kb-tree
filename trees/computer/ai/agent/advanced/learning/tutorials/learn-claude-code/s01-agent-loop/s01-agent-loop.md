---
description: "Agent Loop：一个循环就够了 — lesson 01 of learn-claude-code"
描述: "Agent Loop：一个循环就够了（learn-claude-code 第 01 节）"
name: "S01 Agent Loop"
名称: "Agent Loop：一个循环就够了"
---

# Agent Loop：一个循环就够了

主轨第 1 节，入口课；后面所有机制都挂在这个循环上。

## 问题

模型能输出一条 bash 命令，但输出完就停：它不会自己执行，也看不到执行结果，更不会根据结果继续推理。人被迫在模型与终端之间来回粘贴，成了中间层。

## 机制

用 `while True` 把“模型调用、工具执行、结果回填”串起来。响应里出现 `tool_use` 就执行工具并把 `tool_result` 追加回 `messages`；没有 `tool_use` 就退出。这个最小 Agent Loop 只配一个 Bash 工具，先证明循环本身能产生行动。

## 代码实现

`agent_loop()` 把用户问题放进 `messages`，调用 `client.messages.create(..., tools=TOOLS)`，追加 assistant 内容，筛出 `tool_use` block，执行 `run_bash()`，把结果作为新的 user 消息追加。循环不关心命令内容，只关心“还有没有工具调用”。

## 运行与观察

运行 `python s01_agent_loop/code.py`，让它“列出目录并运行某个脚本”。观察第一次工具结果如何回到模型，以及模型在拿到结果后继续发起下一条命令，最后用自然语言收尾。

## 边界

Bash 没有任何权限边界，也没有沙箱；这是教学用的最小闭环，不是可上线的执行环境。循环也缺少完整的轮次上限、超时和错误恢复。

## 一句话

一个循环把模型从“会说”变成“会做”。

## 参考资料

- 课程 README（第 01 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s01_agent_loop/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s01_agent_loop/code.py
