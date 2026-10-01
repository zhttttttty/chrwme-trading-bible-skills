#!/usr/bin/env python3
"""Audit a closed-trade CSV without modifying it or requiring third-party packages."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Iterable


def _round(value: float | None, digits: int = 6) -> float | None:
    return None if value is None else round(value, digits)


def read_pnls(path: Path, pnl_column: str = "pnl") -> list[float]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or pnl_column not in reader.fieldnames:
            raise ValueError(f"missing required column: {pnl_column}")
        pnls: list[float] = []
        for line_number, row in enumerate(reader, start=2):
            raw = (row.get(pnl_column) or "").strip()
            try:
                value = float(raw)
            except ValueError as exc:
                raise ValueError(
                    f"non-numeric {pnl_column} at CSV line {line_number}: {raw!r}"
                ) from exc
            if not math.isfinite(value):
                raise ValueError(
                    f"non-finite {pnl_column} at CSV line {line_number}: {raw!r}"
                )
            pnls.append(value)
    if not pnls:
        raise ValueError("trade log contains no rows")
    return pnls


def summarize(pnls: Iterable[float], initial_equity: float | None = None) -> dict:
    values = list(pnls)
    if not values:
        raise ValueError("at least one P&L value is required")
    if initial_equity is not None and initial_equity <= 0:
        raise ValueError("initial equity must be greater than zero")

    wins = [value for value in values if value > 0]
    losses = [value for value in values if value < 0]
    breakeven = len(values) - len(wins) - len(losses)
    gross_profit = sum(wins)
    gross_loss = -sum(losses)
    net_profit = sum(values)

    longest_losses = current_losses = 0
    for value in values:
        if value < 0:
            current_losses += 1
            longest_losses = max(longest_losses, current_losses)
        else:
            current_losses = 0

    best = max(values)
    worst = min(values)
    top_five = sum(sorted(wins, reverse=True)[:5])
    net_share = lambda amount: 100 * amount / net_profit if net_profit > 0 else None

    trade_close_mdd_pct = ending_equity = total_return_pct = None
    if initial_equity is not None:
        equity = initial_equity
        peak = initial_equity
        max_drawdown = 0.0
        for value in values:
            equity += value
            peak = max(peak, equity)
            if peak > 0:
                max_drawdown = min(max_drawdown, equity / peak - 1)
        ending_equity = equity
        total_return_pct = 100 * (equity / initial_equity - 1)
        trade_close_mdd_pct = 100 * max_drawdown

    return {
        "trades": len(values),
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "breakeven_trades": breakeven,
        "win_rate_pct": _round(100 * len(wins) / len(values)),
        "gross_profit": _round(gross_profit),
        "gross_loss": _round(gross_loss),
        "net_profit": _round(net_profit),
        "average_win": _round(gross_profit / len(wins) if wins else None),
        "average_loss": _round(sum(losses) / len(losses) if losses else None),
        "expectancy_per_trade": _round(net_profit / len(values)),
        "profit_factor": _round(gross_profit / gross_loss if gross_loss else None),
        "payoff_ratio": _round(
            (gross_profit / len(wins)) / (gross_loss / len(losses))
            if wins and losses
            else None
        ),
        "longest_consecutive_losses": longest_losses,
        "best_trade": _round(best),
        "worst_trade": _round(worst),
        "best_trade_share_of_net_profit_pct": _round(net_share(best)),
        "top5_winners_share_of_net_profit_pct": _round(net_share(top_five)),
        "initial_equity": _round(initial_equity),
        "ending_equity": _round(ending_equity),
        "total_return_pct": _round(total_return_pct),
        "trade_close_max_drawdown_pct": _round(trade_close_mdd_pct),
        "limitations": [
            "Metrics use closed-trade P&L in CSV row order.",
            "Trade-close drawdown excludes intratrade and open-position excursions.",
            "Profit contribution can exceed 100% when winners offset losses.",
            "The script does not verify signal timing, fees, slippage, or data provenance.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="closed-trade CSV to audit")
    parser.add_argument("--pnl-column", default="pnl")
    parser.add_argument("--initial-equity", type=float)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        pnls = read_pnls(args.csv_path, args.pnl_column)
        result = summarize(pnls, args.initial_equity)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), flush=True)
        return 2
    result["source_file"] = args.csv_path.name
    result["pnl_column"] = args.pnl_column
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
