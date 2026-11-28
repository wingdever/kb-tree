---
description: "Cron Scheduler：按时间启动任务 — lesson 12 of learn-claude-code"
描述: "Cron Scheduler：按时间启动任务（learn-claude-code 第 12 节）"
name: "S12 Cron Scheduler"
名称: "Cron Scheduler：按时间启动任务"
---

# Cron Scheduler：按时间启动任务

第 12 节，把触发从用户输入扩展到时间。

## 问题

“每天早上跑测试”“每半小时查 CI”这类需求，不能靠用户每次到点再发 prompt。Harness 需要记住执行时间，到点把任务放进队列，并在 Agent 空闲时交给循环。

## 机制

用五段式 Cron 表达式保存计划；调度线程持续检查本地时间，命中后把 `[Scheduled] prompt` 放进队列；队列等待 Agent 空闲再启动一轮。`pending_delivery` 与 `last_fired` 防止同一分钟重复触发。

## 代码实现

`CronJob` 保存表达式、prompt、是否循环、是否持久化；`validate_cron()` 检查字段数量与范围；`schedule_job()` 保存任务；`poll_due_jobs()` 每秒匹配并入队；持久化文件支持重启后恢复。

## 运行与观察

运行 `python s12_cron_scheduler/code.py`，注册一个每分钟执行的任务。观察到点后 prompt 进入队列，Agent 空闲时才被消费，而不是打断正在进行的轮次。

## 边界

使用本地时间，跨时区与夏令时要宿主处理；只支持五段表达式的一个子集。进程不在运行时不会触发，错过的任务也不会自动补跑。

## 一句话

定时不是闹钟，是把 prompt 在正确时间放进队列。

## 参考资料

- 课程 README（第 12 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s12_cron_scheduler/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s12_cron_scheduler/code.py
