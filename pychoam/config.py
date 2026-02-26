from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


def _load_env(path: str | Path) -> None:
    """Simple .env file loader."""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


@dataclass
class Settings:
    """Application settings loaded from env or YAML."""

    ib_host: str = "127.0.0.1"
    ib_port: int = 7497
    ib_client_id: int = 1
    trade_qty: int = 1
    stop_pct: float | None = None

    @classmethod
    def load(cls, env_path: str | None = None, yaml_path: str | None = None) -> "Settings":
        if env_path:
            _load_env(env_path)
        data: Dict[str, Any] = {}
        if yaml_path:
            with Path(yaml_path).open("r", encoding="utf-8") as fh:
                data.update(yaml.safe_load(fh) or {})
        data.update(
            ib_host=os.getenv("IB_HOST", str(cls.ib_host)),
            ib_port=int(os.getenv("IB_PORT", str(cls.ib_port))),
            ib_client_id=int(os.getenv("IB_CLIENT_ID", str(cls.ib_client_id))),
            trade_qty=int(os.getenv("TRADE_QTY", str(cls.trade_qty))),
            stop_pct=float(os.getenv("STOP_PCT", "0") or 0) or None,
        )
        return cls(**data)


__all__ = ["Settings"]
