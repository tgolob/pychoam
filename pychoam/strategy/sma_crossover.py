from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional

import numpy as np

from ..data.bar import Bar
from ..engine.event_loop import Order


@dataclass
class SmaCrossStrategy:
    """Simple moving-average cross strategy."""

    fast: int = 5
    slow: int = 60
    quantity: int = 1

    def __post_init__(self) -> None:
        self._prices: Deque[float] = deque(maxlen=self.slow)
        self._prev_diff: float = 0.0

    def on_bar(self, bar: Bar) -> Optional[Order]:
        self._prices.append(bar.c)
        if len(self._prices) < self.slow:
            return None
        arr = np.array(self._prices, dtype=float)
        fast_ma = arr[-self.fast :].mean()
        slow_ma = arr.mean()
        diff = fast_ma - slow_ma
        signal: Optional[Order] = None
        if self._prev_diff <= 0 < diff:
            signal = Order("BUY", self.quantity)
        elif self._prev_diff >= 0 > diff:
            signal = Order("SELL", self.quantity)
        self._prev_diff = diff
        return signal


__all__ = ["SmaCrossStrategy"]
