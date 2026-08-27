---
name: chrwme-pdh-pdl-reversal-executor
description: >-
  当价格先扫过 PDL 后强势收复，或扫过 PDH 后明显跌回，用户要核对 Chrwme 的对称反转模型是否具备结构、回撤区域和风险条件时使用。只有 Sweep、边界收复/拒绝、同向 Displacement/MSS 与有效回撤候选依次成立才进入计划。不适用于仅因触碰或扫取就逆向交易。Triggers: PDL reversal, PDH reversal, 昨低反转, 昨高反转。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第3、15、16、17章"
  tags: [trading, pdh, pdl, reversal, execution]
  related_skills:
    - slug: chrwme-dynamic-working-range
      relation: depends-on
    - slug: chrwme-liquidity-sweep-router
      relation: depends-on
    - slug: chrwme-structure-state-classifier
      relation: depends-on
    - slug: chrwme-invalidation-risk-sizing
      relation: composes-with
---

# PDH/PDL 对称反转执行器

## R — 原文（Reading）

> “价格先跌破 PDL、获取 Sell-Side Liquidity，随后以较强 Bullish Price Delivery 重新站回 PDL 上方。如果之后出现 Bullish Displacement / MSS，并出现有效回撤入场区域，则结构确认更强。”
>
> — 第16章《我的交易模型》；PDH Reversal 为镜像情景

## I — 方法论骨架（Interpretation）

模型是严格的事件链，不是位置交易。PDL 多头情景要求先扫下方流动性，再有力收复 PDL，随后出现多头位移/MSS，并在有效回撤区域定义失效与风险；PDH 空头情景完全镜像。任一步缺失都不得由后面的标签倒推补齐，目标也只是待验证的流动性 Objective，不是必达价位。

## A1 — 书中的应用（Past Application）

第16章用 PDL 与 PDH 两组教学图展示对称反转路径，并说明作者把整体框架视为主要模型。原文曾对两个子模型各写一次“99% of the time”，技术校订版已合并解释；这仍是作者自述，不是胜率或频率统计。

## A2 — 触发场景（Future Trigger）

- 用户描述“跌破昨低又收回”或“突破昨高又跌回”。
- 用户要检查反转模型目前完成了哪几道门。
- 用户已有边界、结构和区域，想形成带失效点的候选计划。

与 `chrwme-dynamic-working-range` 的区别：区间 skill 判断 PDH/PDL 假设是否有效；本 skill 只处理确认后的反转链。与 `chrwme-liquidity-sweep-router` 的区别：后者是通用事件路由，不负责具体 PDH/PDL 执行条件。

## E — 可执行步骤（Execution）

1. **验证边界事件**：确认先发生 PDL 下扫后收复，或 PDH 上扫后跌回；只有触碰、未收复或外侧持续接受时停止。
2. **验证结构确认**：要求同向 Displacement 和相关 Swing 的 MSS/CHoCH；只有微型影线时输出“未确认”。
3. **筛选回撤区域**：用 PD Array 质量门检查候选区域；没有合格区域时等待，不追价。
4. **定义风险计划**：调用失效点仓位 skill 给出 Thesis 失效位置、止损距离、最大允许风险和仓位输入；数据不足时不计算。
5. **输出候选而非承诺**：列出方向假设、证据链、目标候选、失效条件和未满足项，并明确交易教育性质。

## B — 边界（Boundary）

- Sweep、收复或回落任何一个单独事件都不足以触发完整模型。
- 边界外持续 Acceptance 更可能要求区间迁移，而不是反向套模型。
- 重大消息、跳空、极低流动性会使“强势收复”和位移难以比较。
- 资料没有客观定义“强势”，也没有提供胜率；用户必须用自己的品种和周期回测。

## 相关 skills

- depends-on: `chrwme-dynamic-working-range`, `chrwme-liquidity-sweep-router`, `chrwme-structure-state-classifier`。
- composes-with: `chrwme-invalidation-risk-sizing` — 条件成立后再约束损失和仓位。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v07。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
