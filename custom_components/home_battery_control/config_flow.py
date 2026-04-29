"""Config flow for Home Battery Control."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import selector

from .const import CONF_P1_ENTITY, DOMAIN

# Schema for the single-step user form. EntitySelector renders an entity
# picker in the UI and HA validates that the chosen entity matches every
# filter — here: any `sensor` entity whose `device_class` is `power`.
USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_P1_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor", device_class="power"),
        ),
    }
)


class HomeBatteryControlConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the user-initiated config flow.

    `domain=DOMAIN` registers this class with HA as the flow handler
    for our integration; HA finds it during `Add Integration`.
    """

    # Version of the `entry.data` shape. Bump when the schema changes —
    # HA will then call `async_migrate_entry` for older entries.
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        # HA calls this method twice: first with user_input=None (render the
        # form) and again after the user submits (with their answers).
        if user_input is not None:
            # Reject if another entry already stores the same P1 entity —
            # one P1 meter per HA instance is the realistic case.
            self._async_abort_entries_match(user_input)
            return self.async_create_entry(
                title="Home Battery Control", data=user_input
            )
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        # Triggered from the integration card's "..." menu -> Reconfigure.
        # Same form as the initial setup, but writes back to the existing
        # entry and reloads it so the coordinator re-subscribes.
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            # Allow the user to resubmit the same value (no-op), but still
            # block collisions with *other* entries.
            if dict(user_input) != dict(entry.data):
                self._async_abort_entries_match(user_input)
            return self.async_update_reload_and_abort(
                entry, data_updates=user_input
            )
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                USER_SCHEMA, dict(entry.data)
            ),
        )
