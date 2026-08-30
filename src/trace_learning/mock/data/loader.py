"""Load deterministic mock domain data from JSON files."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

MOCK_DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "mock"


@lru_cache(maxsize=1)
def load_orders() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "orders.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_parts() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "parts.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_shipments() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "shipments.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_inventory() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "inventory.json").open() as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_tickets() -> dict[str, Any]:
    with (MOCK_DATA_DIR / "tickets.json").open() as f:
        return json.load(f)


def get_reference_date() -> str:
    return load_orders()["reference_date"]
