from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as get_dev_reg, DeviceEntryType

from custom_components.fast_fan.model import Device
from custom_components.fast_fan.model.fan.zhimi.ZA5 import FanZhimiZA5
from custom_components.fast_fan.model.fan.zhimi.ZA5.ent import FanEntity

from .const import DOMAIN

from miio import MiotDevice

import logging
_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = [
    "switch", 
]

# "button", "select",
#     "number", "sensor", "fan"

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry
) -> bool:
    ip = entry.data["ip"]
    token = entry.data["token"]

    _object = MiotDevice(ip=ip, token=token)
    _device = Device(_object)
    device = None
    
    match _device.info.model.lower():
        case "zhimi.fan.za5":
            device = FanZhimiZA5(object=_object)

    if device is None:
        raise Exception("Device not found")

    entity = FanEntity(device)
    entity.upload_entities()

    hass.data.setdefault(
        DOMAIN, {}
    )[entry.entry_id] = device

    await device.environment.upload_data()
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    dev_reg = get_dev_reg(hass)
    info = device.info
    dev_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, info.mac_address)},
        manufacturer="Xiaomi",
        name="Fast Fan",
        model=info.model,
        sw_version=info.firmware_version,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
