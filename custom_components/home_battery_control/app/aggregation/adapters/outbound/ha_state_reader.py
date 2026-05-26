"""HaStateReader — outbound adapter implementing ForReadingHouseState.

Phase 2 stub. Reads relevant HA entity states via `hass.states.get(...)`
and assembles a HouseStateSnapshot. Which entities are relevant is owned
by this adapter — the core only sees the snapshot.

See ADR-002 §"State Aggregation".
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from ...core.house_state_snapshot import HouseStateSnapshot


class HaStateReader:
    """Reads relevant HA entity states into a HouseStateSnapshot."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    def read(self) -> HouseStateSnapshot:
        # TODO Phase 2: read devices/settings/plan from HA entity states
        #               (see ADR-002 §"State lives in Home Assistant" and
        #               ADR-005 for the asset-keyed device/settings shape).
        raise NotImplementedError("Phase 2 — state reader not yet wired")
