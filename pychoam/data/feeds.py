from __future__ import annotations

from asyncio import sleep
from pathlib import Path
from typing import AsyncIterator, Iterable

import pandas as pd
from ib_insync import Contract

from .bar import Bar
from ..broker.ib_connector import IBConnector


class IDataFeed(Iterable[Bar]):
    """Abstract data feed."""

    async def __aiter__(self) -> AsyncIterator[Bar]:  # pragma: no cover - interface
        raise NotImplementedError


class CSVFeed(IDataFeed):
    def __init__(self, path: str | Path):
        df = pd.read_csv(path, parse_dates=["ts"])
        self._bars = [
            Bar(row.ts.to_pydatetime(), row.o, row.h, row.l, row.c, row.v)
            for row in df.itertuples(index=False)
        ]

    def __iter__(self) -> Iterable[Bar]:
        return iter(self._bars)

    async def __aiter__(self) -> AsyncIterator[Bar]:
        for bar in self._bars:
            yield bar
            await sleep(0)


class LiveFeed(IDataFeed):
    """Real-time feed from Interactive Brokers."""

    def __init__(self, ib: IBConnector, contract: Contract):
        self._ib = ib
        self._contract = contract

    def __iter__(self) -> Iterable[Bar]:
        return iter([])

    async def __aiter__(self) -> AsyncIterator[Bar]:
        bars = await self._ib.ib.reqHistoricalDataAsync(
            self._contract,
            endDateTime="",
            durationStr="1 D",
            barSizeSetting="1 min",
            whatToShow="TRADES",
            useRTH=True,
        )
        for bar in bars:
            yield Bar(bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume)
            await sleep(0)


__all__ = ["IDataFeed", "CSVFeed", "LiveFeed"]
