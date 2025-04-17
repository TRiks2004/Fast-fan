from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import fan
from .const import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["switch", "button", "select"]

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry
) -> bool:
    _object = fan.Fan(
        hass, 
        entry.data["ip"], 
        entry.data["token"]
    )
    
    hass.data.setdefault(
        DOMAIN, {}
    )[entry.entry_id] = _object

    await hass.async_add_executor_job(_object.pull_data)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
