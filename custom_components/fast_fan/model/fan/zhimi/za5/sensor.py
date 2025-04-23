from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass

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

class FanTempSensor(MySensorEntity):
    name_prefix: str = "Temperature"

    @property
    def native_value(self):
        return self.device.environment.temperature

    @property
    def native_unit_of_measurement(self):
        return "°C"
    
    @property
    def device_class(self):
        return SensorDeviceClass.TEMPERATURE

    @property
    def icon(self):
        return self.device.icon_temperature
    
    async def async_update(self):
        await self.device.environment.update_temperature()

class FanHumiditySensor(MySensorEntity):
    name_prefix: str = "Humidity"

    @property
    def native_value(self):
        return self.device.environment.humidity

    @property
    def native_unit_of_measurement(self):
        return "%"
    
    @property
    def device_class(self):
        return SensorDeviceClass.HUMIDITY

    @property
    def icon(self):
        return self.device.icon_humidity
    
    async def async_update(self):
        await self.device.environment.update_humidity()

class FanPowerSourceSensor(MySensorEntity):
    name_prefix: str = "Power Source"

    @property
    def native_value(self):
        return self.device.environment.power_source

    @property
    def icon(self):
        return self.device.icon_power_source

    async def async_update(self):
        await self.device.environment.update_power_source()