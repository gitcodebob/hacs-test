"""Aggregator — use-case implementation for ForBuildingHbcMsg.

Phase 1 scaffold: forwards each P1 reading to a callback. The Phase 2
shape — build a full HbcMsg and publish via a ForPublishingHbcMsg outbound
port — is documented on the port itself.

See ADR-002 §"State Aggregation".
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from .ports import (
    ForPublishingHbcMsg,  # noqa: F401 — Phase 2 contract documented in ports.py
    ForReadingHouseState,
)

_LOGGER = logging.getLogger(__name__)


class Aggregator:
    """Implements ForBuildingHbcMsg.

    Phase 1: takes a callable that receives each grid-power reading. The
    state-reader and publisher ports are already injected so the DI shape
    matches Phase 2; their `.read()` / `.publish()` methods are not called
    yet.
    Phase 2: will call `state_reader.read()`, build an HbcMsg, and
    `publisher.publish(msg)`. The Aggregator's external API
    (`on_grid_power`) stays the same; only what it does internally changes.
    """

    def __init__(
        self,
        on_grid_power: Callable[[float], None],
        state_reader: ForReadingHouseState,
    ) -> None:
        self._on_grid_power = on_grid_power
        self._state_reader = state_reader

    def on_grid_power(self, power_w: float) -> None:
        # TODO Phase 2: snap = self._state_reader.read()
        #               msg = HbcMsg(grid_power_w=power_w, timestamp=now(),
        #                            devices=snap.devices, settings=snap.settings,
        #                            plan=snap.plan)
        #               self._publisher.publish(msg).
        self._on_grid_power(power_w)
