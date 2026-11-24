---
description: "Runnable examples of ReAct, function calling, LangChain and CrewAI"
描述: "ReAct、函数调用、LangChain 与 CrewAI 的可运行示例"
name: "Code Examples"
名称: "代码示例"
---

# 06 代码示例

> 说明：示例中的 API Key 需自行申请；模型名称与框架 API 会随时间变化，使用时请对照官方文档调整。离线阅读时重点理解结构，而非逐字照搬。

## 示例 1：ReAct 提示模板（最基础的推理-行动结构）

来自 MeshWorld 的 ReAct 模板，展示"思考→行动→观察→最终答案"的骨架：

```
Question: {user_query}
Thought: I need to find the user's billing history. I will use the SQL tool.
Action: execute_sql
Action Input: SELECT * FROM billing WHERE user_id = 123;
Observation: [后端执行 SQL 并返回结果行]
Thought: I have the billing data. Now I need to summarize it.
Final Answer: The user paid $50 last month.
```

要点：强制模型在输出 Action 前先产出 Thought，把文本当作草稿纸；Observation 由后端真实执行结果填充后再回灌模型。

## 示例 2：Function Calling 最小示例（Anthropic API）

来自 Etuu Technologies 的入门示例——给模型一个工具，它返回结构化调用，由你的代码执行：

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "web_search",
        "description": "Search the web for current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{
        "role": "user",
        "content": "What's the latest news on AI agents?"
    }]
)
print(response.content)
```

实际 Agent 循环会检查响应中的 tool_use 块，执行对应函数，把 tool_result 作为新消息回灌，直到模型给出最终答案。

## 示例 3：LangChain + Gemini + Tavily 研究型 Agent

来自 Reskilll 的完整入门示例。它能：接收研究问题 → 联网搜索 → 分析结果 → 带引用地综合成报告。

前置：

```bash
pip install langchain langchain-google-genai tavily-python
```

需要 Google AI Studio API Key 与 Tavily API Key。

```python
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.tavily_search import TavilySearchResults
from langchain.prompts import PromptTemplate

os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key"

# 初始化模型
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# 给 Agent 一个搜索工具
tools = [TavilySearchResults(max_results=5)]

# 定义 Agent 行为
prompt = PromptTemplate.from_template("""
You are a research agent. Given a question, search for information,
analyze multiple sources, and provide a comprehensive answer with citations.

Question: {input}
{agent_scratchpad}
""")

# 创建并运行
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({
    "input": "What are the latest trends in AI agent development?"
})
print(result["output"])
```

运行时（`verbose=True`）你会看到 Agent 的思维过程：读问题 → 决定搜索 → 构造查询调用 Tavily → 读结果判断是否需要更多信息 → 可能用精炼后的查询再搜 → 综合成答案。这就是 Agentic 行为——AI 根据已学到的信息决定下一步做什么。

改进方向：加更多工具（文件读取、网页抓取、计算器、代码执行）、改进提示词（输出格式、引用风格、分析深度）、加记忆（记住之前的研究）、加反思（返回前自评输出质量）。

## 示例 4：CrewAI 多智能体协作

来自 ThinkCloudly 的示例，展示角色化的多智能体定义方式：

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Researcher",
    goal="Find latest info",
    llm=llm,
    tools=[web_search_tool]
)

task = Task(
    description="Research Artificial Intelligence agents in 2026",
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
print(result)
```

多智能体系统里，不同 LLM Agent 组队：一个研究、一个写作、一个核查事实；可创建一个"老板"Agent 把任务分派给 worker。注意：只有在单个工具齐备的 Agent 被证明不够用之后，才升级到多智能体——它会成倍增加成本、延迟和失败模式。

## 把示例变成真正的 Agent

上面的示例只是起点。原型的差距不在"能不能跑"，而在"能不能被组织依赖"——评估、权限、监控与上线路径。

一个可运行的原型是一个周末的项目；从原型到可靠系统，靠的是工程化。
