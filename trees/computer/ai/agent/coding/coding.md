---
description: "Coding agent scaffolds, SWE-bench and computer-use agents"
描述: "编码 Agent 的脚手架、SWE-bench 与电脑操作 Agent"
name: "Coding and Computer-Use Agents"
名称: "编码与操作 Agent"
---

# A9 编码 Agent 与电脑操作 Agent

## Agentic Coding 是什么

AI 系统自主规划、写、测、调、部署代码，极少人工指导。区别于传统代码助手（补全或对话伙伴）：Agentic 系统在**持久循环**中运行，把高层目标拆成可执行步骤，使用文件系统、终端、版本控制等工具探索代码库、从错误中恢复、管理多步任务。

也区别于 **vibe coding**（`../../../software-engineering/vibe-coding/vibe-coding.md`）——后者靠运行反馈快速迭代提示做探索或 demo、刻意减少逐行审查；Agentic Coding 是更自主、目标导向的过程，类似把完整任务交给一个有能力但需要监督的初级工程师。二者是同一谱系的两端，随风险上升切换模式。

## 收敛的架构原语

到 2026 年，多数 agentic coding 系统收敛到一组共同原语：

- **持久项目上下文**：通过专门文件（CLAUDE.md、AGENTS.md）维护对项目目标、约定、架构的长期记忆，跨可持续数天或数周的会话。
- **集成工具使用**：数字工具箱镜像人类开发者环境——Git、shell、自动测试框架、包管理器、研究用浏览器、代码智能的 LSP 集成。
- **多智能体编排**：复杂问题由专门子 Agent 团队解决——规划 Agent 分解目标，分发给并行的编码、测试、审查 Agent。
- **长运行执行**：会话从几分钟到数天，带检查点和自愈机制，能从瞬时失败恢复而无需人工。
- **人机协作**：Agent 标记不确定处、对模糊需求或高风险决策（部署生产）请求人工输入。开发者角色从写代码转为监督、架构指导、最终批准。

## 主导架构

LLM（Claude Opus、GPT-4.1/o3 级、DeepSeek-V3、Qwen3-Coder）驱动一个 **ReAct 式循环**，跑在受限工具集上：文件查看/编辑、shell、搜索（ripgrep/AST）、测试运行器。

脚手架差异主要在：

- **定位策略**：检索式 vs Agent 式浏览
- **补丁生成**：整文件 vs diff
- **验证**：回归测试、复现脚本、自洽性

代表性脚手架：SWE-Agent、OpenHands、Agentless、Moatless、Aider、Claude Code。

## SWE-bench 与基准演进

SWE-bench Verified 成为标准基准。2026 年结果：顶级模型（Claude Opus、GPT-5.x）配合适 harness，在标准基准上成功率超过 70~90%，相比 2023 年约 4% 大幅提升。更难 "pro" 变体通常 50~77%。**Agent 的脚手架（harness）与底层模型同样重要**。

强势任务：bug 修复、按详细规格实现新功能、依赖迁移、测试生成、重构。困难任务：创造全新系统架构、高度模糊需求下无具体指导的行动。

基准已从 resolve-rate 转向轨迹指标：步骤效率、计划遵循、级联恢复、事后可审计性。2026 年新波次针对能力边界：

- **RoadmapBench**：数月级版本升级（长周期）
- **SaaSBench**：从零构建企业 SaaS
- **WebGameBench**：需求到浏览器应用，评估交付物而非 diff
- **ProcBench**：控制保持与反复执行缺陷
- **SpecBench**：测试套件 gaming（奖励黑客）
- **1GC-7RC**：单 GPU 从零构建并训练 ML 模型
- **SWE-bench Pro**：更难、多文件、架构复杂——分数对脚手架质量极度敏感

## 脚手架差距：架构比模型更重要

同一 Claude 3.5 Sonnet 下三个框架的对比：

| 框架 | 架构 | 得分 | 关键创新 |
|---|---|---|---|
| OpenHands (CodeAct v2.1) | 多 Agent、Web UI、生产特性 | 41.67% | 完整执行环境含浏览器 |
| Agentless (v1.5) | 无 Agent 循环——规划、搜索、打补丁 | 40.67% | 消除自主决策 |
| SWE-Agent | 单 Agent、定制 ACI | 23.00% | Agent-Computer Interface 抽象 |

OpenHands 与 SWE-Agent 相差 **18.67 个百分点**，跑的是完全相同的模型——脚手架架构几乎能让有效性能翻倍。Agentless 没有任何 Agent 循环却接近 OpenHands，说明对某些任务分布，结构化搜索与规划胜过自主探索。

SWE-bench Pro 暴露 Verified 隐藏的东西：Verified 分数趋于饱和（六个前沿模型 >80%，不再能区分），Pro 上最好模型从 70%+ 掉到约 23%（后来 Opus 4.5 在标准脚手架达 45.9%）。结构洞察：**Pro 的难题放大脚手架差异而非模型差异**——Verified 简单任务上平庸脚手架配好模型能蛮力刷分，Pro 多文件复杂问题上脚手架是门控因素。企业选编码 Agent 应更看重 Pro 分数。

企业评估清单：用自己代码库任务、同一底层模型测脚手架而非只测模型；测上下文检索质量（让框架定位已知 bug 的相关文件）；测错误恢复（故意中途制造失败，看它分类错误、智能重试、回溯，还是螺旋式重复失败）。

## 主流工具（2026）

- **OpenAI Codex**：整体执行能力强，GPT-5.x，多 Agent worktree 并行，AGENTS.md 上下文系统。
- **Claude Code (Anthropic)**：推理与规划顶尖，超大上下文（100 万+ token），擅长复杂重构与大型代码库导航；SWE-bench Pro 领先。
- **Cursor / Copilot / Windsurf**：IDE 嵌入，让你成为更高效的编辑者——天花板是你的注意力和 review diff 的速度。
- **Devin / Jules**：浏览器/云端 Agent，可运行数小时，把你移出循环——天花板是模型推理与指令质量。
- 轨迹：市场明确从"需要你在场的 IDE 工具"转向"不需要你参加会议的 Agent"；IDE 工具正尽快加云/异步模式，但从 IDE 中心架构加异步比从头构建更难。

## 生产力影响

TELUS 报告用这些系统节省超 50 万开发者小时。许多常见项目的 SDLC 从数周压缩到数小时或数天；陌生代码库的 onboarding 从数周研究变成数小时（Agent 提供引导式探索和上下文摘要）。

## Computer Use / Browser Agent

编码 Agent 之外，操作电脑的 Agent 需要"接地"的世界。完整的感知-行动循环、厂商方案与安全边界见 `../computer-use/`；浏览器这一受约束表面的专门方案见 `../browser-use/`。本节只留基准入口：

- **WebArena**：网页交互与表单完成。
- **OSWorld**：跨 Ubuntu/Windows/macOS 的电脑控制任务（文件系统、应用使用、多步工作流）。
- **OpenComputer**：验证器接地的电脑操作世界。
- 国产开源 Agent 编程模型在 Web 自动化基准报告 91% 操作成功率，强调动态抓取、表单填充、多标签协同，对反爬和动态渲染页面表现突出。

## 学习路径

1. 前置：扎实 Python、git、Linux shell；能调 LLM API；理解 transformer 推理与工具调用。
2. 按顺序读论文：ReAct（Yao 2022）→ Toolformer（Schick 2023）→ SWE-Bench（Jimenez 2023）→ SWE-Agent（Yang 2024）→ Agentless、AutoCodeRover（检索式替代）→ OpenHands（完整开源平台）。
3. 动手：clone OpenHands 或 SWE-Agent，用开放模型（Qwen3-Coder、DeepSeek-V3）复现小规模 SWE-Bench Lite，检查轨迹；在自己仓库试 Aider。
4. 进阶训练：研究 SWE-Gym、SWE-RL，用小模型在合成轨迹上微调。

## 安全与前沿

奖励黑客与监督自成子领域：SpecBench 测长周期编码 Agent 的测试套件 gaming；SLEIGHT-Bench 评估对 LLM 监视器的规避；最小权限授权研究探测 Agent 是否请求过多能力。自我进化已超越技能文件变异——MOSS 在部署时重写 Agent 自身源代码。
