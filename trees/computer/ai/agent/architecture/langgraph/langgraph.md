---
description: "Stateful graph orchestration with checkpoints, resume and interrupts"
描述: "带状态图、检查点、恢复与中断审批的编排框架实战"
name: "LangGraph In Depth"
名称: "LangGraph 深度"
---

# A5 LangGraph 深度

普通的 Agent 循环（调用→调用→回灌）在进程崩溃时就失效——对话和花掉的钱一起蒸发。LangGraph 的换个心智模型：**显式的节点与边组成的图，状态是一等公民，每个 super-step 后存到 checkpointer**。这一个改变免费换来持久化执行、人在回路和时间旅行。

## 核心概念对照

| 术语 | 通俗说法 | 实际含义 |
|---|---|---|
| State graph | "Agent 即状态机" | 类型化状态 + 节点 + 边 + reducer |
| Checkpointer | "持久化后端" | 每个节点后序列化状态；支持恢复 |
| Reducer | "状态合并器" | 把当前状态与节点更新合并的函数 |
| Conditional edge | "分支" | 由状态函数选择的边 |
| Subgraph | "嵌套图" | 作为另一张图节点的图 |
| Durable execution | "从失败恢复" | 用精确状态从最后成功节点重启 |
| Supervisor | "路由 LLM" | 中央分派器，委派给专门子 Agent |
| Swarm | "P2P Agent" | Agent 通过共享工具交接，无中央路由 |

## 状态与 Reducer

状态是 `TypedDict`（或 Pydantic 模型）。字段可带 **reducer**，声明新值如何与旧值合并——这是对话记忆的关键：

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]   # 追加，而非覆盖
    topic: str
```

`add_messages` 把新消息追加到历史而非替换，所以每轮模型看到完整对话。

> 常见错误：列表状态忘记 reducer。没有 `Annotated[list, add_messages]`，每个节点会**覆盖** messages 列表，Agent 在第一次工具调用后丢失所有上下文，然后你会花一小时困惑模型为什么一直重复。

## 建图

```python
from langgraph.graph import StateGraph, START, END

def analyze(state: State) -> dict:
    return {"messages": [{"role": "assistant", "content": f"Researching: {state['topic']}"}]}

def synthesize(state: State) -> dict:
    return {"messages": [{"role": "assistant", "content": "Final summary here."}]}

builder = StateGraph(State)
builder.add_node("analyze", analyze)
builder.add_node("synthesize", synthesize)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", "synthesize")
builder.add_edge("synthesize", END)
graph = builder.compile()
```

只有 `compile()` 后才得到实现标准 Runnable 接口（`invoke`、`stream`、`ainvoke`、`astream`）的 `CompiledStateGraph`；这个分离让 LangGraph 能在编译期校验图并挂上持久化。

图在你想要的地方是确定性的（边、手编码节点），在需要的地方是 LLM 驱动的（选择工具的 Agent 节点）。**单一图中混合确定性与模型驱动步骤是 LangGraph 的核心优势**。

## 条件边与 ReAct 循环

```python
from langgraph.prebuilt import ToolNode

builder.add_node("tools", ToolNode(tools))

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "call_tools"
    return "done"

builder.add_conditional_edges(
    "model", should_continue,
    {"call_tools": "tools", "done": END},
)
builder.add_edge("tools", "model")   # 工具跑完后回到模型
```

这一条条件边 + 从 tools 回到 model 的边，就是整个 ReAct 循环：推理→行动→观察→重复，直到模型不再请求工具。`ToolNode` 读取最新 AI 消息上的 `tool_calls`，执行对应函数，把每个结果包装成模型下一轮可读的 tool message。

因为图可循环，必须有停止条件与兜底：LangGraph 强制 `recursion_limit`（默认 25 supersteps），超过抛 `GraphRecursionError`。合法工作流需要更多步时用 `graph.invoke(input, {"recursion_limit": 50})`，但把触限当作"路由函数永不返回终止键"的信号。

## Checkpointer 与 thread_id

上面的图在 `invoke()` 返回后忘记一切。编译时挂 checkpointer，在每个 **super-step**（所有调度节点运行的一个 tick）后持久化：

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()   # 仅开发用——重启即丢失
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "alice"}}
graph.invoke({"topic": "Transformers", "messages": []}, config)
graph.invoke({"topic": "Transformers", "messages": []}, config)
# 第二次调用恢复同一 thread，通过 add_messages 追加
```

每个 super-step 边界产生一个 **checkpoint**——通道值快照 + 下一步排队的节点。`thread_id` 选择运行属于哪段对话历史。

## 崩溃恢复就是再次 invoke

**没有特殊的"恢复" API**。执行中途崩溃，用同一个 `thread_id` 再次调用图即可。LangGraph 加载最新 checkpoint，从队列中下一个节点继续。状态从磁盘往返与在内存中无异——持久化和进程重启恢复是同一个操作。

要复现错误答案：从旧 checkpoint 重跑，或用 `graph.update_state()` 修补历史 checkpoint 后沿修正分支继续——**像 git branch 一样管理 Agent 运行**。

## 人在回路：interrupt

Checkpoint 让暂停成为可能。`interrupt()` 保存 checkpoint 并交还控制权；人工输入到达后，图从那个精确点恢复。等待可持续几分钟到几天，远超任何进程的生命周期，因为运行状态按 thread 持久在磁盘上。

```python
from langgraph.types import interrupt, Command

def approval_node(state: State):
    decision = interrupt({"question": "Send this email?"})
    return {"approved": decision}
```

人工审阅后，用 `Command(resume=...)` 恢复。旧式做法是编译时 `interrupt_before=["tools"]`，在每个工具调用前暂停：应用检查待执行工具，批准（`graph.invoke(None, config)`）、修改状态（`graph.update_state(config, ...)`）或取消。凡是写数据库、发邮件、转钱的动作都应先过审批节点。

## 流式

```python
for event in graph.stream(
    {"messages": [HumanMessage(content="...")]},
    config, stream_mode="updates"
):
    for node_name, update in event.items():
        print(f"[{node_name}] {update}")
```

`stream_mode`：`"updates"`（每节点状态差异）、`"values"`（每节点后完整状态）、`"messages"`（LLM 生成的 token）。

## 记忆：短期与长期

- **短期**：运行内——状态中的对话历史。
- **长期**：跨运行——checkpointer + 独立长期存储（store）。通过工具集成外部记忆系统（Mem0 或自定义）。

## 三种拓扑

- **Supervisor**：中央路由 LLM 分派给专门子 Agent。`create_supervisor()`（langgraph-supervisor）；不过 LangChain 团队 2026 年推荐直接用工具调用实现，以更紧地控制上下文。
- **Swarm / P2P**：Agent 通过共享工具表面直接交接，无中央路由；系统记住最后活跃的是哪个 Agent，以便从正确的专家恢复。
- **Hierarchical**：监督者管理子监督者，实现为嵌套子图。

## 生产要点

- **选对 checkpointer**：`MemorySaver` 重启全丢；`SqliteSaver` 在容器里需要持久卷挂载（否则重启等于内存）；`PostgresSaver` 用于多进程、并发线程。容器里以 SQLite 开发、生产换 Postgres，通常是一行改动。
- **保持 checkpoint 精简**：单个 checkpoint 超过约 50KB，把载荷移到外部存储（S3），状态里只存引用。状态每个字段都要付序列化时间和 LLM 上下文预算。
- **子图只用一个 checkpointer**：只编译**父图**时挂 checkpointer；子图挂 checkpointer 会造成重复命名空间和膨胀状态。
- **不要把状态与对话历史混为一谈**：状态是图需要的一切——待执行工具调用、重试计数器、中间检索结果、用户偏好。全塞进 `messages` 会让提示词巨大且困惑模型。非消息状态用专门字段。
- **不要跨用户共享 thread_id**：checkpointer 以 thread_id 为键；两个用户命中同一 thread 会看到彼此的对话历史。按用户、按会话生成 thread_id，当作 session token 对待。
- **不要在节点内给每个工具包 try/except**：LangGraph 已隔离节点失败并可通过 checkpointer 重试；节点内手动异常处理常吞掉本应暴露为失败运行的错误。
- **节点返回部分更新**：只返回改动的字段；不要直接修改输入状态对象，始终返回新 dict。
- **非确定性节点要小心**：恢复假定节点输入产生相同状态更新；随机种子、墙上时钟、外部 API 结果必须被捕获。

## 何时用 / 不用

**用**：控制流需要循环（ReAct、重试、自我批评）；Agent 必须能崩后恢复；想要一等公民的人工审批门；需要向前端流式输出中间状态；已用 LangChain 组件；工作流有 5+ 步骤且带条件分支。

**不用**：Agent 只是一次 LLM 调用 + 一次工具调用（直接用 LLM SDK）；需要严格 TypeScript 类型（考虑 Mastra 或 Vercel AI SDK）；团队零 LangChain 经验且是一次性脚本；需要毫秒级路由（图编译与分发开销虽小但真实存在）；纯线性无分支的工作流（普通函数顺序调用更清晰）。

## 参考资料

- LangGraph 官方概览：https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph 持久化与 Checkpointer：https://docs.langchain.com/oss/python/langgraph/persistence
- langchain-ai/langgraph 仓库：https://github.com/langchain-ai/langgraph
