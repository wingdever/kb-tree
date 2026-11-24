---
description: "End-to-end agent loop, parallel calls, streaming and tool design"
描述: "端到端 Agent 循环、并行组合、流式聚合与工具设计"
name: "End-to-End Loop and Tool Design"
名称: "端到端循环与工具设计"
---

# 07 端到端 Agent 循环与工具设计

这份把前面各厂商规范串成一份可照抄的"生产形状"参考：从工具声明到循环终止、并行/组合调用、流式聚合、错误自愈、工具设计原则。

## 一、工具声明的形状（三种厂商写法对照）

同样是"查天气"工具，三种写法：

**OpenAI / Anthropic 风格（JSON Schema 直接写）：**

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {"type": "string", "description": "City name"}
    },
    "required": ["location"],
    "additionalProperties": false
  }
}
```

（Anthropic 把 `parameters` 换成 `input_schema`。）

**Gemini 风格（OpenAPI Schema）：**

```python
types.FunctionDeclaration(
    name="get_weather",
    description="Get current weather for a city",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={"location": types.Schema(type=types.Type.STRING)},
    ),
)
```

**LangChain 风格（Python 函数 + 装饰器）：**

```python
@tool
def get_weather(location: str) -> str:
    """Get current weather for a city."""
    ...
```

## 二、通用 Agent 循环（生产形状）

```python
def run_agent(prompt, model, tools, tool_functions, max_iterations=5):
    messages = [{"role": "user", "content": prompt}]
    for _ in range(max_iterations):
        resp = model.generate(messages, tools=tools)
        calls = resp.tool_calls or []
        if not calls:                       # 终止条件：无工具调用
            return resp.text

        for call in calls:
            fn = tool_functions.get(call.name)
            try:
                result = fn(**call.args) if fn else f"unknown tool: {call.name}"
            except Exception as e:
                result = f"Error: {e}"      # 错误回灌，让模型自我纠正
            messages.append(assistant_tool_call_msg(call))
            messages.append(tool_result_msg(call.id, result))
    return resp.text                        # 到达上限，优雅降级
```

**三条不可妥协的性质：**

1. **终止**：无工具调用时结束；必须封顶迭代（`max_iterations`），否则卡住的 Agent 永远烧 token。生产部署显式设 `recursion_limit` 并监控触限事件。
2. **并行**：模型可一轮请求多个独立函数；并发执行，按 call id 映射结果。
3. **组合**：依赖工具链式调用（先定位再查询），每轮往返 = 一次模型调用 + 你的执行。

## 三、并行调用

- 一轮响应含多个 tool_use / tool_calls block → 全部执行。
- OpenAI：结果用多条 `{"role":"tool","tool_call_id":...}` 消息回灌。
- Anthropic：所有 `tool_result` block 放进**同一条 user 消息**的 content 数组。
- Gemini：`FunctionResponse` parts 顺序必须与 `functionCall` parts **完全一致**，`name` 一一对应（位置顺序规则适用于所有版本）。
- 用 call id 正确匹配——并行结果可以乱序执行完成，但必须按 id 归位。

## 四、流式工具调用：先聚合再执行

流式时参数分片到达：

- OpenAI：设 `stream: true`，读 `delta.tool_calls`，聚合 delta 成完整 `tool_calls` 再执行。
- Gemini：`stream_function_call_arguments: true`，读 `step.delta` 增量参数，聚合后执行。

**经典 bug**：未重建完整参数就执行，导致参数残缺。务必先把所有分片拼接、校验 JSON 完整，再调用工具。

## 五、错误自愈

- 工具失败是常态，循环必须能捕获失败、把**干净的错误**回灌、让模型重试或换路，而非让整个系统崩溃。
- 用模型能推理的错误信息（"未找到该 ID 的客户"），不要回传原始堆栈。
- 推理模型/带 thinking 的模型：响应中的 reasoning items 或 `thought_signature` 必须随工具结果一起回传，否则多步工具使用丢上下文。
- 每个工具调用必须有对应结果（id 关联）；缺 result 时有些框架（如 ToolNode）直接报错。

## 六、工具设计 ACI 清单

| 原则 | 做法 |
|---|---|
| **少而精** | 给 3~5 个工具，不要 20 个；重叠工具让模型选错 |
| **名字规范** | snake_case，字母数字/下划线/连字符，≤64 字符 |
| **描述三要素** | 做什么、何时用/不用、返回什么 |
| **参数 schema** | 每参数有 type + description；必填列 required；枚举用 enum |
| **严格模式** | 需要确定性时开 strict：`additionalProperties:false`、全字段 required、可选加 null |
| **输入校验** | schema 校验 + 范围检查 + 清洗，绝不直传破坏性操作 |
| **可推理错误** | 返回可操作反馈（MCP `isError:true`），支持模型自我纠正 |
| **危险动作门禁** | 转账/删除/对外发送需显式确认或人工审批（elicitation / interrupt） |
| **格式贴近自然** | 避免精确行数统计、字符串转义；给模型思考 token |
| **防错** | 改参数设计让错误更难发生（如强制绝对路径） |
| **最小权限** | 短期窄 scope 凭据，密钥不进提示词；打破致命三要素 |

## 七、控制模式速查

| 场景 | OpenAI | Anthropic | Gemini |
|---|---|---|---|
| 自行决定 | `"auto"` | `{"type":"auto"}` | `AUTO` |
| 禁止调用 | `"none"` | 不传 tools | `NONE` |
| 必须调用 | `"required"` | `{"type":"any"}` | `ANY` |
| 指定函数 | `{"type":"function","name":...}` | `{"type":"tool","name":...}` | `ANY`+`allowed_function_names` |
| 严格 schema | `strict: true` | `strict: true` | `validated` |

## 八、MCP 工具调用的额外规范

- 发现：`tools/list`（支持分页、缓存；`nextCursor`、`ttlMs`、`cacheScope`）。
- 调用：`tools/call`，参数在 `params.arguments`。
- 结果：`content`（多类型项）+ `structuredContent`（符合 outputSchema）+ `isError`。
- 错误分两层：协议错误用 JSON-RPC error（模型难修复）；执行错误用 `isError:true`（模型可自我纠正）。
- 需要补充输入时返回 `resultType:"input_required"` + `inputRequests`（elicitation），重试时换新 JSON-RPC id。
- 工具注解视为不可信，除非来自可信 server。

## 九、常见坑（上线前对照）

- [ ] 忘了封顶迭代 → 卡住 Agent 烧光预算
- [ ] 流式参数未聚合就执行 → 参数残缺
- [ ] 工具调用无对应结果 → 框架报错 / 模型困惑
- [ ] 回传错误用原始堆栈 → 模型无法自愈
- [ ] 推理模型的 thought_signature / reasoning items 未回传 → 多步上下文丢失
- [ ] Gemini 并行结果顺序错乱 → 结果错配
- [ ] 工具太多/太重叠 → 选错工具、错误率上升
- [ ] 描述模糊 → 参数模糊
- [ ] 危险动作无门禁 → 不可逆损失
- [ ] 把工具返回数据当可信 → 提示注入 / 数据外泄

## 十、一句话总结

> 工具调用的本质是"模型声明意图、你执行、结果回灌"的循环。可靠性不来自更聪明的提示词，而来自：精确的工具声明、严格的 schema、封顶的循环、干净的错误自愈、确定性的护栏，以及对并行/流式/多轮细节的正确处理。
