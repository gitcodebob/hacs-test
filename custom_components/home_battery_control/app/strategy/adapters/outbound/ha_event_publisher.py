"""HaEventPublisher — outbound adapter implementing ForPublishingSolution.

Phase 2 stub. Fires `hbc_solution_ready` on the HA event bus once a
strategy has produced a Solution.

See ADR-002 §"Always event-driven".
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from ....domain.events import HBC_SOLUTION_READY
from ....domain.solution import Solution


class HaEventPublisher:
    """Fires hbc_solution_ready on the HA event bus."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    def publish(self, solution: Solution) -> None:
        # TODO Phase 2: serialise Solution -> dict and fire via
        #               self._hass.bus.async_fire(HBC_SOLUTION_READY, payload).
        raise NotImplementedError("Phase 2 — event-bus pipeline not yet wired")

    @staticmethod
    def event_name() -> str:
        return HBC_SOLUTION_READY
