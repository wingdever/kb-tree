---
description: "LangChain @tool, args_schema, ToolNode and headless tools"
描述: "LangChain 的装饰器、参数 schema、ToolNode 与无头工具"
name: "LangChain Tools Specification"
名称: "LangChain 工具规范"
---

# 06 LangChain Tools 规范

LangChain 的 `create_agent` 是"模型 + harness"的最小 Agent 框架：harness = 提示词 + 工具 + 中间件。

## 工具的本质

工具是可调用函数，有明确定义的输入输出，被传给 chat model。模型根据对话上下文决定何时调用、传什么参数。底层模型处理工具调用的细节见官方文档；用 LangSmith 追踪工具调用与调试错误。

## 创建工具

### 基础：@tool 装饰器

函数 docstring 默认成为工具描述。**类型注解是必需的**——它们定义工具的输入 schema。docstring 应信息充分且简洁。

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

命名：优先 snake_case（如 `web_search` 而非 `Web Search`）。部分模型提供者对含空格或特殊字符的名称有问题或直接拒绝；坚持字母数字、下划线、连字符可提升跨提供者兼容性。

### 自定义名称与描述

```python
@tool("web_search")  # 自定义名称
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
```

### 高级 schema：Pydantic / JSON Schema

```python
from pydantic import BaseModel, Field
from typing import Literal
from langchain.tools import tool

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius", description="Temperature unit preference"
    )
    include_forecast: bool = Field(default=False, description="Include 5-day forecast")

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    ...
```

## 访问运行时上下文

```python
from langchain.tools import tool, ToolRuntime

@tool
def summarize(runtime: ToolRuntime) -> str:
    """Summarize the conversation."""
    messages = runtime.state["messages"]
    return f"Conversation length: {len(messages)} messages."
```

## 工具执行

- LangChain：工具由 agent（如 `create_agent`）使用，工具错误处理通过**中间件**配置。
- LangGraph：工具执行由 **`ToolNode`** 处理；工具可访问当前图状态和运行级上下文。

### 返回 Command（更新状态）

工具需要更新图状态时返回 `Command`。针对当前图时，更新中须含一个 `ToolMessage`，其 `tool_call_id` 与当前工具调用匹配。消息历史中每次工具调用都必须有对应 `ToolMessage`；`ToolNode` 强制此要求，缺失则抛 `ValueError`。用 `runtime.tool_call_id` 作为 `tool_call_id` 参数。

```python
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

@tool
def set_language(language: str, runtime: ToolRuntime) -> Command:
    """Set the preferred response language."""
    return Command(
        update={
            "preferred_language": language,
            "messages": [ToolMessage(
                content=f"Language set to {language}.",
                tool_call_id=runtime.tool_call_id,
            )],
        }
    )
```

行为：

- `Command` 用 `update` 更新状态；更新后状态在同一运行后续步骤可用。
- 可能被并行工具调用更新的字段要用 reducer。
- 适用于工具不只返回数据、还改变 agent 状态的场景。

## Headless Tools（无头工具）

模型看到正常工具并可调用，但实际执行发生在服务进程之外。

1. **定义**：`tool(name=..., description=..., args_schema=...)`，仅 schema、无进程内实现。Python 侧只传这三个参数时返回 `HeadlessTool`，**Python 侧无 `.implement()` API**。
2. **注册**：用 `create_agent` 或 LangGraph 图注册，模型可正常调用。
3. **处理中断**：工具被调用时，运行**中断**而非本地执行，产生形如 `{"type":"tool","tool_call":{"id","name","args"}}` 的 payload。
4. **恢复**：你的应用/其他服务/人工步骤执行动作后，用工具结果恢复图。浏览器场景可在前端镜像 schema 并附 `.implement(...)`（JS SDK）。JS SDK hooks 可检测 headless-tool 中断、运行客户端实现、提交恢复命令；可选 `onTool` 回调观察生命周期事件（`start`/`success`/`error`）用于 UI 反馈。

## 创建 Agent 并绑定工具

```python
# pip install -qU langchain "langchain[openai]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

支持 OpenAI、Anthropic、Google 及更多提供者。设置 `LANGSMITH_TRACING=true` 和 API key 即可追踪请求、调试 Agent 行为、评估输出。

## ToolNode（LangGraph）

```python
from langgraph.prebuilt import ToolNode
builder.add_node("tools", ToolNode(tools))
```

`ToolNode` 读取最新 AI 消息的 `tool_calls`，执行匹配函数，把结果包装成模型下轮可读的 tool message。它强制每次工具调用都有对应 `ToolMessage`。

## 版本提示

LangChain v1 对 agent 创建有迁移（`create_react_agent` → `create_agent`）。遇到旧教程 API 对不上时，查官方 v1 迁移指南。

## 框架分层（与 API 的关系）

- **LangChain**（`create_agent`）：高度可定制的 harness，易按场景与数据裁剪。
- **LangGraph**：低层编排框架，适合混合确定性与 Agent 工作流、需要人工审批/持久化/条件分支的场景。
- **Deep Agents**：开箱即用 harness（上下文压缩、虚拟文件系统、子 Agent），基于 LangChain agents。
- **LangSmith**：追踪、调试、评估，框架无关。

工具定义本身在三者间通用——`@tool` / Pydantic schema / ToolNode 是核心原语。
