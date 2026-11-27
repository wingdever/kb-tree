---
description: "QQ official bot Markdown messages with inline keyboard buttons for approvals and choices"
描述: "QQ 官方机器人在 Markdown 消息底部挂内联键盘按钮的交互能力"
name: "QQ Bot Message Buttons"
名称: "QQ 机器人消息按钮"
---

# QQ 机器人消息按钮

QQ 官方机器人没有飞书那种自由布局的交互卡片；可点击的 UI 是 **Markdown 消息底部的内联键盘（keyboard）**，官方称「消息按钮」。正文仍是一条 Markdown 消息，按钮只能挂在最底部，不能嵌进正文、表格或图片里。

## 能力边界

- 场景：单聊、群聊、文字子频道、频道私信都支持发送带 `keyboard` 的消息。
- 形态：按钮是 Markdown 消息的附件，不是独立卡片；一条消息最多 5 行，每行最多 5 个按钮，按钮文字约 10 个字符。
- 动作：`action.type=0` 跳转 URL；`1` 回调后台；`2` 指令按钮，自动在输入框插入 `@bot <data>`。
- 权限：`permission.type=0` 指定用户，`1` 仅管理者，`2` 所有人，`3` 指定身份组（仅频道）。
- 开放范围：FAQ 称单聊、群聊的自定义 Markdown 与消息按钮已对所有机器人开放，无需模板；API 文档仍保留「内邀开通」字样。接入前以管理端配置项与接口实际返回为准。

> 判断：QQ 的消息按钮适合「确认 / 选择 / 跳转」，不适合表单、多选、富文本编辑或任意组件布局。复杂交互应回落到 Web 页面。

## 消息结构

发送时把 `msg_type` 设为 `2`（Markdown），同时带 `markdown` 和 `keyboard`。群聊与单聊都支持这两个字段，只是路径和 openid 不同：群聊用 `group_openid`，单聊用 `user_openid`。

### Keyboard 结构

`keyboard.content.rows` 是按钮行数组；每行一个 `buttons` 数组。每个按钮至少要有：

```json
{
  "id": "allow-once",
  "render_data": {
    "label": "允许一次",
    "visited_label": "已允许",
    "style": 1
  },
  "action": {
    "type": 1,
    "permission": { "type": 2 },
    "data": "approve:once",
    "unsupport_tips": "请升级 QQ 后重试"
  }
}
```

`render_data.style`：`0` 灰色线框，`1` 蓝色线框。`action.unsupport_tips` 是客户端不支持该动作时的提示，必填。

### 按钮动作

| `action.type` | 行为 | 适用 |
|---|---|---|
| `0` | 打开 URL 或小程序 scheme | 「查看详情」「打开 Web 控制台」 |
| `1` | 回调后台，`data` 随互动事件返回 | 审批、选择、确认 |
| `2` | 自动在输入框插入 `@bot <data>` 并发送 | 把按钮变成一条指令 |

> 判断：审批按钮优先用 `type=1` 回调，不要用 `type=2` 指令。指令按钮会把点击变成一条新的用户消息，审批状态容易和原 turn 脱节。

## 回调事件与回应

用户点击 `type=1` 按钮后，平台下发 `INTERACTION_CREATE`：

- `type=11` 表示消息按钮点击；Intent 为 `INTERACTION (1<<26)`。
- 事件里带 `scene`（`c2c` / `group` / `guild`）、`group_openid`、`group_member_openid`、`user_openid`。
- `data.resolved.button_data` 是按钮的 `data`，`button_id` 是按钮 `id`；频道场景另有 `message_id`。

机器人收到后必须调用 `PUT /interactions/{interaction_id}` 回应；不回应客户端会一直 loading 到超时。同一个 `interaction_id` 只能回应一次，超时后失效。

> 判断：回调处理要做三件事——先校验点击者是否是审批发起人，再把 `button_data` 映射回待处理动作，最后只回应一次并落定状态。群聊里不要只靠按钮权限，服务端还要校验 `group_member_openid`。

## 发送窗口与频控

QQ 的消息按钮必须挂在消息上，所以它继承消息的主动/被动规则：

- 被动回复要带 `msg_id`（原消息）或 `event_id`（互动事件）。
- 群聊被动回复：有效 **5 分钟**，同一条消息最多回复 **5 次**。
- 群聊主动消息：每个群每月 **4 条**；群主还要在群里打开「机器人主动在群聊内发言」。
- 单聊被动回复：有效 **60 分钟**；次数在文档更新说明里出现 4 次、规则段写 5 次，接入前按实测为准。
- 单聊主动消息：每个用户每月 **4 条**。
- 消息正文含 URL 时，要提前在管理端「消息 URL 配置」报备，否则可能发送失败。

> 判断：Agent 的长任务里，审批经常在 turn 开始几分钟后才发生。群聊不能假设 5 分钟后还能把卡片挂回原消息；要么在审批发生时立刻发主动消息（消耗每月 4 条配额），要么等用户再发一条消息刷新被动窗口，要么把审批转到单聊/Web。

## 接入 Agent 的映射方式

把平台按钮抽象成中性的待处理交互，不要让 Agent 循环直接理解 `keyboard`：

| 中性字段 | 来源 |
|---|---|
| `interactionId` | 发送时生成的业务 id；回调时与 `interaction_id` 一起做幂等 |
| `kind` | `approval` / `question` / `plan-review` |
| `options` | 按钮的 `id`、`label`、`data` |
| `requester` | 单聊 `user_openid`；群聊 `group_member_openid` |
| `conversation` | `group_openid` 或 `user_openid` |
| `expiresAt` | 群聊 5 分钟、单聊 60 分钟的被动窗口 |

发送侧：审批用 2～3 个按钮（允许一次 / 拒绝 / 查看详情）；选择题最多 5 个按钮；plan review 用「批准 / 拒绝 / 我要修改」，修改意见再让用户发文本。

回调侧：`button_data` 解析成 `approve:once`、`reject`、`edit` 这类稳定值；校验点击者；标记待处理项为已处理；再恢复被挂起的动作。不能用「重新执行整个 turn」来替代审批恢复。

失败侧：按钮发送失败时降级为文本编号选项（`1 允许一次 / 2 拒绝`），并告诉用户直接回复编号。

## 常见失败

| 失败 | 症状 | 修法 |
|---|---|---|
| 没订阅互动事件 | 点击后机器人毫无反应 | 网关 Intent 加上 `1<<26` |
| 没回应互动 | 客户端一直 loading 到超时 | 收到 `type=11` 后立刻 `PUT /interactions/{id}` |
| 重复回应 | 第二次回应被拒绝 | 用 `interaction_id` 做幂等，只回应一次 |
| 群聊审批太晚 | 5 分钟被动窗口已过，卡片发不出去 | 立刻发主动消息，或等用户新消息，或转 Web |
| 群聊配额用完 | 主动消息发送失败 | 审批尽量走被动回复；主动消息留给关键事件 |
| URL 未报备 | 带链接的消息发送失败 | 提前在管理端配置消息 URL |
| 非 Markdown 消息挂按钮 | 按钮不显示或被忽略 | `msg_type=2`，同时带 `markdown` |
| 非审批人点击 | 群里任何人也能点 | 服务端校验 `group_member_openid` / `user_openid` |

## 一句话主线

**QQ 消息按钮是 Markdown 底部的内联键盘，适合审批与选择；真正的难点不是画按钮，而是回调只回应一次、群聊 5 分钟窗口和点击者校验。**

## 参考资料

- QQ 机器人开放平台《消息按钮》（2026-07-21）：https://bot.q.qq.com/wiki/develop/api-v2/server-inter/message/trans/msg-btn.html
- QQ 机器人开放平台《互动事件》（2026-07-23）：https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/interaction_create.html
- QQ 机器人开放平台《发送消息》（2026-06-23）：https://bot.qq.com/wiki/develop/api-v2/server-inter/message/send-receive/send.html
- QQ 机器人开放平台《发送单聊消息》（2026-11-17）：https://bot.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_openid_messages.post.html
- QQ 机器人开放平台《QQ Bot 常见问题答疑》（2026-11-11）：https://bot.q.qq.com/wiki/bot_FAQ/
- QQ 机器人开放平台《基础消息对话》（2026-05-20）：https://bot.qq.com/wiki/develop/api-v2/client-func/intro/baseinfo.html
