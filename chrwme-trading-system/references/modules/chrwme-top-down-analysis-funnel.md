---
name: chrwme-top-down-analysis-funnel
description: >-
  当用户需要把月/周级背景、日线/4H 区域和 1H 以下执行分层，或低周期信号与高周期环境冲突时使用。用于形成从方向与位置到确认再到执行的分析漏斗。不适用于只给一个周期、没有交易时域却要求精确入场，也不要求所有周期重复同一信号。Triggers: top-down analysis, multi-timeframe, 多周期分析, HTF/LTF。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第2、3、10章"
  tags: [trading, top-down, multi-timeframe, context]
  related_skills:
    - slug: chrwme-structure-state-classifier
      relation: composes-with
    - slug: chrwme-pd-array-quality-filter
      relation: composes-with
    - slug: chrwme-dynamic-working-range
      relation: composes-with
---

# 多时间周期分析漏斗

## R — 原文（Reading）

> “Monthly and Weekly Charts 用于识别长期趋势以及重要支撑、阻力位置；Daily and 4-Hour Charts 进一步细化分析；1-Hour and Lower Charts 用于寻找精确的 Entry / Exit。”
>
> — 第10章《自上而下分析》

## I — 方法论骨架（Interpretation）

不同周期承担不同职责，而不是互相投票。高周期定义方向、区间和关键位置；中周期把区域缩小并检查结构；低周期只在前两层提供的背景内寻找执行触发。低周期信号若出现在高周期区间中央或逆高周期关键位置，应降低结论强度，而不是用更精细的图表掩盖背景不足。

## A1 — 书中的应用（Past Application）

第10章用月/周、日/4H、1H 以下的连续教学图例展示分析漏斗：先识别大级别趋势和位置，再细化区域，最后寻找执行触发。资料没有给出这些图例对应的真实交易结果或证明固定周期组合优于其他组合。

## A2 — 触发场景（Future Trigger）

- 用户问应先看哪个周期、不同周期冲突怎么办。
- 低周期出现 OB/FVG/MSS，但用户不知道高周期是否支持。
- 用户要把波段背景和日内执行放在同一计划中。

与 `chrwme-structure-state-classifier` 的区别：本 skill 决定在哪个周期回答什么；结构 skill 在选定周期内分类突破。与 `chrwme-dynamic-working-range` 的区别：后者只处理日内 PDH/PDL 边界。

## E — 可执行步骤（Execution）

1. **确定决策时域**：先确认用户持有周期和执行周期；没有时域时先请求，而不是默认日内。
2. **高周期背景层**：记录趋势/区间、关键支撑阻力和当前位置；若位于区间中央，明确标注位置优势不足。
3. **中周期细化层**：检查相关 Swing、结构状态和候选区域；只保留与背景不冲突或有明确反转证据的区域。
4. **低周期执行层**：寻找位移、MSS/CHoCH、回撤区域与失效点；没有触发则输出等待条件。
5. **合并输出**：分别列出背景、区域、触发、失效和周期冲突；不得用低周期精度替代高周期证据。

## B — 边界（Boundary）

- 月/周、日/4H、1H 以下是资料示例，不是所有品种的固定周期配方；应按交易时域等比例调整。
- 历史反应区域不保证未来再次反应，“机构关键位置”也不能仅由图表证明。
- 周期越多不等于证据越强；重复观察同一价格行为不能算独立确认。
- 没有实时或用户提供的数据时，只能给分析流程，不能伪造当前市场结论。

## 相关 skills

- composes-with: `chrwme-structure-state-classifier` — 在各层分类结构状态。
- composes-with: `chrwme-pd-array-quality-filter` — 在中低周期筛选区域。
- composes-with: `chrwme-dynamic-working-range` — 日内层可用 PDH/PDL 组织边界。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v05。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
