"""BatteryCommandAdapter — outbound adapter implementing ForCommandingAsset.

Phase 2 stub. Translates per-slot battery setpoints into HA service calls
(typically `number.set_value` against the battery's power-control entity).

See ADR-002 §"Distribution" and ADR-005 §"Asset Abstraction".
"""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant


class BatteryCommandAdapter:
    """Commands the home battery."""

    asset_name = "battery"

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    def command(self, setpoints: dict[str, Any]) -> None:
        # TODO Phase 2: map setpoints (e.g., {"power_w": 1500}) to the
        #               battery's HA service call(s).
        raise NotImplementedError("Phase 2 — battery command path not yet wired")
