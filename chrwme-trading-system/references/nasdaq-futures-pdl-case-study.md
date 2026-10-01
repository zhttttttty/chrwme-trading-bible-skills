# Nasdaq Futures PDL Reversal Research Case

Use this reference only when a user asks for a quantified Nasdaq-futures example,
partial-exit comparison, or a template for turning the Chrwme event chain into
testable rules. It is an empirical case study, not a canonical Chrwme rule set,
a live signal, or evidence that the same parameters generalize to another market.
Apply the generic [`Backtest Evidence Standard`](backtest-evidence-standard.md)
when reusing or extending this study.

## Research question

Can a long-only PDL sweep-and-reclaim model use a higher-timeframe regime instead
of an EMA trend filter, while keeping the original event-chain logic recognizable?
The tested implementation used weekly context, daily liquidity, a two-hour RTH
confirmation, and 24-hour risk management.

## Frozen rule version

The following values describe the tested version. Do not silently reuse them as
defaults for another user, instrument, or account.

1. **Weekly regime**
   - Turn bullish when the completed weekly close exceeds the highest high of the
     preceding 13 completed weeks.
   - Leave the bullish regime when the completed weekly close is below the lowest
     low of the preceding 8 completed weeks.
   - Use only information available before the entry bar.
2. **Daily liquidity event**
   - During US regular trading hours, the daily low trades below the preceding
     RTH day's low and the daily close finishes back above that prior low.
3. **Confirmation window**
   - For at most five subsequent RTH sessions, wait for a two-hour RTH bar whose
     close exceeds the highs of the preceding three two-hour bars.
   - Require a bullish body at least `0.7 × ATR(14)` of the two-hour RTH series.
   - Cancel the setup if price trades back below the sweep-day low before entry.
4. **Entry and invalidation**
   - Enter on the next chronological 30-minute bar after confirmation.
   - Initial stop: confirmation-bar low minus `0.1 × ATR(14)` of the two-hour
     series. This is a quantified research proxy for structural invalidation.
   - Position size is the largest whole MNQ contract count not exceeding the
     user-specified account-risk cap after estimated round-trip commissions and
     stop slippage. The study tested 1% and 0.5%; neither is a recommendation.
5. **Partial exit and runner**
   - At `+2R`, sell 75% of the initial quantity while retaining at least one
     contract when position size permits.
   - Move the remaining stop to the entry price.
   - Exit the runner after an RTH daily close below the preceding five-day low,
     when the weekly regime turns off, or after 60 trading days.
   - Monitor protective stops across the available 24-hour session.

For ambiguous 30-minute bars, the implementation checked protective stops before
partial targets. Entries and daily/weekly exits occurred on the next available
bar, preventing same-close execution and obvious look-ahead.

## Cost and contract assumptions

- Initial equity: USD 100,000.
- MNQ point value: USD 2 per index point; whole contracts only.
- Commission: USD 1.25 per contract per side.
- Base slippage: 0.5 index point on every fill; stress case: 1.0 point.
- RTH creates setups and confirmations; the full available session manages stops.
- Bid-only proxy data cannot model bid/ask spread dynamics, exchange fees,
  market impact, limit-order queue position, or roll execution exactly.

## Evidence snapshot (research run dated 2026-10-01)

Only the rule specification and aggregate research snapshot are committed here.
Vendor price files and full trade logs are not redistributed, so the figures
below are provenance-labeled observations rather than independently reproducible
repository tests.

### Ten-year proxy path

Period: 2016-10-03 through 2026-09-30. Source: Dukascopy `USATECHIDXUSD`
30-minute bid bars, used as a Nasdaq-100 price-path proxy and sized as MNQ. This
is not a CME NQ/MNQ continuous-futures history.

| Variant | Trades | Total return | CAGR | Max drawdown | Profit factor |
|---|---:|---:|---:|---:|---:|
| 1% risk, 2R sell 75%, runner | 109 | 222.46% | 12.43% | -5.68% | 4.584 |
| 0.5% risk, same exit | 109 | 77.58% | 5.91% | -2.96% | 4.814 |
| 1% risk, 1-point slippage | 109 | 206.55% | 11.86% | -5.42% | 4.446 |
| 1% risk, no partial exit | 100 | 639.35% | 22.16% | -22.25% | 3.251 |

The no-partial version had much greater convex upside but materially larger
drawdown and concentration: its five largest winners supplied 75.61% of net
profit, versus 25.61% for the partial-exit version. Therefore, a partial exit
should be described as a return-distribution choice, not an unconditional
performance improvement.

The bundled trade-log auditor recomputed 109 trades, profit factor 4.584154,
top-five contribution 25.614521%, and -2.878243% **trade-close** drawdown from
the source closed-trade log during the repository update. The bar-level equity
curve drawdown above is -5.68%; the difference demonstrates why realized
trade-close drawdown must not be presented as mark-to-market drawdown. The
vendor data and source trade log are not committed, so this remains a provenance
note rather than an independently executable repository fixture.

### Five-year nested proxy window

For 2021-10-01 through 2026-09-30, the 1% partial-exit version returned 44.10%
with -4.62% maximum drawdown; the no-partial version returned 41.69% with
-16.14% maximum drawdown. This window is nested inside the ten-year sample and
must not be counted as independent confirmation.

### One-year IBKR MNQ cross-check

For approximately 2025-10-01 through 2026-10-01, actual IBKR MNQ continuous
30-minute bars produced 8 trades, 9.94% total return, -6.74% maximum drawdown,
and profit factor 5.065 under the 1% partial-exit rules. The proxy path over the
overlapping year returned 12.82% with -4.16% drawdown. Direction agreed, but the
proxy was more favorable, so do not splice or present the proxy result as actual
futures performance.

IBKR documents that expired-futures data older than two years from expiration is
unavailable, and continuous-futures requests in current TWS/IB Gateway releases
must leave `endDateTime` empty. These constraints prevent reconstructing a true
ten-year intraday CME series from the tested Gateway alone:

- <https://ibkrcampus.com/docs/web-api/v1/endpoints/market-data/unavailable-historical-data>
- <https://ibkrcampus.com/docs/general/changelog>

## Interpretation rules

- The five- and ten-year proxy windows overlap and are not independent samples.
- The rule set was developed using recent data before the ten-year extension;
  longer history reduces, but does not remove, selection bias.
- A partial winner followed by a breakeven runner counts as a profitable trade;
  its reported win rate is not comparable with an all-in/all-out win rate.
- Integer contract sizing creates nonlinear differences between 0.5% and 1%
  risk, especially for small accounts or wide stops.
- Compare exit policies using return, drawdown, payoff distribution, tail-profit
  concentration, exposure, and costs—not win rate alone.
- Treat actual-contract, continuous-contract, and index/CFD-proxy results as
  separate evidence tiers. Never merge them into one performance claim.
- Before live use, freeze a new version, obtain licensed contract data where
  practical, run walk-forward or held-out tests, and forward-test fills and roll
  behavior. A favorable historical case does not prove a durable edge.

## Reuse boundary

Use the generic [`Backtest Evidence Standard`](backtest-evidence-standard.md) for
the reporting template, evidence tiers, validation labels, exit-policy comparison,
and stopping gates. Keep this file focused on the Nasdaq PDL research instance.


