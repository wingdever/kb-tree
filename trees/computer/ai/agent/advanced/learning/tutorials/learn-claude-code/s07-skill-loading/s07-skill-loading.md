---
description: "Skill Loading：用到时再加载 — lesson 07 of learn-claude-code"
描述: "Skill Loading：用到时再加载（learn-claude-code 第 07 节）"
name: "S07 Skill Loading"
名称: "Skill Loading：用到时再加载"
---

# Skill Loading：用到时再加载

第 7 节，从预加载转向按需知识。

## 问题

把 React 规范、SQL 风格、API 设计文档全部塞进 system prompt，能让模型看到，但每次调用都重复发送全文；当前只改 React 时，另外两份文档纯占上下文。

## 机制

启动时只扫描技能目录，把每个 `SKILL.md` 的 `name` 与 `description` 放进 system prompt 形成目录；模型需要完整说明时调用 `load_skill(name)`，正文作为 `tool_result` 追加。

## 代码实现

`SkillLoader.scan()` 遍历 `skills/*/SKILL.md`，解析 YAML frontmatter；`build_system_prompt()` 拼目录；`load_skill()` 读取完整正文。技能由人编写并只读，模型只负责选择。

## 运行与观察

运行 `python s07_skill_loading/code.py`，要求它按某个技能规范改代码。观察 system prompt 里先只有技能目录，模型调用后再出现完整正文。

## 边界

目录质量决定可发现性；描述写不清，模型就选不中。技能是本地可信文件，没有沙箱与来源校验；这里也没有语义检索，只靠模型读目录做选择。

## 一句话

先给目录，再按需加载正文。

## 参考资料

- 课程 README（第 07 节）：https://github.com/shareAI-lab/learn-claude-code/blob/main/s07_skill_loading/README.zh.md
- 本节代码：https://github.com/shareAI-lab/learn-claude-code/blob/main/s07_skill_loading/code.py
