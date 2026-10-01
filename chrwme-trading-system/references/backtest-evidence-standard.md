# Backtest Evidence Standard

Read this reference for strategy-performance, exit-policy, walk-forward, or
trade-log requests. It defines the minimum evidence needed before describing a
historical result as reproducible. It does not prescribe a strategy or risk
percentage.

## 1. Freeze the rule version

Record the complete decision chain before measuring performance:

- instrument, direction, setup, confirmation, cancellation, and entry timing;
- stop, target, partial-exit, runner, time-exit, and re-entry rules;
- session boundary, timezone, bar construction, and higher-timeframe alignment;
- position-sizing formula, minimum tradable unit, rounding, and portfolio limits;
- commission, exchange fees, spread, slippage, roll, and market-impact assumptions;
- same-bar event priority when a bar can touch both stop and target.

Execute signals on the next eligible observation unless the rule explicitly
models a realizable order at the current close. Do not use completed daily or
weekly information before that period has closed.

## 2. Label the evidence tier

Keep these data types separate:

1. **Actual contract series** — named exchange contracts with an explicit roll
   schedule and contract specifications.
2. **Continuous or back-adjusted futures series** — useful for research, but the
   adjustment and roll method can change levels, gaps, and simulated fills.
3. **Index, CFD, ETF, or other proxy path** — useful for directional logic only
   when its basis, session, spread, and execution differences are disclosed.

Never splice tiers into one equity curve without a documented normalization and
sensitivity analysis. Report proxy performance as proxy performance, not as the
underlying futures result.

## 3. Separate development and validation

Label each interval as one of:

- **development** — used to invent or tune rules;
- **held-out / walk-forward** — not used to choose the tested parameters;
- **forward test** — signals and fills recorded after the rule version froze.

Nested five- and ten-year windows are not independent samples. Extending a rule
chosen on recent history into older history is informative, but selection bias
remains. Any parameter change starts a new version and a new evidence cycle.

## 4. Report the distribution, not one headline

At minimum report:

- dates, trades, exposure, turnover, and time in market;
- net return, CAGR when meaningful, maximum drawdown, and recovery time;
- gross profit, gross loss, profit factor, average win, average loss, and
  expectancy per trade after costs;
- winning, losing, and breakeven counts plus longest losing sequence;
- best/worst trade and top-one/top-five contribution to net profit;
- annual or regime-level results when the sample is large enough.

Trade-close drawdown computed from realized P&L is not the same as mark-to-market
drawdown. Label it explicitly and prefer a bar-level equity curve when available.
Profit-contribution percentages can exceed 100% when large winners offset losses;
that is a concentration warning, not a calculation error.

## 5. Compare exit policies fairly

Use identical entries, cost models, risk budgets, and data when comparing fixed
targets, partial exits, breakeven moves, or runners. A partial exit can increase
the percentage of profitable trades while reducing average win and right-tail
exposure. Compare return, drawdown, payoff distribution, exposure, turnover, and
tail-profit concentration—not win rate alone.

Whole-contract markets require an explicit rounding rule. State what happens when
the position is too small to sell the desired percentage while retaining a runner.

## 6. Stress and stopping gates

Before advancing from historical research to forward testing:

- increase slippage and fees;
- vary adjacent parameters rather than reporting only the optimum;
- inspect performance without the best trade and the five best trades;
- segment obvious regimes only when each segment has enough observations;
- define a forward-test risk cap and precommitted review/stop conditions.

Stop short of an edge claim when rules changed during the sample, costs or data
provenance are missing, the result depends on a few outliers, or the validation
sample is not independent.

## 7. Deterministic trade-log audit

When a CSV trade log contains a numeric `pnl` column, run:

```bash
python scripts/audit_trade_log.py trades.csv --initial-equity 100000
```

The script uses only the Python standard library. It reports realized trade-level
metrics and does not alter the source file. Read its limitations in the JSON
output; it cannot reconstruct intratrade drawdown from closed-trade rows.

