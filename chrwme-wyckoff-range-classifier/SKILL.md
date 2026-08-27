---
name: chrwme-wyckoff-range-classifier
description: >-
  当用户需要根据前置趋势与供需事件链区分 Wyckoff Accumulation 和 Distribution，或判断没有 Spring/UTAD 的区间是否仍可能成立时使用。分别核对 PS/SC/AR/ST/SOS/LPS 与 PSY/BC/AR/ST/SOW/LPSY，不要求每个可选事件齐全。不适用于把吸筹图式换名后直接套到派发，也不处理 Reaccumulation/Redistribution 的位置分流。Triggers: Wyckoff, accumulation, distribution, Spring, UTAD。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第11、12章"
  tags: [trading, wyckoff, accumulation, distribution, range]
  related_skills:
    - slug: chrwme-five-stage-market-cycle
      relation: contrasts-with
    - slug: chrwme-wyckoff-phase-router
      relation: composes-with
---

# Wyckoff 吸筹/派发事件链识别器

## R — 原文（Reading）

> “Spring 并不是必需事件，合法的 Accumulation 也可以没有 Spring。”
>
> “UTAD 可以看作 Distribution 侧与 Spring 对应的结构，但不是所有 Distribution 都必须出现 UTAD。”
>
> — 第11、12章

## I — 方法论骨架（Interpretation）

先用前置趋势确定要验证的供需问题：下跌后的区间观察供给是否被吸收并转向 Markup；上涨后的区间观察供给是否压过需求并转向 Markdown。事件应按功能而非图形记忆：高潮建立边界，测试观察供需变化，SOS/SOW 与 LPS/LPSY提供离开区间的证据。Spring、UT、UTAD 属于可选变体，缺失不自动否定分类。

## A1 — 书中的应用（Past Application）

第11章 image-019 和第12章 image-023 分别给出吸筹与派发教学图式。技术校订版修正了原资料把吸筹内容复制到派发章节的问题；这些图式不是作者披露的真实成交记录，也没有独立成交量统计或样本外验证。

## A2 — 触发场景（Future Trigger）

- 用户要判断一个交易区间更像吸筹还是派发。
- 区间没有 Spring 或 UTAD，用户担心图式“不完整”。
- 用户混用了 PS/SC 与 PSY/BC 等两套事件标签。

与 `chrwme-five-stage-market-cycle` 的区别：作者五阶段模型使用同名 Accumulation/Distribution 作为个人标签；本 skill 严格使用 Wyckoff 供需事件。与 `chrwme-wyckoff-phase-router` 的区别：本 skill 分类初始区间；后者判断区间后半程还是新的再积累/再派发。

## E — 可执行步骤（Execution）

1. **确定前置趋势**：下跌后才优先验证吸筹，上涨后才优先验证派发；没有前置趋势时保持未分类。
2. **建立区间边界**：用 SC/BC 与 AR 等事件说明上下边界；无法说明边界来源时降低置信度。
3. **核对功能证据**：吸筹检查供给减弱、SOS、LPS/BU；派发检查需求减弱、SOW、LPSY。
4. **处理可选事件**：Spring、UT、UTAD、Retest 缺失时不扣成失败，只记录为未观察到。
5. **输出分类**：给出吸筹/派发/未定、支持事件、反对证据、缺失证据和会使分类失效的行为。

## B — 边界（Boundary）

- 不能把 Accumulation 的 PS/SC/AR/ST 原样复制为 Distribution。
- 不要求每个区间逐项重演教科书示意图。
- 缺少成交量或供需代理数据时，事件判别更依赖主观价格行为，必须降低置信度。
- 分类描述结构，不保证随后一定 Markup 或 Markdown。

## 相关 skills

- contrasts-with: `chrwme-five-stage-market-cycle` — 两者同名词含义不同。
- composes-with: `chrwme-wyckoff-phase-router` — 初始区间分类后再判断后半程与中继区间。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v08。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
