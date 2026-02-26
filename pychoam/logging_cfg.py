from __future__ import annotations

import logging
from typing import Optional

from rich.logging import RichHandler


def setup(level: int | str = "INFO") -> None:
    """Configure global logging with a rich handler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    setup()
    return logging.getLogger(name)


__all__ = ["setup", "get_logger"]
