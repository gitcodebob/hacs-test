"""Config flow tests: initial setup and reconfigure."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant import config_entries, data_entry_flow

from custom_components.home_battery_control.const import CONF_P1_ENTITY, DOMAIN

P1_A = "sensor.fake_p1"
P1_B = "sensor.fake_p1_alt"


async def test_user_flow_creates_entry(hass):
    hass.states.async_set(P1_A, "0", {"device_class": "power", "unit_of_measurement": "W"})

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_P1_ENTITY: P1_A}
    )
    await hass.async_block_till_done()

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_P1_ENTITY: P1_A}


async def test_reconfigure_updates_entry_and_reloads(hass):
    hass.states.async_set(P1_A, "0", {"device_class": "power", "unit_of_measurement": "W"})
    hass.states.async_set(P1_B, "0", {"device_class": "power", "unit_of_measurement": "W"})

    entry = MockConfigEntry(domain=DOMAIN, data={CONF_P1_ENTITY: P1_A})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id) is True
    await hass.async_block_till_done()

    result = await entry.start_reconfigure_flow(hass)
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_P1_ENTITY: P1_B}
    )
    await hass.async_block_till_done()

    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert entry.data[CONF_P1_ENTITY] == P1_B
