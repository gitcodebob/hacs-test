"""SolutionReadyListener — inbound adapter for Distribution.

Phase 2 stub. Subscribes to `hbc_solution_ready` on the HA event bus and
invokes the Dispatcher via ForDispatchingSolution.

See ADR-002 §"Always event-driven".
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from ....domain.events import HBC_SOLUTION_READY
from ...core.ports import ForDispatchingSolution


class SolutionReadyListener:
    """Subscribes to hbc_solution_ready and calls the Dispatcher."""

    def __init__(self, hass: HomeAssistant, dispatcher: ForDispatchingSolution) -> None:
        self._hass = hass
        self._dispatcher = dispatcher

    def start(self) -> None:
        # TODO Phase 2: subscribe to HBC_SOLUTION_READY, deserialise the
        #               payload into a Solution, and call dispatcher.dispatch(sol).
        raise NotImplementedError("Phase 2 — event-bus pipeline not yet wired")

    @staticmethod
    def event_name() -> str:
        return HBC_SOLUTION_READY
