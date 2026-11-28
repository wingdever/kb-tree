---
description: "A 17-lesson course that builds a Claude Code-like agent harness in Python, one mechanism per lesson"
描述: "用 Python 从零搭建 Claude Code 式 Agent Harness 的 17 节课程"
name: "Learn Claude Code Harness Course"
名称: "learn-claude-code：17 节 Harness 工程课"
---

# learn-claude-code：17 节 Harness 工程课

这门课拆的不是 Claude Code 的界面，而是它作为一个 **Agent Harness** 的结构：一个循环、工具、权限、hook、计划、子 Agent、技能、压缩、记忆、任务、后台、定时、团队、MCP、集成、workflow 与目标判断。每一节只增加一个机制，代码独立可跑。

## 核心主张

课程的前提是：**Agency 来自模型训练，Agent 产品 = Model + Harness。** 模型负责感知、推理与决策；Harness 提供工具、知识、观察、动作接口和权限边界。写 Agent 的大部分工作不是“替模型思考”，而是把模型能行动的世界搭好。

因此它反对把 Agent 等同于拖拽工作流或提示词链：固定 if-else 和节点图可以搭出流程，但搭不出开放决策。课程选择 Claude Code 作为样本，不是要求复制它，而是因为它把 Harness 的职责展示得足够完整。

## 课程路线

17 节主轨分五个阶段：

- **循环与工具**：先让模型能执行一条命令，再把工具变成结构化接口。
- **边界与扩展**：在工具执行前加权限，把日志、审批与副作用挂到 hook。
- **规划与上下文**：用计划稳住长任务，用子 Agent 隔离上下文，用技能按需加载知识，用压缩与记忆突破窗口。
- **持久化与协作**：把清单升级为任务图，把慢操作放后台，把触发扩展到时间，把单 Agent 扩展到团队，把工具来源扩展到 MCP。
- **集成与编排**：把机制装进同一个循环，用脚本编排固定流程，用独立判断器决定目标是否完成。

逐节清单在 `learn-claude-code.list.csv`，一行一课，列为 `name, group, source, url, note`；正文不重复 17 行表格。

## 怎么学

1. 克隆仓库，安装 `requirements.txt`。
2. 从 `.env.example` 建 `.env`，配置 `ANTHROPIC_API_KEY` 与 `MODEL_ID`。
3. 从 `s01_agent_loop/code.py` 开始，每节先读 README，再运行代码。
4. 不要跳章：后一节默认你已经理解前一节留下的循环与工具基线。
5. 每节至少改一个参数或加一个失败分支，观察 Harness 的行为变化。

环境需要 Python 与 Anthropic API Key；课程不依赖某个 Agent 框架，适合已经会写 Python、理解 `messages` 与工具调用基本结构的人。

## 版本说明

仓库当前主轨是根目录 `s01`–`s17`。`agents/` 与 `docs/` 保留旧的 12 节迁移轨，供旧链接使用；两套章节编号不一一对应。部分第三方文章写 12 节或 20 节，和当前主轨不一致；学习时以根目录的 17 节为准。

## 边界

- 这是 Harness 教学，不教模型训练、微调或 RL；它假设模型本身已经具备能力。
- 权限示例是字符串与规则匹配，不是完整安全边界；真实系统需要沙箱、最小权限与能力级授权。
- MCP 章节使用进程内模拟 server，不覆盖真实 transport、鉴权与网络故障。
- 集成章节是参考实现，不是生产产品：多租户、持久化、审计、并发与成本控制都要另行设计。

## 一句话主线

**模型负责聪明，Harness 负责让聪明能落地；17 节就是从一条 Bash 命令走到一个可治理、可恢复、可协作的 Agent 运行环境。**

## 参考资料

- shareAI-lab/learn-claude-code：https://github.com/shareAI-lab/learn-claude-code
- 课程站点：https://learn.shareai.run
- 仓库 README（17 节主轨与旧 12 节说明）：https://github.com/shareAI-lab/learn-claude-code/blob/main/README.zh.md
