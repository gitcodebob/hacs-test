"""Home Battery Control integration setup.

Clean slate: this is the minimal entry point Home Assistant requires so the
integration loads and the config flow works. The control wiring (orchestrator,
resources, strategies) lands here as PLAN.md is implemented — see step 7,
"Wire into Home Assistant".
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

__all__ = ["DOMAIN", "async_setup_entry", "async_unload_entry"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
