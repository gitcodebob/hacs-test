"""HaEventPublisher — outbound adapter implementing ForPublishingHbcMsg.

Phase 2 stub. Fires `hbc_msg_ready` on the HA event bus with the HbcMsg
serialised to a plain dict. Strategy adapters subscribe to that event.

See ADR-002 §"Always event-driven".
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from ....domain.events import HBC_MSG_READY
from ....domain.hbc_msg import HbcMsg


class HaEventPublisher:
    """Fires hbc_msg_ready on the HA event bus."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    def publish(self, msg: HbcMsg) -> None:
        # TODO Phase 2: serialise HbcMsg -> dict and fire via
        #               self._hass.bus.async_fire(HBC_MSG_READY, payload).
        raise NotImplementedError("Phase 2 — event-bus pipeline not yet wired")

    @staticmethod
    def event_name() -> str:
        return HBC_MSG_READY
