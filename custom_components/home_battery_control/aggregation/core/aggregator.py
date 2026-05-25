"""Aggregator — use-case implementation for ForBuildingHbcMsg.

Phase 1 scaffold: forwards each P1 reading to a callback. The Phase 2
shape — build a full HbcMsg and publish via a ForPublishingHbcMsg outbound
port — is documented on the port itself.

See ADR-002 §"State Aggregation".
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from .ports import ForPublishingHbcMsg  # noqa: F401 — Phase 2 contract documented in ports.py

_LOGGER = logging.getLogger(__name__)


class Aggregator:
    """Implements ForBuildingHbcMsg.

    Phase 1: takes a callable that receives each grid-power reading.
    Phase 2: will take a ForPublishingHbcMsg, build an HbcMsg, and
    publish it. The Aggregator's external API (`on_grid_power`) stays the
    same; only what it does internally changes.
    """

    def __init__(self, on_grid_power: Callable[[float], None]) -> None:
        self._on_grid_power = on_grid_power

    def on_grid_power(self, power_w: float) -> None:
        # TODO Phase 2: build HbcMsg(grid_power_w=power_w, timestamp=now(), ...)
        #               and call self._publisher.publish(msg).
        self._on_grid_power(power_w)
