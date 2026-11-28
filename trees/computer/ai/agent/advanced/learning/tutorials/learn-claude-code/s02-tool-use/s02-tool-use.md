---
description: "Tool Use：加工具只加一个 handler — lesson 02 of learn-claude-code"
描述: "Tool Use：加工具只加一个 handler（learn-claude-code 第 02 节）"
name: "S02 Tool Use"
名称: "Tool Use：加工具只加一个 handler"
---

# Tool Use：加工具只加一个 handler

第 2 节，承接单工具循环，开始扩展工具面。

## 问题

只有 Bash 时，模型想把“读这个文件”变成行动，必须先把它翻译成 `cat`、引号、路径和转义。Harness 收到的也只是一整条不透明命令，后面很难按工具或路径做策略。

## 机制

把工具定义与执行拆成两张表：`TOOLS` 描述能力，`TOOL_HANDLERS` 把工具名映射到处理函数。循环只把 `run_bash()` 换成查表分发；新增工具只需加定义和 handler，循环结构不变。这就是本课的**工具分发**结构。

## 代码实现

五个基础工具是 `bash`、`read_file`、`write_file`、`edit_file`、`glob`；`safe_path()` 把路径限制在工作目录内。执行时用 `TOOL_HANDLERS[block.name]` 找到函数，把结构化参数传进去。

## 运行与观察

运行 `python s02_tool_use/code.py`，分别要求读文件、改一处文本、按模式找文件。观察模型发出的是具名工具和结构化参数，而不是拼出来的一条 shell。

## 边界

这些工具没有给 Agent 增加 Bash 做不到的原始能力，改善的是接口与可治理性。本节尚未加入权限审批，工具仍可直接执行。

## 一句话

工具不是新能力，是把模型意图变成结构化接口。

## 参考资料

- 课程 README（第 02 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s02_tool_use/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s02_tool_use/code.py
