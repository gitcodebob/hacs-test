"""StrategyPort — the driven-side port of the HBC hexagonal architecture.

This module defines the stable contract (StrategyPort) between the
Application Core and any strategy implementation, whether built-in Python
or an external Node-RED flow. It also holds LoggingStrategy, a temporary
stub that satisfies the port for development and testing purposes.

See ADR-002 for the architectural framing.
"""

from __future__ import annotations

import logging
from typing import Protocol

_LOGGER = logging.getLogger(__name__)


class StrategyPort(Protocol):
    """Driven-side port: contract that every strategy must satisfy.

    Called by the Application Core (P1SensorListener / StateAggregator)
    when a new grid-power reading is available. The strategy processes the
    reading and is responsible for firing hbc_solution_ready on the HA
    event bus when it has produced a solution.
    """

    def on_grid_power(self, power_w: float) -> None: ...


class LoggingStrategy:
    """Stub strategy used during development — satisfies StrategyPort.

    Records every grid-power update and logs it. Does not fire
    hbc_solution_ready; replace with a real strategy for production use.
    """

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
