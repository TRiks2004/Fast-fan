from typing import Literal
import logging
import time

from miio import MiotDevice

from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.sensor import SensorEntity

from custom_components.fast_fan.const import DOMAIN 
from custom_components.fast_fan.command import Command
from .common_fan_za5 import CommonFanZA5


_LOGGER = logging.getLogger(__name__)

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class ModelFanZA5:
    model='zhimi.fan.za5'

    lavels = [1, 2, 3, 4]

    min_angle = 30
    max_angle = 120 

    def __init__(self, object: MiotDevice) -> None:
        self.object = object
        self.info = self.object.info()

    def __get(
        self, *, _command: Command
    ) -> (int | float | bool | str):
        _values = self.object.get_property_by(siid=_command.siid, piid=_command.piid)
        
        _value = _values[0]
        _code = _value.get('code')
        
        if _code is None or _code != 0:
            raise Exception(f'Error code: {_code}')
        
        return _value.get('value')

    def __set(
        self, *, _command: Command,
        value: (int | float | bool | str), timeout: int = 1
    ) -> (int | float | bool | str):
        _value = value

        while True:
            self.object.set_property_by(siid=_command.siid, piid=_command.piid, value=value)
            time.sleep(timeout)

            try:
                _value = self.__get(_command=_command)
                _LOGGER.error(f'Current value: {_value}')
                if _value == value:
                    break
            except Exception as e:
                _LOGGER.error(e)
                break
            
        return _value

    @property
    def speed_rpm(self) -> int: 
        return self.__get(_command = CommonFanZA5.CustomService.speed_rpm)

    @property
    def power(self) -> bool: 
        return self.__get(_command = CommonFanZA5.Fan.power)

    @power.setter
    def power(self, value: bool) -> None: 
        self.__set(_command = CommonFanZA5.Fan.power, value=value)

    @property
    def level(self) -> int: 
        return self.__get(_command = CommonFanZA5.Fan.level)

    @level.setter
    def level(self, value: int) -> None: 
        self.__set(_command = CommonFanZA5.Fan.level, value=value)

    @property
    def swing_mode(self) -> bool:
        return self.__get(_command = CommonFanZA5.Fan.swing_mode)
    
    @swing_mode.setter
    def swing_mode(self, value: bool) -> None:
        self.__set(_command = CommonFanZA5.Fan.swing_mode, value=value)

    @property
    def swing_angle(self) -> int:
        return self.__get(_command = CommonFanZA5.Fan.swing_mode_angle)
    
    @swing_angle.setter
    def swing_angle(self, value: int) -> None:
        if not (self.min_angle <= value <= self.max_angle):
            raise ValueError('Angle must be between 30 and 120 degrees')
        
        self.__set(_command = CommonFanZA5.Fan.swing_mode_angle, value=value)

    @property
    def anion(self) -> bool:
        return self.__get(_command = CommonFanZA5.Fan.anion)
    
    @anion.setter
    def anion(self, value: bool) -> None:
        self.__set(_command = CommonFanZA5.Fan.anion, value=value)

    @property
    def temperature(self) -> int:
        return self.__get(_command = CommonFanZA5.Environment.temperature)
    
    @property
    def humidity(self) -> int:
        return self.__get(_command = CommonFanZA5.Environment.humidity)

    @property
    def speed_procent(self) -> int:
        return self.__get(_command = CommonFanZA5.CustomService.speed_procent)
    
    @speed_procent.setter
    def speed_procent(self, value: int) -> None:
        self.__set(_command = CommonFanZA5.CustomService.speed_procent, value=value)

    @property
    def physical_controls_locked(self) -> bool:
        return self.__get(_command = CommonFanZA5.PhysicalControlLocked.physical_controls_locked)
    
    @physical_controls_locked.setter
    def physical_controls_locked(self, value: bool) -> None:
        self.__set(_command = CommonFanZA5.PhysicalControlLocked.physical_controls_locked, value=value)

    @property
    def brightness(self) -> int:
        return self.__get(_command = CommonFanZA5.IndicatorLight.brightness)
    
    @brightness.setter
    def brightness(self, value: int) -> None:
        if not (0 <= value <= 100):
            raise ValueError('Brightness must be between 0 and 100')
        self.__set(_command = CommonFanZA5.IndicatorLight.brightness, value=value)

    @property
    def alarm(self) -> bool:
        return self.__get(_command = CommonFanZA5.Alarm.alarm)
    
    @alarm.setter
    def alarm(self, value: bool) -> None:
        self.__set(_command = CommonFanZA5.Alarm.alarm, value=value)

    @property
    def battery_state(self) -> bool:
        return self.__get(_command = CommonFanZA5.CustomService.battery_state)

    @property
    def ac_state(self) -> bool:
        return self.__get(_command = CommonFanZA5.CustomService.ac_state)

    def move(self, value: Literal['left', 'right']) -> None:
        self.__set(_command = CommonFanZA5.CustomService.move, value=value)

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class FanZA5(ModelFanZA5):

    def __init__(self, object: MiotDevice) -> None:
        super().__init__(object=object)
        
        self.name = ' '.join(map(
            lambda x: x[0].upper() + x[1:],
            self.model.split('.')
        ))

        self._switches = [FanPowerSwitch, FanSwingModeSwitch, FanAnionSwitch, FanPyhsicalControlLockedSwitch, FanAlarmSwitch]
        self._buttons  = [FanMoveLeftButton, FanMoveRightButton]
        self._selects  = [FanSpeedLevelSelect] 
        self._numbers  = [FanSwingAngleNumber, FanSpeedPercentNumber, FanBrightnessNumber]
        self._sensors  = [FanSpeedRpmSensor, FanTempSensor, FanHumiditySensor, FanBatterySensor, FanAcStateSensor]

    def __entity(self, entity: list[any]):
        return list(map(
            lambda x: x(self),
            entity
        ))

    @property
    def switches(self):
        return self.__entity(self._switches)

    @property
    def buttons(self):
        return self.__entity(self._buttons)

    @property
    def selects(self):
        return self.__entity(self._selects)

    @property
    def numbers(self):
        return self.__entity(self._numbers)

    @property
    def sensors(self):
        return self.__entity(self._sensors)

    def power_on(self) -> None:
        self.power = True

    def power_off(self) -> None:
        self.power = False

    def swing_mode_on(self) -> None:
        self.swing_mode = True
    
    def swing_mode_off(self) -> None:
        self.swing_mode = False

    def anion_on(self) -> None:
        self.anion = True

    def anion_off(self) -> None:
        self.anion = False

    def physical_controls_locked_on(self) -> None:
        self.physical_controls_locked = True

    def physical_controls_locked_off(self) -> None:
        self.physical_controls_locked = False

    def alarm_on(self) -> None:
        self.alarm = True

    def alarm_off(self) -> None:
        self.alarm = False

    def move_left(self) -> None:
        self.move('left')
    
    def move_right(self) -> None:
        self.move('right')

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class FanPowerSwitch(SwitchEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Power {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._device.power

    def turn_on(self):
        self._device.power_on()

    def turn_off(self):
        self._device.power_off()

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_power"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:fan" if self.is_on else "mdi:fan-off"

class FanSwingModeSwitch(SwitchEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Swing Mode {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._device.swing_mode

    def turn_on(self):
        self._device.swing_mode_on()

    def turn_off(self):
        self._device.swing_mode_off()

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_swing_mode"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:sync" if self.is_on else "mdi:circle-outline"

class FanAnionSwitch(SwitchEntity):
    
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Anion {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._device.anion

    def turn_on(self):
        self._device.anion_on()

    def turn_off(self):
        self._device.anion_off()

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_anion"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:blur" if self.is_on else "mdi:blur-off"

class FanPyhsicalControlLockedSwitch(SwitchEntity):

    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Physical Control Locked {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._device.physical_controls_locked

    def turn_on(self):
        self._device.physical_controls_locked_on()

    def turn_off(self):
        self._device.physical_controls_locked_off()

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_physical_controls_locked"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:lock-outline" if self.is_on else "mdi:lock-open-variant-outline"

class FanAlarmSwitch(SwitchEntity):

    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Alarm {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._device.alarm

    def turn_on(self):
        self._device.alarm_on()

    def turn_off(self):
        self._device.alarm_off()

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_alarm"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:bell-outline" if self.is_on else "mdi:bell-off-outline"

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class FanMoveLeftButton(ButtonEntity):

    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Move Left {self._device.name}"

    @property
    def name(self):
        return self._name

    def press(self):
        self._device.move_left()

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_move_left"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:arrow-left"

class FanMoveRightButton(ButtonEntity):

    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Move Right {self._device.name}"

    @property
    def name(self):
        return self._name

    def press(self):
        self._device.move_right()

    def release(self):
        pass
    
    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_move_right"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

    @property
    def icon(self):
        return "mdi:arrow-right"

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class FanSpeedLevelSelect(SelectEntity):
    
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Speed Level {self._device.name}"
        self._options = list(map(str, self._device.lavels))
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def options(self) -> list:
        return self._options
    
    @property
    def current_option(self) -> str:
        return str(self._device.level)
    
    def select_option(self, option: str) -> None:
        self._device.level = int(option)

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_level"
    
    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class FanSwingAngleNumber(NumberEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Swing Angle {self._device.name}"
    
    @property
    def name(self):
        return self._name
    
    @property
    def native_value(self):
        return self._device.swing_angle
    
    @property
    def native_min_value(self):
        return 30

    @property
    def native_max_value(self):
        return 120
    
    @property
    def native_step(self):
        return 1
    
    @property
    def icon(self):
        return "mdi:arrow-left-right-bold"
    
    def set_native_value(self, value: float):
        _LOGGER.error("Swing angle: %s", value)
        self._device.swing_angle = int(value)

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_swing_angle"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

class FanSpeedPercentNumber(NumberEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Speed Control % {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._device.speed_procent

    def set_native_value(self, value: float):
        self._device.speed_procent = int(value)

    @property
    def native_unit_of_measurement(self):
        return "%"

    @property
    def native_min_value(self):
        return 0

    @property
    def native_max_value(self):
        return 100

    @property
    def icon(self):
        return "mdi:speedometer-medium"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_speed_procent"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

class FanBrightnessNumber(NumberEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Brightness {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._device.brightness

    def set_native_value(self, value: float):
        self._device.brightness = int(value)

    @property
    def native_unit_of_measurement(self):
        return "%"

    @property
    def native_min_value(self):
        return 0

    @property
    def native_max_value(self):
        return 100

    @property
    def icon(self):
        match value := self.native_value:
            case 0:
                return "mdi:lightbulb-off"
            case 100:
                return "mdi:lightbulb-on"
            case _:
                _value = min(90, max(10, round(value / 10) * 10))
                return f"mdi:lightbulb-on-{_value}"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_brightness"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class FanSpeedRpmSensor(SensorEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Speed RPM {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._device.speed_rpm

    @property
    def native_unit_of_measurement(self):
        return "RPM"

    @property
    def icon(self):
        return "mdi:fan"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_speed_rpm"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

class FanTempSensor(SensorEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Temp {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._device.temperature

    @property
    def native_unit_of_measurement(self):
        return "°C"

    @property
    def icon(self):
        return "mdi:thermometer"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_temperature"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}
    
class FanHumiditySensor(SensorEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Humidity {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._device.humidity

    @property
    def native_unit_of_measurement(self):
        return "%"

    @property
    def icon(self):
        return "mdi:water-percent"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_humidity"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}
    
class FanBatterySensor(SensorEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"Fan Battery State {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self) -> bool:
        return self._device.battery_state

    @property
    def icon(self):
        return "mdi:battery" if self.native_value else "mdi:battery-off"

    @property
    def device_class(self):
        return "battery"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_battery"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

class FanAcStateSensor(SensorEntity):
    def __init__(self, fan_device: FanZA5):
        self._device = fan_device
        self._name = f"AC Power {self._device.name}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self) -> bool:
        return self._device.ac_state

    @property
    def icon(self):
        return "mdi:power-plug-outline" if self.native_value else "mdi:power-plug-off-outline"

    @property
    def device_class(self):
        return "power"

    @property
    def unique_id(self):
        return f"{self._device.info.mac_address}_ac_state"

    @property
    def device_info(self):
        _LOGGER.error(f"ac_state: {self._device.ac_state} | DOMAIN: {DOMAIN} | mac_address: {self._device.info.mac_address}")
        return {"identifiers": {(DOMAIN, self._device.info.mac_address)}}

