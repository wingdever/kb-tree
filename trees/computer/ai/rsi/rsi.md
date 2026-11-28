---
description: "Recursive Self-Improvement (RSI): AI systems improving the components that determine future capability, and what it does to ecosystem moats"
描述: "RSI（递归自我改进）：AI 改进决定未来能力的组件，以及它对生态壁垒的影响"
name: "Recursive Self-Improvement"
名称: "RSI（递归自我改进）"
---

# RSI（递归自我改进）

## 定义与缩写

在 AI 讨论里，RSI 通常指 **Recursive Self-Improvement，递归自我改进**：一个系统用当前能力去改进“决定未来能力”的组件——模型权重、提示与策略、工具与代码、数据与评估、甚至训练流程——然后用改进后的版本继续改进下一轮。关键不是“一次变强”，而是**改进能力本身也在变强**，形成复利循环。

> 注意缩写歧义：金融里的 RSI 是 Relative Strength Index（相对强弱指标）；医学里的 RSI 是 Repetitive Strain Injury（重复性劳损）。AI 语境下的 RSI 一般指递归自我改进。

## 循环由什么组成

| 组件 | 系统能改什么 | 为什么会影响下一轮 |
|---|---|---|
| 模型 | 权重、蒸馏、微调、RL、架构 | 直接决定推理与生成能力 |
| 策略 | Prompt、规划、工具调用策略 | 同样的模型，策略更好就表现更好 |
| 工具与代码 | 自己写工具、改代码、修 bug | 工具变强，后续任务成功率变高 |
| 数据与评估 | 自生成数据、自评分、难例挖掘 | 评估变准，改进方向才不跑偏 |
| 训练流程 | 数据配比、超参、课程、奖励 | 训练效率本身被优化 |

只要其中一环的改进能稳定传导到下一轮，就会出现“能力 → 改进能力 → 更强能力”的回路。反过来，如果评估不可靠、工具链不稳定、或者改进无法验证，循环就会断，变成“自我折腾”而不是 RSI。

## 三个层级

- **工具级自我改进**：Coding Agent 改自己的代码、优化器改 Prompt、Agent 自己写新工具。这是今天真实发生的，但通常有人类审查与测试闸门。
- **能力级 RSI**：模型参与改进自己的训练数据、评估器、奖励模型或训练配方，把改进结果回流到下一版模型。已有部分研究原型，但仍在人类设定的目标与安全边界内。
- **完全 RSI / 快速起飞**：系统能在没有人类有效监督的情况下，持续提高通用智能，且速度超过人类理解与验证能力。这是理论推演与 speculation，没有公开、可复现的实证。

把三层混在一起，就会得出过度结论：看到 Coding Agent 会改代码，就说“完全 RSI 已到来”；或者因为完全 RSI 没被证实，就否认工具级自我改进正在发生。

## 现实中的近似证据

- **AlphaEvolve**：Gemini 驱动的进化式编码 Agent，能搜索并改进算法与代码，在数学与工程问题上发现更优解。
- **Voyager**：Minecraft 中的终身学习 Agent，自己写技能代码、存技能库、迭代行为。
- **STOP**：Self-Taught Optimizer，让模型改进自己的推理与优化流程。
- **Self-Rewarding Language Models**：模型生成并评估自己的训练数据，用自评分继续训练。
- **Coding Agent 生态**：Agent 修自己的工具、写测试、根据失败日志改代码，已经是工程常态。

这些系统都展示了“改进回路”的局部形态，但离“完全 RSI”还差三件事：**开放目标、可靠自评估、无人监督下的安全验证**。

## RSI 与生态壁垒

这是一个**强命题**，不是共识。它成立的部分是：如果智能能力本身变成廉价、通用、可自我提升的商品，那么“靠某个模型能力领先”形成的老壁垒会快速衰减；开源权重、Agent 框架、API 聚合会让功能差距被迅速追平。

但它把“能力壁垒”误当成“全部壁垒”。生态壁垒至少还有六类，RSI 不会一并抹平：

| 壁垒 | RSI 的影响 | 为什么不会自动消失 |
|---|---|---|
| 模型能力 | 强侵蚀 | 前沿算力、数据、人才仍可能集中在少数机构 |
| 分发与渠道 | 弱侵蚀，甚至增强 | 用户入口、预装、平台规则、品牌信任难以复制 |
| 工作流与集成 | 弱侵蚀，甚至增强 | 深度嵌入业务后，迁移成本与责任边界是壁垒 |
| 数据与权限 | 不侵蚀 | 私有数据、授权、行业资质不能靠“更聪明”凭空获得 |
| 信任与合规 | 增强 | 责任归属、审计、监管牌照、保险与声誉需要时间 |
| 算力与资本 | 增强 | RSI 越强，训练与推理的资本门槛可能越高 |

所以更准确的说法是：**RSI 会削弱“静态能力壁垒”，但会把竞争转移到分发、数据、工作流、信任、算力与监管**。说“生态壁垒完全不存在”，只在“能力即产品、且能力可瞬间复制”的极窄假设下成立；现实里，能力越通用，差异化越往场景、权限与责任转移。

## 对开发者的含义

- 不要把护城河建在“某个模型功能”上；那是最容易被下一代模型或开源实现抹平的部分。
- 把投入放在**分发入口、深度工作流、私有数据与权限、可信责任链**上；这些不会因为模型变强而自动归零。
- 假设能力会商品化，设计可替换的模型层与评估层；但不要假设所有壁垒都消失，否则会低估合规、渠道与迁移成本。
- 如果做 Agent 产品，护城河更可能在“可审计的执行环境 + 行业连接器 + 失败恢复”上，而不是“用了哪个模型”。

## 常见误解

- **RSI = AGI**：不是。RSI 是一种改进动态；AGI 是能力水平。两者相关，但不能画等号。
- **RSI = 完全无人**：今天的近似系统仍有人类设定目标、审查代码、验证结果；完全无人监督是另一层。
- **RSI = 一夜起飞**：递归循环可能遇到评估瓶颈、数据瓶颈、算力瓶颈与安全闸门；不保证指数级。
- **RSI 时代没有壁垒**：把“能力壁垒”当成“全部壁垒”。分发、数据、信任、合规、资本仍然存在，而且可能更集中。

## 一句话主线

RSI 是“改进能力本身也在改进”的复利循环，不是某个产品；它会让静态能力壁垒变薄，但不会让生态壁垒归零——壁垒只是从“谁更聪明”转向“谁掌握分发、数据、工作流、信任与算力”。

## 参考资料

- I.J. Good, Speculations Concerning the First Ultraintelligent Machine（1965）：https://philpapers.org/archive/GOOSCT.pdf
- LessWrong: Recursive Self-Improvement 标签：https://www.lesswrong.com/tag/recursive-self-improvement
- AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms：https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- Voyager: An Open-Ended Embodied Agent with LLMs：https://voyager.minedojo.org/
- STOP: Self-Taught Optimizer：https://arxiv.org/abs/2310.02304
- Self-Rewarding Language Models：https://arxiv.org/abs/2401.10020
