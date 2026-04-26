"""Global pytest fixtures for home_battery_control tests."""
import asyncio
import sys

from pytest_homeassistant_custom_component.common import MockConfigEntry

# pytest-socket blocks asyncio's internal socketpair() on Windows (ProactorEventLoop
# uses AF_INET socketpair for signalling). Switching to SelectorEventLoop avoids this.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

__all__ = ["MockConfigEntry"]
