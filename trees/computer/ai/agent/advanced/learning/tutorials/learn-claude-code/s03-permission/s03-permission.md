---
description: "Permission：执行前先做权限判断 — lesson 03 of learn-claude-code"
描述: "Permission：执行前先做权限判断（learn-claude-code 第 03 节）"
name: "S03 Permission"
名称: "Permission：执行前先做权限判断"
---

# Permission：执行前先做权限判断

第 3 节，在工具执行前加边界。

## 问题

上一节的 Bash 不受 `safe_path` 保护。让 Agent“清理一下项目”，它可能真的执行删除命令；安全边界不能只写在提示词里。

## 机制

在工具执行前插入三道闸门：硬拒绝列表、按工具与参数匹配的规则、命中规则后的用户审批。硬拒绝优先，软询问次之，都不命中才放行。权限检查成为执行管线的一环。

## 代码实现

`DENY_LIST` 拦截明显危险命令；`PERMISSION_RULES` 判断工作区外读写、删除等需要确认的操作；`ask_user()` 在终端等待批准；`check_permission()` 把三道闸门串起来。

## 运行与观察

运行 `python s03_permission/code.py`，先请求工作区外的文件，再请求一条破坏性命令。观察哪些被直接拒绝、哪些进入人工确认，以及拒绝信息如何回到模型。

## 边界

字符串匹配只能演示权限闸门的位置，不能当作完整安全边界；绕过写法、编码变形和间接执行都可能漏过。真实系统需要沙箱、最小权限和能力级授权。

## 一句话

权限是工具执行前的门，不是提示词里的劝告。

## 参考资料

- 课程 README（第 03 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s03_permission/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s03_permission/code.py
