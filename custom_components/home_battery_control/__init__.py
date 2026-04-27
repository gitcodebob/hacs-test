"""Home Battery Control integration setup."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_P1_ENTITY, DOMAIN
from .coordinator import HBCCoordinator
from .strategy import LoggingStrategy

__all__ = ["DOMAIN", "async_setup_entry", "async_unload_entry"]


@dataclass
class HBCRuntimeData:
    coordinator: HBCCoordinator
    strategy: LoggingStrategy


type HBCConfigEntry = ConfigEntry[HBCRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: HBCConfigEntry) -> bool:
    p1_entity = entry.data[CONF_P1_ENTITY]
    strategy = LoggingStrategy()
    coordinator = HBCCoordinator(hass, p1_entity, strategy)
    coordinator.prime_from_current_state()
    entry.runtime_data = HBCRuntimeData(coordinator=coordinator, strategy=strategy)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HBCConfigEntry) -> bool:
    await entry.runtime_data.coordinator.async_shutdown()
    return True
