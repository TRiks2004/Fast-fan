from homeassistant.core import HomeAssistant
import logging

from miio import MiotDevice

from .model.zhimi_fan.za5 import FanZA5


_LOGGER = logging.getLogger(__name__)

class Fan: 
    def __init__(
        self, 
        hass: HomeAssistant, 
        ip: str, token: str
    ) -> None:        
        self.hass:HomeAssistant = hass
        self._ip = ip
        self._token = token
        self.object = MiotDevice(ip=ip, token=token)

    def ppull_dataull_data(self):
        self.info = self.object.info().data

        match self.info['model']:
            case 'zhimi.fan.za5':
                self.devices = FanZA5(object=self.object)
                
        