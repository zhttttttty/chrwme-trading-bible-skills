# Composition Patterns

Use these patterns only after classifying the request in the parent `SKILL.md`.
They are routing defaults, not mandatory checklists for every question.

## Full technical scenario review

Typical request: "Here are several timeframes. Is this setup actionable?"

1. `top-down-analysis-funnel`
2. `structure-state-classifier`
3. `liquidity-sweep-router` when a liquidity event exists
4. `pd-array-quality-filter` when an entry zone is proposed
5. the applicable scenario module, if any
6. `invalidation-risk-sizing` only after the thesis can be invalidated

Stop at the first unresolved prerequisite. Do not fabricate later-stage parameters.

## PDH/PDL reclaim or rejection

1. `dynamic-working-range` — decide whether the old range remains relevant.
2. `liquidity-sweep-router` — classify the boundary event.
3. `structure-state-classifier` — check displacement and a relevant swing.
4. `pdh-pdl-reversal-executor` — evaluate the complete reversal chain.
5. `invalidation-risk-sizing` — calculate inputs only if the chain passes.

Acceptance outside the boundary routes toward range migration or continuation;
it does not automatically create a polarity flip.

## OB, FVG, or Breaker question

Use `pd-array-quality-filter` first. Add `structure-state-classifier` when the
zone's structural consequence is disputed. Add `invalidation-risk-sizing` only
if the user asks for a plan and provides the required instrument/account inputs.

Do not load liquidity or PDH/PDL modules merely because a chart contains highs
and lows; require a relevant liquidity-event question.

## Wyckoff range question

1. `wyckoff-range-classifier` — classify the initial event chain.
2. `wyckoff-phase-router` — add only if the question concerns a later range and
   whether Markup/Markdown was already established.

Do not force a Spring or UTAD. Do not use the five-stage module as a substitute
for Wyckoff event-chain classification.

## Chrwme five-stage model

Use `five-stage-market-cycle` for the author's bullish/bearish cycle. Add
`structure-state-classifier` only when stage advancement depends on a disputed
MSS/BOS. Add `top-down-analysis-funnel` when premium/discount context or analysis
horizon is missing.

## Position-size request

Use `invalidation-risk-sizing`. If the invalidation is not structurally defined,
load the relevant structure or setup module first. Never select the user's risk
percentage. Stop numerical sizing when point value, multiplier, fees, or slippage
are missing.

## Strategy-performance request

Use `expectancy-evidence-loop`. Add `invalidation-risk-sizing` only when the user
is defining a repeatable risk model. A chart classification module is unnecessary
unless the strategy's setup definition itself is under review.

For a Nasdaq-futures PDL-reversal study or a partial-exit comparison, also read
[`nasdaq-futures-pdl-case-study.md`](nasdaq-futures-pdl-case-study.md). Reuse its
reporting and evidence-separation method, not its numerical parameters as
defaults. Keep actual futures, continuous futures, and proxy price paths in
separate result tables. When comparing all-in/all-out with scaled exits, report
drawdown and tail-profit concentration alongside return and win rate.

## Minimal-answer rule

For a narrow question, use one primary module and answer directly. Mention other
modules only when their missing prerequisite changes the conclusion.
