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
   - Position size is the largest whole MNQ contract count not exceeding both
     the account-risk cap and a 2.0-times gross-notional leverage cap after
     estimated round-trip commissions and stop slippage.
   - Round fills to the 0.25-point MNQ tick in the adverse direction.
5. **Partial exit and runner**
   - At `+2R`, sell 25% of the initial quantity while retaining at least one
     contract when position size permits.
   - Do not automatically move the remaining stop to entry. After the partial,
     trail below newly confirmed two-hour swing lows with a `0.1 × ATR(14)`
     buffer; never loosen the stop or backdate a swing confirmation.
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

## Evidence snapshot (causal correction dated 2026-10-02)

Only the rule specification and aggregate research snapshot are committed here.
Vendor price files and full trade logs are not redistributed, so the figures
below are provenance-labeled observations rather than independently reproducible
repository tests.

### Superseded result notice

The 2026-10-01 snapshot previously published here was invalid. Its resampling
code labeled a completed two-hour aggregate with the timestamp of its first
30-minute component. The simulator could therefore enter 90 minutes before the
aggregate was observable. In the 109-trade run, 106 entries had this timing
leak. The previously reported 222.46% base return, related five-year variants,
and the one-year IBKR cross-check are withdrawn rather than treated as evidence.
A closed-trade arithmetic audit did not and could not detect this causal error.

### Corrected ten-year proxy path

Period: 2016-10-03 through 2026-09-30. Source: Dukascopy `USATECHIDXUSD`
30-minute bid bars, used as a Nasdaq-100 price-path proxy and sized as MNQ. This
is not a CME NQ/MNQ continuous-futures history.

All variants below use causal two-hour aggregation, discard incomplete RTH tail
windows, round fills to 0.25 point, cap gross entry leverage at 2.0 times, charge
USD 1.25 per contract per side, and apply 0.5 point adverse slippage per fill.

| Exit variant | Trades | Total return | CAGR | Max drawdown | Profit factor |
|---|---:|---:|---:|---:|---:|
| 2R sell 75%, then breakeven | 89 | 30.73% | 2.72% | -6.39% | 1.62 |
| 2R sell 50%, structural trail | 102 | 50.42% | 4.17% | -5.60% | 1.77 |
| 2R sell 25%, structural trail | 102 | 62.55% | 4.98% | -6.42% | 1.89 |

For the 25% partial version, win rate was 42.16%, exposure 15.71%, and maximum
observed gross entry leverage 1.998 times. The bundled closed-trade auditor
recomputed USD 62,548 net profit, 1.885874 profit factor, USD 613.22 expectancy
per trade, seven consecutive losses, and 62.59% of net profit from the five
largest winners. Its -5.03% trade-close drawdown is not the same as the -6.42%
bar-level mark-to-market drawdown.

The 25% result is an in-sample exit-policy comparison, not independent proof that
25% generalizes. Returns were negative in 2022, 2025, and the partial 2026 year.
It requires held-out or forward testing on licensed futures data before any edge
claim.

### Rejected continuation experiment

An optional branch bought a bullish daily breakout of the prior 20-day high only
after a later daily retest held that level and a two-hour displacement confirmed.
It added 19 trades but those trades lost USD 13,698.40 in this sample; the combined
model returned 31.79% with -9.46% drawdown before the final tick-rounding rerun.
The branch is disabled and is not part of the frozen candidate. These figures are
diagnostic only because that branch did not receive the final execution rerun.

IBKR documents that expired-futures data older than two years from expiration is
unavailable, and continuous-futures requests in current TWS/IB Gateway releases
must leave `endDateTime` empty. These constraints prevent reconstructing a true
ten-year intraday CME series from the tested Gateway alone:

- <https://ibkrcampus.com/docs/web-api/v1/endpoints/market-data/unavailable-historical-data>
- <https://ibkrcampus.com/docs/general/changelog>

## Interpretation rules

- The corrected exit variants share the same ten-year development sample and are
  parameter comparisons, not three independent confirmations.
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



