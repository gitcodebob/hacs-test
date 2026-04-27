"""HBCCoordinator: detects P1 power-meter updates and forwards them to a strategy.

This is a push-mode DataUpdateCoordinator: it does not poll. It subscribes
to state changes of the configured P1 sensor and invokes the strategy on
each valid update. See ADR-002 for the architectural framing.
"""

from __future__ import annotations

import logging

from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .strategy import StrategyInterface

_LOGGER = logging.getLogger(__name__)


class HBCCoordinator(DataUpdateCoordinator[float | None]):
    """Watches the P1 sensor and pushes grid-power updates to the strategy."""

    def __init__(
        self,
        hass: HomeAssistant,
        p1_entity: str,
        strategy: StrategyInterface,
    ) -> None:
        super().__init__(hass, _LOGGER, name="HBCCoordinator")
        self._p1_entity = p1_entity
        self._strategy = strategy
        self._unsub = async_track_state_change_event(
            hass, [p1_entity], self._handle_state_change
        )

    @callback
    def _handle_state_change(self, event: Event[EventStateChangedData]) -> None:
        self._dispatch(event.data.get("new_state"))

    @callback
    def prime_from_current_state(self) -> None:
        """Forward the entity's current state once at setup, if valid."""
        self._dispatch(self.hass.states.get(self._p1_entity))

    @callback
    def _dispatch(self, state) -> None:
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

    async def async_shutdown(self) -> None:
        self._unsub()
        await super().async_shutdown()
