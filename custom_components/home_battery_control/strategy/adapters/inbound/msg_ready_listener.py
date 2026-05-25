"""MsgReadyListener — inbound adapter for Strategy.

Phase 2 stub. Subscribes to `hbc_msg_ready` on the HA event bus and
invokes the active strategy via ForProducingSolution.

See ADR-002 §"Always event-driven".
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from ....domain.events import HBC_MSG_READY
from ...core.ports import ForProducingSolution


class MsgReadyListener:
    """Subscribes to hbc_msg_ready and dispatches to the active strategy."""

    def __init__(self, hass: HomeAssistant, strategy: ForProducingSolution) -> None:
        self._hass = hass
        self._strategy = strategy

    def start(self) -> None:
        # TODO Phase 2: subscribe to HBC_MSG_READY, deserialise the payload
        #               into an HbcMsg, and call self._strategy.produce(msg).
        raise NotImplementedError("Phase 2 — event-bus pipeline not yet wired")

    @staticmethod
    def event_name() -> str:
        return HBC_MSG_READY
