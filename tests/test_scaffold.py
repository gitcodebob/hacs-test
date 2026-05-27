"""Step 1 — the ``/app`` package skeleton imports cleanly (PLAN.md).

Imported at module top level (as in ``test_init``); a successful collection of
this module is itself the assertion that every package is importable.
"""

from custom_components.home_battery_control import app
from custom_components.home_battery_control.app import (
    control,
    market,
    planning,
    resources,
    strategy,
)
from custom_components.home_battery_control.app.control import core
from custom_components.home_battery_control.app.control.core import ports
from custom_components.home_battery_control.app.control.core.ports import (
    inbound,
    outbound,
)

PACKAGES = [
    app,
    control,
    core,
    ports,
    inbound,
    outbound,
    resources,
    strategy,
    planning,
    market,
]


def test_every_package_imports():
    assert all(module is not None for module in PACKAGES)
