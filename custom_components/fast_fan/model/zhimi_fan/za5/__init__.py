from dataclasses import dataclass
from typing import Literal
import logging
import time

from miio import MiotDevice
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.select import SelectEntity

from custom_components.fast_fan.const import DOMAIN 

_LOGGER = logging.getLogger(__name__)

@dataclass
class Command:
    siid: int
    piid: int

class CommonFanZA5:

    class Fan:
        power = Command(2, 1) # +
        level = Command(2, 2)
        swing_mode = Command(2, 3)
        swing_mode_angle = Command(2, 5)
        mode = Command(2, 7)
        power_off_time = Command(2, 10)
        anion = Command(2, 11)

    class CustomService:
        move = Command(6, 3) # +
        speed_rpm = Command(6, 4)
        speed_procent = Command(6, 8)

class ModelFanZA5:
    def __init__(self, object: MiotDevice) -> None:
        self.object = object

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
               
                if _value == value:
                    break
            except Exception as e:
                _LOGGER.error(e)
                break
            
        return _value

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

    def move(self, value: Literal['left', 'right']) -> None:
        self.__set(_command = CommonFanZA5.CustomService.move, value=value)


class FanZA5(ModelFanZA5):
    model='zhimi.fan.za5'
    
    lavels = [1, 2, 3, 4]

    def __init__(self, object: MiotDevice) -> None:
        super().__init__(object=object)
        
        self.name = ' '.join(map(
            lambda x: x[0].upper() + x[1:],
            self.model.split('.')
        ))

        self.switches = [FanPowerSwitch(self)]
        self.buttons  = [FanMoveLeftButton(self), FanMoveRightButton(self)]
        self.selects  = [FanSpeedLevelSelect(self)] 

    def power_on(self) -> None:
        self.power = True

    def power_off(self) -> None:
        self.power = False

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
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

    @property
    def icon(self):
        if self.is_on:
            return "mdi:fan"
        else:
            return "mdi:fan-off"

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
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

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
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

    @property
    def icon(self):
        return "mdi:arrow-right"

# # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

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

    