from __future__ import annotations

import numpy as np


def cagr(equity: list[float], periods_per_year: int = 252) -> float:
    if not equity or equity[0] == 0:
        return 0.0
    years = len(equity) / periods_per_year
    if years == 0:
        return 0.0
    total = equity[-1] / equity[0]
    return total ** (1 / years) - 1


def sharpe(returns: np.ndarray, risk_free: float = 0.0, periods_per_year: int = 252) -> float:
    if returns.size == 0:
        return 0.0
    excess = returns - risk_free / periods_per_year
    if excess.std() == 0:
        return 0.0
    return np.sqrt(periods_per_year) * excess.mean() / excess.std()


def max_drawdown(equity: list[float]) -> float:
    if not equity:
        return 0.0
    arr = np.array(equity)
    peak = np.maximum(np.maximum.accumulate(arr), 1e-9)
    drawdown = arr / peak - 1
    return float(drawdown.min())


__all__ = ["cagr", "sharpe", "max_drawdown"]
