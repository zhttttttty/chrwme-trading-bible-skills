---
name: chrwme-trading-system
description: >-
  Route Chrwme/SMC market-analysis requests across 11 internal modules for
  top-down context, structure, liquidity sweeps, PD arrays, five-stage cycles,
  PDH/PDL, Wyckoff, risk sizing, and expectancy. Use for end-to-end trade-plan
  review, ambiguous multi-concept questions, or deciding which framework
  applies. Load only the relevant internal modules. Not for live-price lookup,
  news/fundamental analysis, or profit guarantees.
metadata:
  version: "0.2.0"
  source: "Chrwme Trading Bible Technical Revision"
  architecture: "single skill with routed internal modules"
---

# Chrwme Trading System

This is one installable skill with 11 internal modules. Treat files under
`references/modules/` as private operating modules, not as separately installed
skills. Select and read only the modules needed for the current request.

## Operating invariants

- Separate observable facts, interpretation, and unknowns.
- A liquidity sweep is an event to route, not an automatic reversal.
- OB, FVG, Breaker, PDH, and PDL are contextual candidates, not automatic entries.
- Do not infer a specific institution's intent from candles alone.
- Do not invent timeframe, trading-day boundary, account risk, contract value,
  fees, slippage, or historical performance.
- Teaching charts and routing tests do not prove a statistical edge.
- Give every directional classification an invalidation or downgrade condition.

## Router

### 1. Classify the request

Map the user's request to one or more lanes:

1. **Context** — higher/lower timeframe conflict, bias, or analysis horizon.
2. **Structure** — CHoCH, MSS, BOS, displacement, or swing relevance.
3. **Liquidity event** — sweep, stop run, equal highs/lows, PDH/PDL crossing.
4. **Price zone** — OB, FVG, Breaker, or retracement-zone quality.
5. **Scenario model** — five-stage cycle, PDH/PDL range or reversal, Wyckoff.
6. **Risk** — invalidation, stop distance, position size, or target logic.
7. **Evidence** — expectancy, backtest, forward test, or rule-version update.

### 2. Select the smallest sufficient module set

Read each selected module completely. The YAML block at the top of a module is
descriptive metadata; apply the module's Markdown body inside this parent skill.

| User need | Internal module |
|---|---|
| Multi-timeframe context or conflicting timeframes | [`top-down-analysis-funnel`](references/modules/chrwme-top-down-analysis-funnel.md) |
| CHoCH, MSS, BOS, swing or displacement classification | [`structure-state-classifier`](references/modules/chrwme-structure-state-classifier.md) |
| Sweep versus continuation versus wait | [`liquidity-sweep-router`](references/modules/chrwme-liquidity-sweep-router.md) |
| OB, FVG, Breaker definition and quality | [`pd-array-quality-filter`](references/modules/chrwme-pd-array-quality-filter.md) |
| Chrwme bullish/bearish five-stage model | [`five-stage-market-cycle`](references/modules/chrwme-five-stage-market-cycle.md) |
| PDH/PDL working range, acceptance, or range migration | [`dynamic-working-range`](references/modules/chrwme-dynamic-working-range.md) |
| Complete PDH/PDL reversal condition chain | [`pdh-pdl-reversal-executor`](references/modules/chrwme-pdh-pdl-reversal-executor.md) |
| Initial Wyckoff accumulation/distribution classification | [`wyckoff-range-classifier`](references/modules/chrwme-wyckoff-range-classifier.md) |
| Reaccumulation/redistribution versus initial range | [`wyckoff-phase-router`](references/modules/chrwme-wyckoff-phase-router.md) |
| Invalidation, stop distance, and position-size inputs | [`invalidation-risk-sizing`](references/modules/chrwme-invalidation-risk-sizing.md) |
| Expectancy, backtest, forward test, and evidence updates | [`expectancy-evidence-loop`](references/modules/chrwme-expectancy-evidence-loop.md) |

For a quantified example of translating the PDL event chain into frozen Nasdaq
futures research rules, read
[`nasdaq-futures-pdl-case-study.md`](references/nasdaq-futures-pdl-case-study.md)
only when the user asks about Nasdaq futures, partial exits, or backtest design.
Treat it as a case study rather than an additional canonical module.

Do not load all modules by default. A narrow terminology question usually needs
one module. An end-to-end trade-plan review may need several modules in stages.

### 3. Respect dependencies and order

Use this order when more than one module applies:

```text
Top-down context
  -> structure state
  -> liquidity event and/or PD Array quality
  -> scenario-specific model
  -> invalidation and position sizing
  -> expectancy and evidence review
```

Additional dependency rules:

- Read `dynamic-working-range` before `pdh-pdl-reversal-executor` when range
  validity or migration is unresolved.
- Read `wyckoff-range-classifier` before `wyckoff-phase-router` unless the user
  already established both the initial range and a subsequent trend.
- Keep Chrwme's five-stage Accumulation/Distribution terminology separate from
  Wyckoff Accumulation/Distribution.
- Use `invalidation-risk-sizing` only after a thesis has a defined invalidation.
- Use `expectancy-evidence-loop` for system-level evidence, not to predict the
  next trade from a small sample.

For common multi-module sequences, read
[`composition-patterns.md`](references/composition-patterns.md).

### 4. Execute with gates

At each stage output one of:

- **Confirmed enough to continue** — name the supporting observations.
- **Conditional candidate** — list the next evidence required.
- **Insufficient input** — identify only the missing fields that change the result.
- **Invalidated / wrong module** — stop that branch and route to the relevant one.

Do not let a later module repair a failed earlier gate. For example, an attractive
FVG cannot substitute for missing structure confirmation, and a favorable fixed
R:R cannot justify moving a stop away from the thesis invalidation.

### 5. Synthesize one answer

Do not expose 11 disconnected mini-reports. Produce one ordered response:

1. **Observed facts** — timeframe, levels, swings, closes, displacement, and data supplied.
2. **Modules used** — list the internal modules actually read, in execution order.
3. **Current classification** — include confidence limits; use `undetermined` when needed.
4. **Condition tree** — what confirms, downgrades, or invalidates each live scenario.
5. **Risk inputs** — only when requested or when reviewing an actionable plan.
6. **Evidence status** — distinguish a setup match from a demonstrated strategy edge.

## Stop conditions

Stop before precise execution parameters when any required item is missing:

- the relevant timeframe or trading horizon;
- the swing/level used for structural invalidation;
- a consistent trading-day boundary for PDH/PDL;
- account risk approved by the user;
- contract multiplier, point value, fees, or slippage for position sizing;
- sufficient historical observations for expectancy claims.

State the missing item and continue only with the parts that remain valid.

## Scope boundary

This skill analyzes a supplied technical scenario. It does not fetch live prices,
interpret macro news or company fundamentals, select a user's risk tolerance, or
promise profitability. Route those requests to an appropriate data or research
workflow instead of stretching this framework.
