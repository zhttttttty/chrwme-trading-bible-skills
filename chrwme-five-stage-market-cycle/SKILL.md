---
name: chrwme-five-stage-market-cycle
description: >-
  当用户想把行情映射到 Chrwme 的五阶段多头或空头模型——盘整、向一侧扩张、高周期溢价/折价区反转、回撤建仓、获取对侧流动性——时使用。用于判断模型走到哪一步及缺失条件，不用于把任意区间突破预测为必然反转，也不要把其中 Accumulation/Distribution 当成 Wyckoff 阶段。Triggers: bullish model, bearish model, market cycle, 多空模型。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第8、9、16章"
  tags: [trading, market-cycle, bullish-model, bearish-model]
  related_skills:
    - slug: chrwme-structure-state-classifier
      relation: depends-on
    - slug: chrwme-wyckoff-range-classifier
      relation: contrasts-with
    - slug: chrwme-pd-array-quality-filter
      relation: composes-with
---

# Chrwme 多空五阶段情景循环

## R — 原文（Reading）

> “Consolidation；Sell-Side Expansion；Market Reversal；Long Position-Building；Model Complete：价格上穿原 Consolidation 高点并获取 Buy-Side Liquidity。”
>
> — 第8章《多头模型》；空头模型在第9章镜像展开

## I — 方法论骨架（Interpretation）

模型从盘整两侧形成流动性开始。多头路径先向下扩张至高周期折价区，随后必须出现多头结构确认，再在回撤中评估多头建立，最后以获取原区间上方流动性描述完成；空头路径完全镜像。阶段是观察状态，不是时间表，也不是看到第一步就推定第五步必然发生。

## A1 — 书中的应用（Past Application）

第8、9章的 image-011 至 image-014 用教学图例展示双向五阶段路径。它们证明作者如何组织价格叙事，但不是已披露的真实交易日志；资料没有给出每阶段的客观阈值、发生频率或统计表现。

## A2 — 触发场景（Future Trigger）

- 用户问当前行情处于作者多头/空头模型的哪一阶段。
- 用户看到区间向一侧扩张，想知道反转模型还缺什么。
- 用户混淆作者模型与 Wyckoff Accumulation/Distribution。

与 `chrwme-wyckoff-range-classifier` 的区别：本 skill 是作者个人的五阶段流动性路径；Wyckoff skill 依据 PS/SC/AR/ST 或 PSY/BC/AR/ST 等供需事件链。与 `chrwme-pdh-pdl-reversal-executor` 的区别：本 skill 是抽象路径；后者把 PDH/PDL 作为具体边界执行。

## E — 可执行步骤（Execution）

1. **确认盘整锚**：标出原区间及双侧流动性；没有可识别盘整时输出“不适用”。
2. **确定扩张方向与位置**：说明价格向哪侧离开、是否到达高周期溢价/折价区；只有扩张不算反转。
3. **检查反转证据**：调用结构分类器确认有意义的反向 Swing 与 Displacement；缺失则模型停留在扩张阶段。
4. **判断回撤和完成**：检查回撤区域是否通过 PD Array 质量门；只有价格最终获取原区间对侧流动性才标记模型完成。
5. **输出阶段图**：列出已完成阶段、当前阶段、下一阶段所需证据和模型失效条件。

## B — 边界（Boundary）

- 作者模型中的 Accumulation/Distribution 是个人标签，不是 Wyckoff 术语。
- 价格到达溢价/折价区不保证反转；必须有结构证据。
- 先前阻力或支撑只能评估为潜在角色反转，不能机械认定已经翻转。
- 阶段阈值主观，资料没有统计验证；应用时要保留“不确定/未完成”状态。

## 相关 skills

- depends-on: `chrwme-structure-state-classifier` — Market Reversal 阶段需要结构确认。
- contrasts-with: `chrwme-wyckoff-range-classifier` — 同名词属于不同体系。
- composes-with: `chrwme-pd-array-quality-filter` — 回撤建仓阶段需要区域筛选。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v04。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
