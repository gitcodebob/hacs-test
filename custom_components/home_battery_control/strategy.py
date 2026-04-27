"""Strategy interface and a temporary logging implementation.

The strategy interface is the stable extension point between the
HBCCoordinator and any concrete strategy (built-in or Node-RED). For
this proof-of-concept it carries only the grid power; richer payloads
(battery count, SoC, etc.) are deferred until the interface is specced.
"""

from __future__ import annotations

import logging
from typing import Protocol

_LOGGER = logging.getLogger(__name__)


class StrategyInterface(Protocol):
    """Contract the coordinator uses to invoke a strategy."""

    def on_grid_power(self, power_w: float) -> None: ...


class LoggingStrategy:
    """Temporary strategy that records updates and logs each one."""

    def __init__(self) -> None:
        self.update_count: int = 0
        self.last_power_w: float | None = None

    def on_grid_power(self, power_w: float) -> None:
        self.update_count += 1
        self.last_power_w = power_w
        _LOGGER.info(
            "HBC strategy update #%d: grid_power=%.1f W",
            self.update_count,
            power_w,
        )
