from custom_components.fast_fan.model.fan.zhimi.za5 import FanZhimiZA5, switch, sensor


class FanEntity:
    def __init__(self, object: FanZhimiZA5) -> None:
        self.object = object

        entities = [
            switch.FanPowerSwitch, switch.FanSwingModeSwitch, switch.FanAnionSwitch, switch.FanPyhsicalControlLockedSwitch, switch.FanAlarmSwitch,
            sensor.FanSpeedRpmSensor, sensor.FanTempSensor, sensor.FanHumiditySensor, sensor.FanPowerSourceSensor,
        ]
        
        for obj in entities:
            self.object._entities.append(obj)
        
        self.upload_entities()

    def upload_entities(self):
        for entity in self.object._entities:
            entity(self.object)
    
