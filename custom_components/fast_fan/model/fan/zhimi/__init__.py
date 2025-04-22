
from miio import MiotDevice

from custom_components.fast_fan.model.fan import Fan



class FanZhimi(Fan): 
    
    def __init__(self, object: MiotDevice) -> None:
        super().__init__(object)