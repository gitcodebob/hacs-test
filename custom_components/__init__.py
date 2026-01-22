"""De Home Battery Control integratie."""
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "home_battery_control_test"

async def async_setup(hass, config):
    """Setup via YAML (leeg laten omdat we packages gebruiken)."""
    return True