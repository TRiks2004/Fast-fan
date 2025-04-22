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
        return f"{self.device.info.mac_address}_{self.name_prefix.lower()}"

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

# class FanAnionSwitch(SwitchEntity):
    
#     def __init__(self, fan_device: FanZhimiZA5):
#         self._device = fan_device
#         self._name = f"{self._device.name} Anion"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def is_on(self):
#         return self._device.environment.is_anion

#     def turn_on(self):
#         self._device.anion_on()

#     def turn_off(self):
#         self._device.anion_off()

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_anion"

#     @property
#     def device_info(self):
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

#     @property
#     def icon(self):
#         return "mdi:blur" if self.is_on else "mdi:blur-off"
    
#     def update(self):
#         self._device.environment.is_anion = self._device.anion

# class FanPyhsicalControlLockedSwitch(SwitchEntity):

#     def __init__(self, fan_device: FanZhimiZA5):
#         self._device = fan_device
#         self._name = f"Fan Physical Control Locked {self._device.name}"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def is_on(self):
#         return self._device.environment.is_physical_controls_locked

#     def turn_on(self):
#         self._device.physical_controls_locked_on()

#     def turn_off(self):
#         self._device.physical_controls_locked_off()

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_physical_controls_locked"

#     @property
#     def device_info(self):
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

#     @property
#     def icon(self):
#         return "mdi:lock-outline" if self.is_on else "mdi:lock-open-variant-outline"
    
#     def update(self):
#         self._device.environment.is_physical_controls_locked = self._device.physical_controls_locked

# class FanAlarmSwitch(SwitchEntity):

#     def __init__(self, fan_device: FanZhimiZA5):
#         self._device = fan_device
#         self._name = f"Fan Alarm {self._device.name}"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def is_on(self):
#         return self._device.environment.is_alarm

#     def turn_on(self):
#         self._device.alarm_on()

#     def turn_off(self):
#         self._device.alarm_off()

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_alarm"

#     @property
#     def device_info(self):
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

#     @property
#     def icon(self):
#         return "mdi:bell-outline" if self.is_on else "mdi:bell-off-outline"
    
#     def update(self):
#         self._device.environment.is_alarm = self._device.alarm
