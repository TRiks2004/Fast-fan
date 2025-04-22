from homeassistant.components.switch import SwitchEntity
from custom_components.fast_fan.const import DOMAIN
from custom_components.fast_fan.model.fan.zhimi.za5 import FanZhimiZA5


class MySwitchEntity(SwitchEntity):
    name_prefix: str = None
    
    def __init__(self, device: FanZhimiZA5):
        self.device = device
        self.device._switchs_entities.append(self)

    @property
    def unique_id(self):
        return f"{self.device.info.mac_address}_{"_".join(self.name_prefix.lower().split(' '))}"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self.device.info.mac_address)}}

    @property
    def name(self):
        return f"{self.device.name} {self.name_prefix}"

class FanPowerSwitch(MySwitchEntity):

    name_prefix = "Power"

    @property
    def icon(self):
        return self.device.icon_power

    @property
    def is_on(self):
        return self.device.environment.is_power

    async def async_turn_on(self):
        await self.device.set_power_on()

    async def async_turn_off(self):
        await self.device.set_power_off()
    
    async def async_update(self):
        await self.device.environment.update_power()

class FanSwingModeSwitch(MySwitchEntity):
    
    name_prefix = "Swing Mode"
    
    @property
    def icon(self):
        return self.device.icon_swing_mode

    @property
    def is_on(self):
        return self.device.environment.is_swing_mode

    async def async_turn_on(self):
        await self.device.set_swing_mode_on()

    async def async_turn_off(self):
        await self.device.set_swing_mode_off()
    
    async def async_update(self):
        await self.device.environment.update_swing_mode()

class FanAnionSwitch(MySwitchEntity):
    
    name_prefix = "Anion"
    
    @property
    def icon(self):
        return self.device.icon_anion

    @property
    def is_on(self):
        return self.device.environment.is_anion

    async def async_turn_on(self):
        await self.device.set_anion_on()

    async def async_turn_off(self):
        await self.device.set_anion_off()
    
    async def async_update(self):
        await self.device.environment.update_anion()

class FanPyhsicalControlLockedSwitch(MySwitchEntity):
    
    name_prefix = "Physical Control Locked"
    
    @property
    def icon(self):
        return self.device.icon_physical_controls_locked

    @property
    def is_on(self):
        return self.device.environment.is_physical_controls_locked

    async def async_turn_on(self):
        await self.device.set_physical_controls_locked_on()

    async def async_turn_off(self):
        await self.device.set_physical_controls_locked_off()
    
    async def async_update(self):
        await self.device.environment.update_physical_controls_locked()

class FanAlarmSwitch(MySwitchEntity):
    
    name_prefix = "Alarm"
    
    @property
    def icon(self):
        return self.device.icon_alarm

    @property
    def is_on(self):
        return self.device.environment.is_alarm

    async def async_turn_on(self):
        await self.device.set_alarm_on()

    async def async_turn_off(self):
        await self.device.set_alarm_off()
    
    async def async_update(self):
        await self.device.environment.update_alarm()