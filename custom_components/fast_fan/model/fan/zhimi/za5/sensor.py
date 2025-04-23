from homeassistant.components.sensor import SensorEntity

from custom_components.fast_fan.const import DOMAIN
from custom_components.fast_fan.model.fan.zhimi.za5 import FanZhimiZA5

class MySensorEntity(SensorEntity):
    name_prefix: str = None
    
    def __init__(self, device: FanZhimiZA5):
        self.device = device
        self.device._sensors_entities.append(self)

    @property
    def unique_id(self):
        return f"{self.device.info.mac_address}_{"_".join(self.name_prefix.lower().split(' '))}"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self.device.info.mac_address)}}

    @property
    def name(self):
        return f"{self.device.name} {self.name_prefix}"


class FanSpeedRpmSensor(MySensorEntity):
    name_prefix: str = "Speed RPM"

    @property
    def native_value(self):
        return self.device.environment.speed_rpm

    @property
    def native_unit_of_measurement(self):
        return self.device.unit_speed_rpm

    @property
    def icon(self):
        return self.device.icon_speed_rpm
    
    async def async_update(self):
        await self.device.environment.update_speed_rpm()

# class FanTempSensor(SensorEntity):
#     def __init__(self, fan_device: FanZA5):
#         self._device = fan_device
#         self._name = f"Fan Temp {self._device.name}"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def native_value(self):
#         return self._device.environment.temperature

#     @property
#     def native_unit_of_measurement(self):
#         return "°C"

#     @property
#     def icon(self):
#         return "mdi:thermometer"

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_temperature"

#     @property
#     def device_info(self):
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}
    
#     def update(self):
#         self._device.environment.temperature = self._device.temperature
    
# class FanHumiditySensor(SensorEntity):
#     def __init__(self, fan_device: FanZA5):
#         self._device = fan_device
#         self._name = f"Fan Humidity {self._device.name}"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def native_value(self):
#         return self._device.environment.humidity

#     @property
#     def native_unit_of_measurement(self):
#         return "%"

#     @property
#     def icon(self):
#         return "mdi:water-percent"

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_humidity"

#     @property
#     def device_info(self):
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}
    
#     def update(self):
#         self._device.environment.humidity = self._device.humidity
    
# class FanBatterySensor(SensorEntity):
#     def __init__(self, fan_device: FanZA5):
#         self._device = fan_device
#         self._name = f"Fan Battery State {self._device.name}"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def native_value(self) -> bool:
#         return self._device.environment.is_battery_state

#     @property
#     def icon(self):
#         return "mdi:battery" if self.native_value else "mdi:battery-off"

#     @property
#     def device_class(self):
#         return "battery"

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_battery"

#     @property
#     def device_info(self):
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}
    
#     def update(self):
#         self._device.environment.is_battery_state = self._device.battery_state

# class FanAcStateSensor(SensorEntity):
#     def __init__(self, fan_device: FanZA5):
#         self._device = fan_device
#         self._name = f"AC Power {self._device.name}"

#     @property
#     def name(self):
#         return self._name

#     @property
#     def native_value(self) -> bool:
#         return self._device.environment.is_ac_state

#     @property
#     def icon(self):
#         return "mdi:power-plug-outline" if self.native_value else "mdi:power-plug-off-outline"

#     @property
#     def device_class(self):
#         return "power"

#     @property
#     def unique_id(self):
#         return f"{self._device.info.mac_address}_ac_state"

#     @property
#     def device_info(self):
#         _LOGGER.error(f"ac_state: {self._device.ac_state} | DOMAIN: {DOMAIN} | mac_address: {self._device.info.mac_address}")
#         return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}
    
#     def update(self):
#         self._device.pull_data()

