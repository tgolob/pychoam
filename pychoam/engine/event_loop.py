from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterable

from ..data.bar import Bar
from ..logging_cfg import get_logger


@dataclass(slots=True)
class Order:
    action: str
    quantity: int


class EventLoop:
    """Event-driven loop connecting feed, strategy and broker."""

    def __init__(self, feed: AsyncIterable[Bar], strategy, broker, settings) -> None:
        self.feed = feed
        self.strategy = strategy
        self.broker = broker
        self.settings = settings
        self.position = 0
        self.entry_price = 0.0
        self.log = get_logger(__name__)

    async def run(self) -> None:
        async for bar in self.feed:
            if self.position and self.settings.stop_pct:
                stop = self.entry_price * (1 - self.settings.stop_pct)
                if bar.c <= stop:
                    await self.broker.execute(
                        order=Order("SELL", self.position),
                        contract=None,
                        bar=bar,
                    )
                    self.log.info("stop hit at %.2f", bar.c)
                    self.position = 0
            order = self.strategy.on_bar(bar)
            if not order:
                continue
            if order.action == "BUY" and self.position == 0:
                await self.broker.execute(
                    order=Order("BUY", self.settings.trade_qty),
                    contract=None,
                    bar=bar,
                )
                self.position = self.settings.trade_qty
                self.entry_price = bar.c
                self.log.info("bought %s at %.2f", self.position, bar.c)
            elif order.action == "SELL" and self.position:
                await self.broker.execute(
                    order=Order("SELL", self.position),
                    contract=None,
                    bar=bar,
                )
                self.log.info("sold %s at %.2f", self.position, bar.c)
                self.position = 0


__all__ = ["EventLoop", "Order"]
