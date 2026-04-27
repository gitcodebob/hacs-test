"""Config flow for Home Battery Control."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import selector

from .const import CONF_P1_ENTITY, DOMAIN

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_P1_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor", device_class="power"),
        ),
    }
)


class HomeBatteryControlConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the user-initiated config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            self._async_abort_entries_match(user_input)
            return self.async_create_entry(
                title="Home Battery Control", data=user_input
            )
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)
