from __future__ import annotations

from datetime import datetime, timedelta

from pychoam.data.bar import Bar
from pychoam.strategy.sma_crossover import SmaCrossStrategy


def make_bar(ts: datetime, price: float) -> Bar:
    return Bar(ts, price, price, price, price, 0)


def test_sma_crossover_signals() -> None:
    strat = SmaCrossStrategy(fast=3, slow=5, quantity=1)
    start = datetime(2024, 1, 1)
    prices = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]
    signals = []
    for i, p in enumerate(prices):
        bar = make_bar(start + timedelta(minutes=i), p)
        order = strat.on_bar(bar)
        if order:
            signals.append(order.action)
    assert signals == ["BUY", "SELL"]
