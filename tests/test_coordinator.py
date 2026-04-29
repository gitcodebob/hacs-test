"""End-to-end wiring test: P1 state change -> P1SensorListener -> StrategyPort."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.home_battery_control import async_setup_entry, async_unload_entry
from custom_components.home_battery_control.const import CONF_P1_ENTITY, DOMAIN

P1_ENTITY = "sensor.fake_p1"


async def test_p1_updates_reach_strategy(hass):
    hass.states.async_set(P1_ENTITY, "100")

    entry = MockConfigEntry(domain=DOMAIN, data={CONF_P1_ENTITY: P1_ENTITY})
    entry.add_to_hass(hass)

    assert await async_setup_entry(hass, entry) is True
    await hass.async_block_till_done()

    strategy = entry.runtime_data.strategy
    # Priming on setup counts as the first observed value.
    assert strategy.update_count == 1
    assert strategy.last_power_w == 100.0

    hass.states.async_set(P1_ENTITY, "250")
    await hass.async_block_till_done()
    assert strategy.update_count == 2
    assert strategy.last_power_w == 250.0

    # Unavailable / non-numeric states are skipped without raising.
    hass.states.async_set(P1_ENTITY, "unavailable")
    await hass.async_block_till_done()
    hass.states.async_set(P1_ENTITY, "not-a-number")
    await hass.async_block_till_done()
    assert strategy.update_count == 2
    assert strategy.last_power_w == 250.0

    assert await async_unload_entry(hass, entry) is True
