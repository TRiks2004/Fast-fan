from custom_components.fast_fan.model import Device
from miio import MiotDevice

class Fan(Device): 
    
    def __init__(self, object: MiotDevice) -> None:
        super().__init__(object)
