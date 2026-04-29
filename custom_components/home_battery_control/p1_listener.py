"""P1SensorListener — driving adapter in the HBC hexagonal architecture.

Translates Home Assistant state-change events from the P1 grid-power sensor
into domain calls on a StrategyPort. This is a push-mode adapter: it does
not poll. It subscribes to entity state changes and forwards valid readings
to the strategy, which is responsible for producing a solution.

See ADR-002 for the architectural framing.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import (
    Event,
    EventStateChangedData,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .strategy_port import StrategyPort

_LOGGER = logging.getLogger(__name__)


class P1SensorListener(DataUpdateCoordinator[float | None]):
    """Driving adapter: subscribes to the P1 sensor and forwards readings to a StrategyPort."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        p1_entity: str,
        strategy: StrategyPort,
    ) -> None:
        # Passing config_entry explicitly opts in to HA's auto-cleanup:
        # the coordinator's `async_shutdown` is wired to the entry's unload.
        super().__init__(hass, _LOGGER, name="P1SensorListener", config_entry=entry)
        self._p1_entity = p1_entity
        self._strategy = strategy
        # async_on_unload guarantees this listener is detached when the
        # entry is unloaded or reloaded — no manual bookkeeping needed.
        entry.async_on_unload(
            async_track_state_change_event(hass, [p1_entity], self._handle_state_change)
        )

    @callback
    def _handle_state_change(self, event: Event[EventStateChangedData]) -> None:
        self._dispatch(event.data.get("new_state"))

    @callback
    def prime_from_current_state(self) -> None:
        """Forward the entity's current state once at setup, if valid."""
        self._dispatch(self.hass.states.get(self._p1_entity))

    @callback
    def _dispatch(self, state: State | None) -> None:
        if state is None or state.state in ("unknown", "unavailable"):
            return
        try:
            power_w = float(state.state)
        except (TypeError, ValueError):
            _LOGGER.warning(
                "P1 entity %s has non-numeric state %r; skipping",
                self._p1_entity,
                state.state,
            )
            return
        self._strategy.on_grid_power(power_w)
        self.async_set_updated_data(power_w)
