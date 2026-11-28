---
description: "Background Tasks：慢操作放后台 — lesson 11 of learn-claude-code"
描述: "Background Tasks：慢操作放后台（learn-claude-code 第 11 节）"
name: "S11 Background Tasks"
名称: "Background Tasks：慢操作放后台"
---

# Background Tasks：慢操作放后台

第 11 节，把慢操作移出主循环。

## 问题

安装依赖、跑完整测试、构建项目可能持续几分钟。同步执行时，整个 Agent Loop 停在这次 Bash 调用上，后面不依赖它的工作也做不了。

## 机制

模型显式给 Bash 的 `run_in_background` 参数，Harness 用后台线程执行，先返回一个 `bg_id` 占位结果，让循环继续；后续轮次开始时收集已完成结果，以通知形式注入对话。

## 代码实现

`BackgroundManager` 保存任务、结果和完成队列；`start()` 登记并启动 daemon 线程，立即返回 ID；`collect()` 把完成结果变成通知。进程组清理避免留下孤儿子进程。

## 运行与观察

运行 `python s11_background_tasks/code.py`，启动一个慢命令，同时让它做别的事。观察主循环没有阻塞，完成通知在后续轮次出现。

## 边界

只有模型明确请求才进后台，不靠关键词猜测；后台任务没有依赖图，完成顺序不等于业务顺序。进程生命周期、输出大小和宿主机重启都要额外处理。

## 一句话

慢操作放后台，主循环继续思考。

## 参考资料

- 课程 README（第 11 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s11_background_tasks/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s11_background_tasks/code.py
