---
description: "Goal Loop：停止由判断器决定 — lesson 17 of learn-claude-code"
描述: "Goal Loop：停止由判断器决定（learn-claude-code 第 17 节）"
name: "S17 Goal Loop"
名称: "Goal Loop：停止由判断器决定"
---

# Goal Loop：停止由判断器决定

第 17 节，从轮次结束扩展到目标完成。

## 问题

循环一直把“模型不再调用工具”当作结束。但对“修到测试全过”“完成所有验收项”这类目标，模型停手只说明这一轮结束，不等于目标完成；它可能漏做，也可能自认为做完。

## 机制

`/goal` 是会话级 Stop hook：保存可检查的完成条件；主模型不再调用工具时，先由独立判断器读完成条件和对话记录，返回 `ok`、`reason`、`impossible`。未完成就把理由追加回同一段 `messages`，继续下一轮。

## 代码实现

`GoalController` 持有目标与判断器；`evaluate_after_turn()` 在主循环准备退出时调用；判断器是独立模型调用，没有工具，只能看 transcript；`StopDecision` 决定放行还是继续，`SessionResult` 返回最终状态。

## 运行与观察

运行 `python s17_goal_loop/code.py`，输入 `/goal` 加一个可检查条件，例如测试退出码为零。观察主模型停手后判断器如何拦截、给出缺失证据，再让循环继续。

## 边界

判断器看不到文件与命令，只能根据对话中已出现的证据判断；完成条件必须可检查，否则会变成主观评审。自动继续有轮次上限，后台任务未结束时应先等待，不能无限自循环。

## 一句话

停止由模型提出，完成由独立判断器决定。

## 参考资料

- 课程 README（第 17 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s17_goal_loop/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s17_goal_loop/code.py
