---
name: chrwme-invalidation-risk-sizing
description: >-
  当用户已有明确交易 Thesis，需要先确定结构失效点，再依据账户净值、止损距离和用户已批准的最大风险计算仓位输入时使用。Stop 必须放在逻辑真正失效处，Target 连接结构、流动性和经测试的退出规则。不适用于替用户选择风险比例、在缺少合约价值/点值时猜测仓位，或为了固定 R:R 扭曲止损。Triggers: position size, invalidation, stop loss, 仓位, 止损, 单笔风险。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第3、16、17章"
  tags: [trading, risk, position-sizing, invalidation, stop-loss]
  related_skills:
    - slug: chrwme-pd-array-quality-filter
      relation: composes-with
    - slug: chrwme-pdh-pdl-reversal-executor
      relation: composes-with
    - slug: chrwme-expectancy-evidence-loop
      relation: composes-with
---

# 结构失效点驱动的仓位与退出框架

## R — 原文（Reading）

> “Position Size 应根据账户净值、结构失效点 / Stop 的距离，以及交易系统允许的最大风险比例计算。Stop 应放在交易 Thesis 真正失效的位置，并考虑市场 Volatility 与交易品种特性。”
>
> — 第17章《风险管理》

## I — 方法论骨架（Interpretation）

顺序不能倒置：先说明交易逻辑为何成立，再找到该逻辑被证明错误的位置，然后由止损距离和用户已有风险上限反推仓位。不能先选固定手数或理想 R 倍数，再移动 Stop 去适配。Target 同样应来自流动性 Objective、结构和经测试的退出规则，而不是为获得漂亮 R:R 随意拉远。

## A1 — 书中的应用（Past Application）

第3、16章的 SMC 检查清单反复把 Invalidation、Stop、Target、Position Size 放在入场前；第17章说明如何用账户净值、失效距离和最大风险连接这些字段。资料没有给出一笔可核验的数值交易或推荐风险百分比，因此本 skill 不补造默认比例。

## A2 — 触发场景（Future Trigger）

- 用户已有入场逻辑和结构图，想确定 Stop 与仓位输入。
- 两个品种止损距离不同，用户想保持相同账户风险。
- 用户为了满足固定 R:R 想移动止损或目标。

与 `chrwme-pd-array-quality-filter` 的区别：区域 skill 判断 Setup 是否值得跟踪；本 skill 只在 Thesis 明确后计算风险输入。与 `chrwme-expectancy-evidence-loop` 的区别：本 skill 管单笔风险；后者评估跨样本系统表现。

## E — 可执行步骤（Execution）

1. **写出 Thesis**：用一句话说明方向假设、触发证据和必须保持的结构；无法表述时停止计算仓位。
2. **确定失效点**：找到价格到达后会否定 Thesis 的结构位置，并说明波动、点差、跳空等执行风险；不得只用任意固定距离。
3. **收集输入**：账户净值、用户已批准的最大货币/比例风险、入场价、止损价、品种点值/合约乘数、费用和滑点。缺字段则列出缺口，不猜值。
4. **计算仓位上限**：允许亏损额除以每单位从入场到 Stop 的总风险；按可交易最小单位向下取整，并复核费用后风险不超限。
5. **检查 Target**：目标须连接流动性、结构或已测试退出逻辑；报告实际 R:R，但不因低于任意阈值自动宣判系统无效。

## B — 边界（Boundary）

- 本 skill 不决定用户应承担多少风险，也不提供个性化投资建议；最大风险必须来自用户或其经测试计划。
- 缺少点值、合约乘数、费用、滑点或跳空风险时，仓位结果不可靠。
- Stop 不能保证按指定价格成交；杠杆、相关持仓和极端行情可能放大损失。
- 结构分析不能让未来价格确定；任何 Setup 都必须允许失败。

## 相关 skills

- composes-with: `chrwme-pd-array-quality-filter`, `chrwme-pdh-pdl-reversal-executor` — 条件通过后再约束风险。
- composes-with: `chrwme-expectancy-evidence-loop` — 单笔规则需要在跨样本中验证。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v10。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
