from typing import Literal
import logging
import time

from miio import MiotDevice
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity

from custom_components.fast_fan.const import DOMAIN 

_LOGGER = logging.getLogger(__name__)

class FanZA5:
    model='zhimi.fan.za5'
    entities_name = 'zhimi fan za5'
    is_on = False

    def get_entities_switch(self):
        return [
            FanPowerSwitch(self.entities_name, self)
        ]

    def get_entities_button(self):
        return [
            FanMoveLeftButton(self.entities_name, self),
            FanMoveRightButton(self.entities_name, self)
        ]

    def __init__(self, object: MiotDevice) -> None:
        self.object = object
        
        self.is_on = self.get_power()

    def __set(
        self, 
        *,
        siid: int, piid: int,
        value: int | float | bool | str,        
        timeout: int = 1
    ) -> int | float | bool | str:
        self.object.set_property_by(
            siid=siid,
            piid=piid,
            value=value
        )
        time.sleep(timeout)
        return self.__get(siid=siid, piid=piid)

    def __get(
        self, 
        *,
        siid: int, piid: int,
        timeout: int = 3
    ) -> int | float | bool | str:
        get =  self.object.get_property_by(
            siid=siid,
            piid=piid
        )

        _LOGGER.error(f"get siid:{siid} piid:{piid} status:{get}")

        return get[0].get('value')

    def get_power(
        self, 
        *, 
        siid: int = 2, piid: int = 1
    ) -> bool:
        return self.__get(
            siid=siid,
            piid=piid
        )

    def __set_power(self, 
        value: bool, 
        *, 
        siid: int = 2, piid: int = 1
    ) -> bool:
        self.is_on = self.__set(
            siid=siid,
            piid=piid,
            value=value
        )

        return self.is_on

    def set_power_on(self) -> bool:
        return self.__set_power(value=True)

    def set_power_off(self) -> bool:
        return self.__set_power(value=False)

    def _move(self, 
        value: Literal['left', 'right'], *, 
        siid: int = 6, piid: int = 3
    ) -> None:
        self.__set(value=value, siid=siid, piid=piid)

    def set_move_left(self) -> None:
        self._move('left')
    
    def set_move_right(self) -> None:
        self._move('right')

class FanPowerSwitch(SwitchEntity):
    def __init__(self, id, fan_device: FanZA5):
        self._id = id
        self._device = fan_device
        self._name = f"Fan Power {self._id}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._device.is_on

    def turn_on(self):
        self._device.set_power_on()

    def turn_off(self):
        self._device.set_power_off()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

    @property
    def icon(self):
        # меняем иконку в зависимости от состояния вентилятора
        if self._device.is_on:
            return "mdi:fan"  # вентилятор включён
        else:
            return "mdi:fan-off"  # вентилятор выключен


class FanMoveLeftButton(ButtonEntity):

    def __init__(self, id, fan_device: FanZA5):
        self._id = id
        self._device = fan_device
        self._name = f"Fan Move Left {self._id}"

    @property
    def name(self):
        return self._name

    @property
    def enabled(self):
        return self._device.is_on

    def press(self):
        self._device.set_move_left()

    def release(self):
        pass

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

    @property
    def icon(self):
        return "mdi:arrow-left"


class FanMoveRightButton(ButtonEntity):

    def __init__(self, id, fan_device: FanZA5):
        self._id = id
        self._device = fan_device
        self._name = f"Fan Move Right {self._id}"

    @property
    def name(self):
        return self._name

    @property
    def enabled(self):
        return self._device.is_on

    def press(self):
        self._device.set_move_right()

    def release(self):
        pass

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._name.lower().replace(" ", "_"))}}

    @property
    def icon(self):
        return "mdi:arrow-right"
