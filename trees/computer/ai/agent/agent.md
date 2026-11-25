---
description: "Knowledge tree for designing, building and evaluating agents"
描述: "Agent 开发：基础、架构、互操作、工程、运维与进阶"
name: "Agent Engineering"
名称: "Agent 开发"
---

# Agent 领域

这棵树讲的是怎么把 Agent 从想法做到能长期运行的服务。起点是一个等式：**Agent = 模型 + harness**，harness 再由 agent-loop、memory、tool 三块组成。绝大多数工程质量问题，最后都落在 harness 上，而不是模型上。

六个方向对应从设计到上线的生命周期，但**不必按顺序读**：遇到具体问题时按方向查，比从头读到尾有效。

## 生命周期上的六段

- **基础**：先划边界——什么该做成 Agent、什么做成工作流、什么只是个聊天框；再决定提示、上下文与外部知识各占多大比重。这一段的结论会决定后面所有取舍。
- **架构**：内部怎么转起来。循环形态、模式选择、单 Agent 还是多 Agent、关键控制流是否显式化、横切逻辑挂在哪。
- **互操作**：往外伸的手。工具契约决定能做什么，协议决定跟谁对话，技能把知识打包，渠道决定怎么触达用户。
- **工程**：怎么搭起来并证明它行。最小闭环、评测与黄金集、框架取舍、安全与权限边界。
- **运维**：上线后怎么跑稳。追踪与信号、成本与延迟、版本与灰度、多租户与隔离。
- **专项**：通用骨架之上的深挖。编码 Agent、云端运行形态、用 RL 训练、以及补齐体系的学习资源。

## 用这棵树的三条建议

1. **按问题查，不按目录背**。每个节点要能独立回答一个问题；读完一个节点就该能做出一个判断，而不是记住一堆术语。
2. **先看判断，再看方法**。带 `> 判断：` 的段落是这一页的结论，方法与数据都是为它服务的；时间紧就先读判断。
3. **警惕「更复杂 = 更好」**。多 Agent、图式编排、自主循环都是按失败代价选的，不是能力等级；每一层复杂度都要能说清它挡住了哪种具体失败。

## 一句话主线

Agent 的工程质量主要不取决于模型，而取决于 harness：先把边界与上下文定清楚，再选循环与协作形态，把外部接口标准化，用评测与安全护栏兜住，最后才谈规模化与专项优化。

## 参考资料

- Anthropic《Building effective agents》（Agent 与工作流的分界、五种工作流模式）：https://www.anthropic.com/engineering/building-effective-agents
- Anthropic《Effective context engineering for AI agents》（上下文是稀缺资源）：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
