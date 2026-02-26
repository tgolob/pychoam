from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

import typer
from ib_insync import Contract, Stock

from .broker.ib_connector import IBConnector
from .config import Settings
from .data.feeds import CSVFeed, LiveFeed
from .engine.backtester import Backtester
from .engine.event_loop import EventLoop
from .strategy.sma_crossover import SmaCrossStrategy

app = typer.Typer()


@app.command()
def backtest(
    file: Path = typer.Option(..., "--file", "-f", exists=True, help="CSV file"),
    env: Optional[Path] = typer.Option(None, help="Path to .env"),
) -> None:
    settings = Settings.load(env_path=str(env) if env else None)
    feed = CSVFeed(file)
    strategy = SmaCrossStrategy(quantity=settings.trade_qty)
    tester = Backtester(feed, strategy, settings)
    asyncio.run(tester.run())


@app.command()
def live(
    env: Path = typer.Option(..., help="Path to .env"),
    symbol: str = "TQQQ",
) -> None:
    settings = Settings.load(env_path=str(env))
    ib = IBConnector(settings)
    asyncio.run(ib.connect())
    contract: Contract = Stock(symbol, "SMART", "USD")
    feed = LiveFeed(ib, contract)
    strategy = SmaCrossStrategy(quantity=settings.trade_qty)
    loop = EventLoop(feed, strategy, ib, settings)
    asyncio.run(loop.run())


if __name__ == "__main__":
    app()
