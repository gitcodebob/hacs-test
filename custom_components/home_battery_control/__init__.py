"""De Home Battery Control integratie."""

import logging

_LOGGER = logging.getLogger(__name__)
# Unique identifier for this integration; must match the folder name under custom_components/ , so "home_battery_control" in this case.
DOMAIN = "home_battery_control"


async def async_setup(hass, config):
    """Setup via YAML (leeg laten omdat we packages gebruiken)."""
    return True
