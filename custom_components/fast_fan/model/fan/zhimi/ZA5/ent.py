from custom_components.fast_fan.model.fan.zhimi.ZA5 import FanZhimiZA5, switch


class FanEntity:
    def __init__(self, object: FanZhimiZA5) -> None:
        self.object = object
        self.object._entities.append[
            switch.FanPowerSwitch,
        ]
        self.upload_entities()

    def upload_entities(self):
        for entity in self._entities:
            entity(self)
    
