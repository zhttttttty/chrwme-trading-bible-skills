---
name: chrwme-liquidity-sweep-router
description: >-
  当价格接近或穿越 PDH/PDL、等高等低、时段或 Swing 高低点，用户要判断是流动性扫取、延续还是尚未确认时使用。按“预判—确认—执行”路由，Sweep 本身不等于反转。不适用于从 K 线断言具体机构意图，也不在没有结构确认时直接给逆向交易结论。Triggers: liquidity sweep, stop run, 假突破, 扫流动性。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第3、4、15、16章"
  tags: [trading, liquidity, sweep, confirmation, scenario-routing]
  related_skills:
    - slug: chrwme-structure-state-classifier
      relation: depends-on
    - slug: chrwme-dynamic-working-range
      relation: composes-with
    - slug: chrwme-pdh-pdl-reversal-executor
      relation: composes-with
---

# Liquidity Sweep 预判—确认—执行路由器

## R — 原文（Reading）

> “Sweep 并不保证反转。之后可能出现反转、盘整，也可能继续突破，必须结合高时间周期结构、Displacement、后续价格行为等进行确认。”
>
> — 第4章《流动性》

## I — 方法论骨架（Interpretation）

明显高低点只提供潜在订单聚集位置。价格穿越这些位置后，后续路径至少有反转、盘整和延续三种。这个方法把责任分开：事前标记候选池，事件发生后等待结构和位移，最后才考虑执行。它不要求相信“机构猎杀止损”的单一叙事，也不允许用 Sweep 代替确认。

## A1 — 书中的应用（Past Application）

第16章用 PDL 与 PDH 教学情景展示：价格先穿越前日边界，再重新站回或跌回，随后若出现同向 Displacement/MSS 与有效回撤区域，反转情景才更强。配图是教学示意；资料没有给出真实订单流、成交身份或统计结果。

## A2 — 触发场景（Future Trigger）

- 用户看到价格扫过昨高、昨低、等高等低或时段边界，问是否会反转。
- 用户想区分假突破、盘整和有效突破。
- 用户需要列出 Sweep 之后仍缺哪些确认。

与 `chrwme-dynamic-working-range` 的区别：本 skill 处理任意显著流动性池；后者只管理 PDH/PDL 工作区间是否保留或迁移。与 `chrwme-pdh-pdl-reversal-executor` 的区别：本 skill 负责通用路由；后者处理边界收复后的具体反转条件。

## E — 可执行步骤（Execution）

1. **标记候选池**：列出价格上下最近的显著高低点及其类别；没有明显池时输出“不适用”。
2. **描述事件而非动机**：记录是否仅触及、短暂穿越后返回，或在边界外持续接受；不推断具体参与者意图。
3. **检查确认**：调用结构证据检查 CHoCH/MSS、Displacement、相关 PD Array 与高周期方向。缺任一关键证据时保持“等待/未确认”。
4. **路由情景**：确认反向结构才进入反转候选；边界外持续接受且顺向结构延续则进入延续候选；两者都不足则归为盘整/等待。
5. **交付边界**：输出情景、证据、失效条件和仍需观察的数据，不自动下达买卖指令。

## B — 边界（Boundary）

- 仅凭 K 线不能证明某机构故意推动价格；流动性池是解释框架，不是可验证的参与者身份。
- Sweep 本身不保证反转，也不证明延续。
- 消息脉冲和流动性极差时，穿越与收回可能失真；必须降低结论强度。
- 不能把止损简单移到“更远处”；止损应由交易 Thesis 的结构失效决定。

## 相关 skills

- depends-on: `chrwme-structure-state-classifier` — 反转确认需要结构状态证据。
- composes-with: `chrwme-dynamic-working-range` — PDH/PDL 是常见流动性边界。
- composes-with: `chrwme-pdh-pdl-reversal-executor` — 通用 Sweep 路由可进入具体边界反转模型。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v02。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
