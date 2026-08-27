---
name: chrwme-wyckoff-phase-router
description: >-
  当用户需要区分“同一个初始吸筹/派发区间的后半程”与“趋势已经启动后在新位置形成的 Reaccumulation/Redistribution”时使用。核心门是 Markup/Markdown 是否已经建立，以及当前是否为更高/更低位置的新中继区间。不适用于初始区间尚未分类的场景，也不把 Retest 当成必然步骤。Triggers: reaccumulation, redistribution, 再积累, 再派发, Phase E。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第11至14章"
  tags: [trading, wyckoff, reaccumulation, redistribution, phase-routing]
  related_skills:
    - slug: chrwme-wyckoff-range-classifier
      relation: depends-on
---

# 初始区间完成与再积累/再派发分流器

## R — 原文（Reading）

> “真正的 Reaccumulation 是 Markup 已经开始后，价格在更高位置形成新的 Consolidation / Trading Range，作为原有 Uptrend 的中继。”
>
> — 第13章；Redistribution 在第14章为向下镜像

## I — 方法论骨架（Interpretation）

判断名称的关键不是区间“看起来像第二段”，而是趋势状态与位置是否改变。原始底部吸筹中的 Phase B、可选 Spring/Test、SOS、LPS/BU 仍属于同一个初始区间的完成；只有 Markup 已经建立，随后在更高位置形成新交易区间，才叫 Reaccumulation。顶部派发与 Redistribution 镜像处理。

## A1 — 书中的应用（Past Application）

第13、14章分别用 image-024、image-025 修正原资料的术语错误：原始区间后半程不能直接改名为 Reaccumulation/Redistribution。图例用于说明阶段与位置差异，资料没有给出这些分类的统计预测结果。

## A2 — 触发场景（Future Trigger）

- 用户问当前是原始吸筹后半程还是 Reaccumulation。
- 用户问顶部区间完成是否已经属于 Redistribution。
- 用户需要纠正“第二阶段吸筹/派发”的命名。

本 skill 依赖 `chrwme-wyckoff-range-classifier`：必须先确认初始区间类型。它不替代该 skill 的 PS/SC/AR/ST 或 PSY/BC/AR/ST 事件判别，而只负责趋势已启动前后的阶段分流。

## E — 可执行步骤（Execution）

1. **确认初始区间**：先取得吸筹/派发/未定分类；未定时返回前置任务而不继续命名。
2. **检查趋势是否已建立**：寻找价格已离开初始区间并形成 Markup 或 Markdown 的证据；仍在原边界内则属于初始区间完成过程。
3. **检查新位置与新边界**：Markup 后更高位置的新 TR 才是 Reaccumulation；Markdown 后更低位置的新 TR 才是 Redistribution。
4. **输出分流**：给出“初始区间后半程 / Reaccumulation / Redistribution / 证据不足”，并列出位置、趋势状态和失效条件。

## B — 边界（Boundary）

- 同一原始区间中的后半程不能因为时间推移就改名为再积累/再派发。
- 新区间必须发生在已建立趋势中的不同位置；仅一次回撤或反弹不足以构成 TR。
- Retest、Spring、UTAD 都可能缺失，不得当作必然顺序。
- 该分类不保证原趋势随后一定继续。

## 相关 skills

- depends-on: `chrwme-wyckoff-range-classifier` — 先识别初始吸筹/派发，再进行阶段路由。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v09。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
