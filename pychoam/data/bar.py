from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Bar:
    ts: datetime
    o: float
    h: float
    l: float  # noqa: E741
    c: float
    v: float


__all__ = ["Bar"]
