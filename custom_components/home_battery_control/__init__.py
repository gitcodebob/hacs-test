"""Home Battery Control integration setup."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .app.aggregation.adapters.inbound.p1_sensor_listener import P1SensorListener
from .app.aggregation.adapters.outbound.ha_state_reader import HaStateReader
from .app.aggregation.core.aggregator import Aggregator
from .app.strategy.core.strategies.logging_strategy import LoggingStrategy
from .const import CONF_P1_ENTITY, DOMAIN

__all__ = ["DOMAIN", "async_setup_entry", "async_unload_entry"]


@dataclass
class HBCRuntimeData:
    coordinator: P1SensorListener
    strategy: LoggingStrategy


type HBCConfigEntry = ConfigEntry[HBCRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: HBCConfigEntry) -> bool:
    p1_entity = entry.data[CONF_P1_ENTITY]
    strategy = LoggingStrategy()
    # Phase 1 wiring: P1 -> Aggregator -> Strategy(callback). The state-reader
    # is injected so the DI shape already matches Phase 2; its `.read()` is
    # not called yet. Phase 2 swaps the callback for a ForPublishingHbcMsg
    # outbound port + event-bus pipeline.
    state_reader = HaStateReader(hass)
    aggregator = Aggregator(
        on_grid_power=strategy.on_grid_power,
        state_reader=state_reader,
    )
    coordinator = P1SensorListener(hass, entry, p1_entity, aggregator)
    coordinator.prime_from_current_state()
    entry.runtime_data = HBCRuntimeData(coordinator=coordinator, strategy=strategy)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HBCConfigEntry) -> bool:
    # No manual teardown needed: the coordinator and the state-change listener
    # are both registered via entry.async_on_unload, so HA cleans them up.
    return True
