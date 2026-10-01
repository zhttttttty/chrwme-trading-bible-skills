from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from audit_trade_log import read_pnls, summarize


class AuditTradeLogTests(unittest.TestCase):
    def test_summary_and_trade_close_drawdown(self) -> None:
        result = summarize([100, -50, -25, 0, 200], initial_equity=1000)
        self.assertEqual(result["trades"], 5)
        self.assertEqual(result["winning_trades"], 2)
        self.assertEqual(result["losing_trades"], 2)
        self.assertEqual(result["breakeven_trades"], 1)
        self.assertEqual(result["longest_consecutive_losses"], 2)
        self.assertAlmostEqual(result["net_profit"], 225)
        self.assertAlmostEqual(result["profit_factor"], 4)
        self.assertAlmostEqual(result["expectancy_per_trade"], 45)
        self.assertAlmostEqual(result["ending_equity"], 1225)
        self.assertAlmostEqual(result["trade_close_max_drawdown_pct"], -6.818182)

    def test_csv_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trades.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["pnl"])
                writer.writeheader()
                writer.writerows([{"pnl": "12.5"}, {"pnl": "-3"}])
            self.assertEqual(read_pnls(path), [12.5, -3.0])

    def test_missing_pnl_column_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trades.csv"
            path.write_text("profit\n10\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required column"):
                read_pnls(path)


if __name__ == "__main__":
    unittest.main()

