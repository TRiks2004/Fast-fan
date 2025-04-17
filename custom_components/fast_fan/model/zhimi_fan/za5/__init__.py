from dataclasses import dataclass
from typing import Literal
import logging
import time

from miio import MiotDevice
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.number import NumberEntity

from custom_components.fast_fan.const import DOMAIN 

_LOGGER = logging.getLogger(__name__)

@dataclass
class Command:
    siid: int
    piid: int

class CommonFanZA5:

    class Fan:
        power = Command(2, 1)             # +
        level = Command(2, 2)             # +
        swing_mode = Command(2, 3)        # +
        swing_mode_angle = Command(2, 5)  # +
        mode = Command(2, 7)              # TODO Not implemented
        power_off_time = Command(2, 10)   # TODO Not implemented
        anion = Command(2, 11)            # TODO Not implemented

    class CustomService:
        move = Command(6, 3)           # +
        speed_rpm = Command(6, 4)      # TODO Not implemented
        speed_procent = Command(6, 8)  # TODO Not implemented

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
                _LOGGER.error(f'Current value: {_value}')
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
        if not (30 <= value <= 120):
            raise ValueError('Angle must be between 30 and 120 degrees')
        
        self.__set(_command = CommonFanZA5.Fan.swing_mode_angle, value=value)

    @property
    def anion(self) -> bool:
        return self.__get(_command = CommonFanZA5.Fan.anion)
    
    @anion.setter
    def anion(self, value: bool) -> None:
        self.__set(_command = CommonFanZA5.Fan.anion, value=value)

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

        self._switches = [FanPowerSwitch, FanSwingModeSwitch, FanAnionSwitch]
        self._buttons  = [FanMoveLeftButton, FanMoveRightButton]
        self._selects  = [FanSpeedLevelSelect] 
        self._numbers  = [FanSwingAngleNumber]

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

    def power_on(self) -> None:
        self.power = True

    def power_off(self) -> None:
        self.power = False

    def swing_mode_on(self) -> None:
        self.swing_mode = True
    
    def swing_mode_off(self) -> None:
        self.swing_mode = False

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
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

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
        self._device.anion = True

    def turn_off(self):
        self._device.anion = False

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

    @property
    def icon(self):
        return "mdi:blur" if self.is_on else "mdi:blur-off"

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
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}