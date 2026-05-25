"""LoggingStrategy — Phase-1 stub implementation of ForProducingSolution.

Records every grid-power update and logs it. Does not yet produce a
Solution or fire `hbc_solution_ready`; replace with real strategies as
they land in Phase 2.

See ADR-002 §"Phased Delivery".
"""

from __future__ import annotations

import logging

_LOGGER = logging.getLogger(__name__)


class LoggingStrategy:
    """Phase-1 stub satisfying ForProducingSolution via `on_grid_power`."""

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
