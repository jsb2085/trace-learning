"""Load deterministic warehouse mock data from JSON files."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

MOCK_DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "mock"


@lru_cache(maxsize=1)
def load_warehouse() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "warehouse.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_pick_orders() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "pick_orders.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_skus() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "skus.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_locations() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "locations.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_lots() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "lots.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_inbound() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "inbound.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_workers() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "workers.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_wms() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "wms.json").open() as f:
        return json.load(f)


def get_reference_date() -> str:
    return load_warehouse()["reference_date"]
