---
name: chrwme-pd-array-quality-filter
description: >-
  当用户标出 Order Block、Fair Value Gap 或 Breaker Block，想判断该区域的机械定义是否成立、上下文质量是否足够时使用。统一检查形成原因、结构结果、高周期方向、流动性目标和失效条件。不适用于“价格碰到区域就进场”或假设所有 FVG 必回补。Triggers: OB, FVG, Breaker, PD Array, 订单块, 公平价值缺口。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第3、5、6、7章"
  tags: [trading, pd-array, order-block, fvg, breaker]
  related_skills:
    - slug: chrwme-structure-state-classifier
      relation: depends-on
    - slug: chrwme-liquidity-sweep-router
      relation: composes-with
    - slug: chrwme-invalidation-risk-sizing
      relation: composes-with
---

# PD Array 上下文质量筛选器

## R — 原文（Reading）

> “识别由该次 Displacement 形成或确认的有效 Order Block / Fair Value Gap / Breaker Block；等待价格回到选定的 PD Array，并确认高时间周期方向与 Liquidity Target 仍保持一致。”
>
> — 第3章《SMC 入场检查清单》

## I — 方法论骨架（Interpretation）

先验证形态，再评价上下文。OB 要有前置反向 K 线和产生结构结果的位移；FVG 要满足三 K 线 Candle 1/3 影线不重叠；Breaker 要先有有效 OB、明确失效、反向位移与从另一侧回测。三者都不能仅靠形状决定质量，还需高周期方向、流动性目标、结构结果和可定义失效点共同支持。

## A1 — 书中的应用（Past Application）

第5至7章分别给出多空 OB、Breaker 和 FVG 教学图例。它们用于说明机械识别和上下文条件；资料没有证明图中区域代表特定机构订单，也没有提供每类形态的真实胜率、样本量或交易成本后收益。

## A2 — 触发场景（Future Trigger）

- 用户问某个区域是否真的算 OB、FVG 或 Breaker。
- 多个区域重叠，用户想比较优先级。
- 用户要知道区域触及后仍缺哪些入场条件。

与 `chrwme-structure-state-classifier` 的区别：本 skill 评价区域；结构 skill 评价 Swing 突破状态。与 `chrwme-invalidation-risk-sizing` 的区别：本 skill 说明区域是否值得跟踪；风险 skill 根据 Thesis 失效点计算可承担仓位。

## E — 可执行步骤（Execution）

1. **机械验证**：按 OB、FVG 或 Breaker 的定义逐项核对；定义不成立即停止。
2. **形成原因检查**：指出产生区域的 Displacement、相关 Swing 结果和前置流动性事件；缺失时降级为低质量候选。
3. **上下文评分**：分别判断高周期方向、明确目标、回测反应和失效条件是否一致；不得用“标签重叠数量”代替证据。
4. **输出结论**：分为“定义不成立 / 定义成立但上下文不足 / 值得等待确认”，并列出下一项确认；不把第三类直接写成买卖信号。

## B — 边界（Boundary）

- OB 不限于全局绝对顶底，但必须产生清晰结构结果。
- 普通突破回测区不是 Breaker；没有前置 OB 失效链时不得套用。
- FVG 不是“完全没有成交的区域”，也不保证部分或完全回补。
- 图表不能独立证明区域背后的机构身份或意图。

## 相关 skills

- depends-on: `chrwme-structure-state-classifier` — 区域质量依赖真实结构结果。
- composes-with: `chrwme-liquidity-sweep-router` — 前置流动性事件可提高候选相关性。
- composes-with: `chrwme-invalidation-risk-sizing` — 通过筛选后仍须用失效点约束风险。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v03。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
