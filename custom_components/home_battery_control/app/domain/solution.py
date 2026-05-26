"""Solution — output of the Strategy context.

Per-asset setpoints keyed by asset name (see ADR-005). The Distribution
context iterates these to command devices.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Solution:
    """Per-asset setpoints produced by a Strategy.

    Example: {"battery": {"power_w": 1500}, "ev_charger": {"charge_w": 0}}
    """

    setpoints: dict[str, dict[str, Any]] = field(default_factory=dict)
