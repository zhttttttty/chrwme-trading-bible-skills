---
name: chrwme-structure-state-classifier
description: >-
  当用户需要区分 CHoCH、MSS、BOS，或判断某次 Swing 突破究竟是首次反向转变、强化确认还是趋势延续时使用。重点检查 Swing 是否相关、是否有明确 Displacement 与有效收盘。不适用于仅凭单根影线预测涨跌，也不替代高周期方向与风险评估。Triggers: CHoCH, MSS, BOS, structure shift, 结构突破。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第2、3、16章"
  tags: [trading, market-structure, choch, mss, bos]
  related_skills:
    - slug: chrwme-liquidity-sweep-router
      relation: composes-with
    - slug: chrwme-pd-array-quality-filter
      relation: composes-with
---

# CHoCH / MSS / BOS 结构状态判别器

## R — 原文（Reading）

> “CHoCH 是市场首次对原有趋势方向形成反向的、具有意义的关键 Swing Point 突破；MSS 更强调确认意义，通常应伴随明显 Displacement；BOS 用于确认趋势延续。”
>
> — 第2章《市场结构》

## I — 方法论骨架（Interpretation）

结构标签不是按“突破了一个高低点”机械分配，而是按突破在原结构中的职责分类：

1. 先找原方向中真正相关的 Swing，不把微型噪声当结构锚。
2. 首次对原结构方向形成有意义的反向破坏，才是 CHoCH 候选。
3. 反向突破若伴随明确位移、实体有效收盘和上下文支持，可提升为 MSS 确认。
4. 新方向已建立后，沿该方向再破相关 Swing，才使用 BOS 表示延续。
5. 标签不预测未来，只描述当前证据完成到哪一步。

## A1 — 书中的应用（Past Application）

第2章的多头与空头教学图例分别展示：形成有意义低点后以位移突破相关 Swing High，或形成有意义高点后跌破相关 Swing Low。图例用于说明分类规则；资料没有提供这些示例的真实成交记录、胜率或样本外结果。

## A2 — 触发场景（Future Trigger）

- 用户问“这算 CHoCH、MSS 还是 BOS？”
- 用户提供结构描述，想判断影线刺穿是否足以改变方向。
- 用户需要把首次反转证据和趋势延续证据分开。

与 `chrwme-liquidity-sweep-router` 的区别：本 skill 分类结构状态；后者判断 Sweep 后应等待、反转还是按延续处理。与 `chrwme-top-down-analysis-funnel` 的区别：本 skill 处理单一分析尺度内的结构证据；后者分配不同周期的职责。

## E — 可执行步骤（Execution）

1. **重建原结构**：列出原方向和最近两个相关 Swing；无法说明 Swing 重要性时，输出“结构锚不足”并停止贴标签。
2. **检查突破质量**：记录突破方向、实体收盘、位移幅度和后续保持情况；只有影线刺穿时标记为“未确认”。
3. **分配状态**：首次反向破坏标为 CHoCH 候选；带位移强化的反向确认标为 MSS；新方向建立后的顺向突破标为 BOS。
4. **输出证据与缺口**：给出标签、支持证据、尚缺证据和会使判断失效的 Swing；不得把标签改写成确定性交易建议。

## B — 边界（Boundary）

- 不把无关小级别 Swing 的影线刺穿直接认作 CHoCH/MSS。
- 不同 SMC/ICT 教学体系对术语使用不统一；输出应同时描述实际结构，不只给缩写。
- “相关 Swing”“明显位移”在资料中没有量化阈值，必须结合品种、周期和用户定义；不能伪造固定数值。
- 技术结构只能组织概率情景，不能证明价格下一步必涨或必跌。

## 相关 skills

- composes-with: `chrwme-liquidity-sweep-router` — Sweep 后由本 skill 提供结构确认。
- composes-with: `chrwme-pd-array-quality-filter` — 结构结果是 PD Array 质量门之一。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v01。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
