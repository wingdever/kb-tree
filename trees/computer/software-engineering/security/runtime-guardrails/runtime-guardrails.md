---
description: "Operational guardrails that turn a compromise from invisible into detectable: authentication throttling, daily digests, ownership audits and alert routing"
描述: "运行期护栏：认证限速、每日摘要、包归属巡检与告警闭环，让入侵从不可见变为可发现"
name: "Runtime Guardrails"
名称: "运行期护栏"
---

# 运行期护栏

加固决定"能不能进来"，护栏决定"进来之后多久被发现"。只有加固没有护栏，机器会在无人知晓的状态下持续被使用。

## 认证面的自动化

速率限制与自动封禁处理的是"尝试"：它们降低噪声、减少日志体积、抬高爆破成本。但它们不改变认证配置本身——开着密码认证时，护栏只是把命中时间往后推。自动化要配合"认证面最小化"才有意义。

## 每日摘要

固定时间输出一行，进入人看得见的通道（邮件、IM、值班群）：

- 失败登录次数与来源分布
- 非白名单来源的成功登录
- 首次出现的新来源地址
- 出站与入站流量的比例变化
- 新增的自启单元与定时任务

摘要留在主机上等于没有摘要。它必须离开主机，并且在正常日子里也出现，否则"没有消息"和"没人看"无法区分。

## 归属巡检

定期核对两件事：系统目录里的可执行文件是否都有包归属，自启单元与定时任务是否可以解释来源。攻击者的持久化必然落在这两类清单里，包归属是成本最低的筛子。

## 告警闭环

主机安全类 agent 显示"运行中"不等于"生效"。需要确认三点：告警能到达人、有明确的责任人、误报白名单是显式维护的。安装了但无人响应，与没安装等价。

## 变更留痕

对配置目录、自启目录、授权公钥保留基线快照，使"什么时候多了这个文件"可以被回答。没有基线，取证只能靠推断；有基线，异常是可见的增量。

## 参考资料

- fail2ban 文档：https://fail2ban.readthedocs.io/
- systemd.timer 手册：https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
