"""Smoke tests: integration imports and exposes the expected DOMAIN."""
from custom_components.home_battery_control import DOMAIN


def test_domain_constant():
    """The DOMAIN constant must match the component folder name."""
    assert DOMAIN == "home_battery_control"
