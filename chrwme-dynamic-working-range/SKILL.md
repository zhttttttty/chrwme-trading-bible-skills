---
name: chrwme-dynamic-working-range
description: >-
  当用户用 PDH/PDL 组织日内 Working Range、Daily Bias，并需判断短暂越界后原区间是否保留，或持续 Acceptance 是否要求区间迁移时使用。输出区间状态与重估条件，不把 PDH/PDL 当成价格必须遵守的固定边界，也不自动把越界认作反转。Triggers: PDH, PDL, working range, daily bias, 前日高低点。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第4、15、16章"
  tags: [trading, pdh, pdl, working-range, daily-bias]
  related_skills:
    - slug: chrwme-top-down-analysis-funnel
      relation: composes-with
    - slug: chrwme-liquidity-sweep-router
      relation: composes-with
    - slug: chrwme-pdh-pdl-reversal-executor
      relation: composes-with
---

# PDH/PDL 动态 Working Range 管理器

## R — 原文（Reading）

> “如果价格短暂突破 PDH 后很快重新回到 PDH 下方，PDH 与 PDL 仍可以作为当天 Working Range；如果价格在 PDH 上方形成持续 Acceptance，则原来的 Range 假设可能失效。”
>
> — 第15章《定义交易区间 / 日内方向》

## I — 方法论骨架（Interpretation）

PDH 与 PDL 是日内工作假设，不是硬边界。短暂越界后拒绝回区间，只说明原区间仍可能有参考价值；明显位移越界并在外侧持续接受，才支持区间失效和重定位。状态应随证据更新：默认区间、扫取后保留、边界外接受、区间迁移，而不是全天固定一个 Bias。

## A1 — 书中的应用（Past Application）

第15、16章的教学情景分别展示：短暂突破 PDH 后回落可暂时保留原区间；明显跌破 PDL 并在反弹中将其当作阻力可支持空头延续；PDH 上方持续 Acceptance 则要求上移 Working Range。图例没有披露真实样本统计。

## A2 — 触发场景（Future Trigger）

- 用户问今天的 PDH/PDL 区间是否仍有效。
- 价格短暂越界后返回，用户想区分 Sweep 与有效扩张。
- 用户需要因 Acceptance 更新 Daily Bias。

与 `chrwme-liquidity-sweep-router` 的区别：本 skill 只管理 PDH/PDL 日内区间状态；Sweep skill 可处理任何显著高低点。与 `chrwme-pdh-pdl-reversal-executor` 的区别：本 skill 先判断区间是否保留；后者只在反转条件齐备时组织执行候选。

## E — 可执行步骤（Execution）

1. **建立基准**：取得 PDH、PDL、当前价和交易时段；数据缺失时只返回所需字段。
2. **分类边界行为**：对每侧标记“未触及 / 短暂越界后返回 / 明显位移并持续接受 / 证据冲突”。
3. **更新区间状态**：短暂越界后返回可暂时保留原区间；外侧持续接受支持区间迁移；证据冲突则保持中性并等待。
4. **输出 Bias 假设**：写明当前 Working Range、潜在流动性目标、使假设失效的行为，以及下一次重估触发点。

## B — 边界（Boundary）

- PDH/PDL 不是保证边界，市场可以在任一侧扩张。
- “持续 Acceptance”未被资料量化；必须按品种、周期和用户规则说明判据，不得假装存在统一 N 根 K 标准。
- 对无明确日切或全天连续流动性结构不同的市场，应先定义何为“前一日”。
- 短暂越界后返回只保留区间假设，不自动产生反向入场。

## 相关 skills

- composes-with: `chrwme-top-down-analysis-funnel` — 日内区间仍需服从更高周期背景。
- composes-with: `chrwme-liquidity-sweep-router` — 边界越界属于流动性事件的一种。
- composes-with: `chrwme-pdh-pdl-reversal-executor` — 本 skill 的区间状态是反转执行器的输入。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v06。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
