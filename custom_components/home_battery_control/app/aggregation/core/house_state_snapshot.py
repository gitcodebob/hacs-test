"""HouseStateSnapshot — return type of the state-reader outbound port.

Internal to the Aggregation context: holds the fields the Aggregator needs
to build an HbcMsg, minus the trigger value that already arrived via the
inbound port (`grid_power_w`).

See ADR-002 §"State Aggregation".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HouseStateSnapshot:
    """Snapshot of relevant HA entity states at a single point in time."""

    devices: dict[str, dict[str, Any]] = field(default_factory=dict)
    settings: dict[str, dict[str, Any]] = field(default_factory=dict)
    plan: dict[str, Any] | None = None
