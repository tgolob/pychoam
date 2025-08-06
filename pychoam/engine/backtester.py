from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
from rich.table import Table
from rich.console import Console

from ..logging_cfg import get_logger
from .metrics import cagr, max_drawdown, sharpe


@dataclass
class Trade:
    entry_ts: str
    exit_ts: str
    entry_price: float
    exit_price: float
    qty: int


class Backtester:
    def __init__(self, feed, strategy, settings) -> None:
        self.feed = feed
        self.strategy = strategy
        self.settings = settings
        self.trades: List[Trade] = []
        self.equity: List[float] = []
        self.log = get_logger(__name__)

    async def run(self) -> None:
        cash = 0.0
        position = 0
        entry_price = 0.0
        entry_ts = ""
        async for bar in self.feed:
            if position and self.settings.stop_pct:
                stop = entry_price * (1 - self.settings.stop_pct)
                if bar.c <= stop:
                    cash += (bar.c - entry_price) * position
                    self.trades.append(
                        Trade(entry_ts, str(bar.ts), entry_price, bar.c, position)
                    )
                    self.log.info("stop hit at %.2f", bar.c)
                    position = 0
            order = self.strategy.on_bar(bar)
            if order:
                if order.action == "BUY" and position == 0:
                    position = order.quantity
                    entry_price = bar.c
                    entry_ts = str(bar.ts)
                elif order.action == "SELL" and position:
                    cash += (bar.c - entry_price) * position
                    self.trades.append(
                        Trade(entry_ts, str(bar.ts), entry_price, bar.c, position)
                    )
                    position = 0
            self.equity.append(cash + position * bar.c)
        self._report()

    def _report(self) -> None:
        console = Console()
        returns = (
            np.diff(self.equity)/np.maximum(self.equity[:-1], 1e-9)
            if len(self.equity) > 1
            else np.array([])
        )
        table = Table(title="Performance")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("CAGR", f"{cagr(self.equity):.2%}")
        table.add_row("Sharpe", f"{sharpe(returns):.2f}")
        table.add_row("MaxDD", f"{max_drawdown(self.equity):.2%}")
        console.print(table)
        if self.trades:
            trades_table = Table(title="Trades")
            trades_table.add_column("Entry")
            trades_table.add_column("Exit")
            trades_table.add_column("PnL")
            for t in self.trades:
                pnl = t.qty * (t.exit_price - t.entry_price)
                trades_table.add_row(t.entry_ts, t.exit_ts, f"{pnl:.2f}")
            console.print(trades_table)


__all__ = ["Backtester", "Trade"]
