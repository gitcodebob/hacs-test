"""Smoke test: verify the integration loads without errors."""
from custom_components.home_battery_control import DOMAIN


async def test_domain_constant():
    """The DOMAIN constant must match the component folder name."""
    assert DOMAIN == "home_battery_control"


async def test_async_setup(hass):
    """async_setup should return True and not raise."""
    from custom_components.home_battery_control import async_setup

    result = await async_setup(hass, {})
    assert result is True
