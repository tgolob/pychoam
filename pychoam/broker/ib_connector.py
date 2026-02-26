from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Optional

from ib_insync import IB, Contract, MarketOrder

from ..config import Settings
from ..logging_cfg import get_logger
from ..data.bar import Bar
from ..engine.event_loop import Order


@dataclass
class IBConnector:
    """Thin wrapper around ``ib_insync.IB`` with reconnect logic."""

    settings: Settings
    ib: IB = IB()

    async def connect(self) -> None:
        logger = get_logger(__name__)
        while True:
            try:
                await self.ib.connectAsync(
                    self.settings.ib_host,
                    self.settings.ib_port,
                    clientId=self.settings.ib_client_id,
                )
                logger.info("connected to IB")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("IB connection failed: %s", exc)
                await asyncio.sleep(5)

    async def execute(self, contract: Contract, order: Order, _bar: Optional[Bar] = None) -> None:
        ib_order = MarketOrder(order.action, order.quantity)
        await self.ib.placeOrderAsync(contract, ib_order)


__all__ = ["IBConnector"]
