---
description: "OpenAI's post-2025 structure: OpenAI Foundation controlling OpenAI Group PBC, the OpenAI OpCo contracting entity, and why mainland China has no local counterparty"
描述: "OpenAI 重组后的主体结构：基金会控制 OpenAI Group PBC、签约主体 OpenAI OpCo，以及中国大陆为何没有本地合同相对方"
name: "OpenAI"
名称: "OpenAI（OpenAI Group PBC）"
---

# OpenAI（OpenAI Group PBC）

OpenAI 不是一个普通的科技公司，而是"非营利基金会控制营利性公益公司"的双层结构。2025 年 10 月 28 日完成重组后，原来那家非营利组织改名为 OpenAI Foundation，营利的有限责任公司转成公益公司 OpenAI Group PBC，基金会继续控制它并持有股权。

## 主体结构

| 层 | 主体 | 作用 |
|---|---|---|
| 控制方 | OpenAI Foundation（原非营利组织） | 持有 OpenAI Group 股权，任命与控制其董事会，使命与营利实体一致 |
| 经营主体 | OpenAI Group PBC | 公益公司（Public Benefit Corporation），董事需兼顾使命与股东利益 |
| 历史形态 | 2015 年非营利起步，2019 年设营利性子公司（LLC） | 重组前的"非营利 + 上限利润"安排已废止 |

重组的意义在于：营利实体可以按普通股权融资，不再受"投资回报上限"约束；控制权仍留在基金会手里，避免被纯资本逻辑接管。代价是治理结构更复杂，公开信息里"公司"这个词可能指基金会，也可能指 PBC。

## 签约主体

OpenAI 的服务协议把签约方写得很清楚：

- 位于欧洲经济区与瑞士之外的客户，签约主体是 **OpenAI OpCo, LLC**（特拉华州公司，旧金山）。
- 位于欧洲经济区与瑞士的客户，签约主体是 **OpenAI Ireland Ltd**。
- 政府与公共部门客户，可能指定 **OpenAI Public Sector, LLC**。

个人使用 ChatGPT 的条款同样指向 OpenAI OpCo, LLC。也就是说，中国客户即便能用上服务，合同相对方也是美国实体，不是任何境内公司。

## 中国大陆的实际状态

- **不提供服务**：OpenAI 未在中国大陆开放注册与服务，官网与 API 对大陆网络环境不可用。
- **无境内法人**：没有注册运营公司、没有 ICP 备案，因此不存在境内开票、境内投诉与监管对接主体。
- **数据在境外**：账号、对话与 API 请求由美国实体处理，受美国法律与 OpenAI 条款约束。
- **付款路径**：以美元计价，通过国际信用卡或境外对公账户结算；境内主体付款涉及外汇与合规判断。
- **第三方转售不等于官方**：市面上"OpenAI 代理"多为二次封装或转售，合同相对方是那家代理，不是 OpenAI。

## 产品与主体的对应

- **ChatGPT 个人版**：由 OpenAI OpCo, LLC 提供服务，订阅与账单在 OpenAI 侧。
- **API 与 ChatGPT Enterprise / Business**：走商业服务协议，签约方按客户所在地确定（OpCo 或 Ireland Ltd）。
- **Azure 上的 OpenAI 模型**：由微软的云服务转售，合同与计费在微软或其运营方，不在 OpenAI。
- **开源权重与论文**：以开放许可发布，使用者与 OpenAI 之间不构成服务合同关系。
- **面向企业的定制与优先访问**：通常通过 OpenAI 自身的商业团队或指定合作伙伴签署。

## 对合作方的含义

- **没有境内相对方**：需要境内发票、境内数据合规承诺的项目，OpenAI 官方路径走不通。
- **合同与付款分离**：订阅由 OpCo 收款，代理转售则由代理收款，出问题时先看合同相对方是谁。
- **数据合规**：涉及个人信息出境，使用前要评估申报义务，不能因为"服务在境外"就默认可行。
- **可用性风险**：服务在中国大陆不可用属长期状态，不是临时故障，业务连续性方案要预设替代模型。
- **品牌与实体**：合同里写"OpenAI"不构成有效主体，须写 OpenAI OpCo, LLC 或对应实体全称。

## 怎么核实

1. 读服务协议里的 "OpenAI Contracting Party" 定义，按客户所在地对号入座。
2. 看账单页收款方名称，个人订阅与 API 账单都指向具体法人。
3. 查 OpenAI 官方结构说明页，确认当前是基金会 + PBC 双层，而不是旧的非营利 + LLC。
4. 采购时要求供应商说明它是官方直签、云厂商转售还是第三方代理。

## 常见误区

- **把非营利当成签约方**：基金会是控制方，日常服务合同在 OpCo 等经营实体。
- **以为重组后变成普通公司**：仍是公益公司，董事义务包含使命，不等同于普通股份有限公司。
- **把 Azure OpenAI 当成 OpenAI 直签**：那是微软云的转售，计费与责任在云服务商。
- **以为"能访问就能合规使用"**：网络可达不等于服务可用，也不等于数据出境合规。
- **忽略代理层级**：第三方代理的合同相对方是代理公司，OpenAI 不承担其履约责任。

## 一句话主线

OpenAI 是"基金会控制公益公司"的双层结构，服务合同落在 OpenAI OpCo 等经营实体上：**谈合作看签约实体，谈治理看基金会，谈中国业务则要看有没有本地相对方——目前没有**。

## 参考资料

- OpenAI 官方组织架构说明（2025-10-28 重组）：https://openai.com/zh-Hans-CN/our-structure/
- OpenAI Services Agreement（签约主体定义，2026-01-01 生效）：https://openai.com/policies/services-agreement/
- OpenAI 使用条款（个人服务的合同相对方）：https://openai.com/zh-Hans-CN/policies/row-terms-of-use/
- OpenAI 企业版与 API 条款入口：https://openai.com/policies/
