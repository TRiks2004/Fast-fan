from dataclasses import dataclass
from typing import Literal
from custom_components.fast_fan.model.fan.zhimi import FanZhimi
from miio import MiotDevice

from custom_components.fast_fan.model.spiid.fan_xiaomi_za5 import SPIIDFanXiaomiZA5

LAVELS = Literal[1, 2, 3, 4]
MODES = Literal[0, 1]
MOVE = Literal['left', 'right']

class EnvironmentFanZA5:
    is_power: bool
    is_swing_mode: bool
    is_anion: bool
    is_physical_controls_locked: bool
    is_alarm: bool

    power_source: str

    temperature: float
    humidity: int
    speed_rpm: int

    level: LAVELS
    swing_angle: int
    mode_name: str
    power_off_time: int
    speed_procent: int
    brightness: int

    def __init__(self, object: "FanZhimiZA5") -> None:
        self.object = object

    async def upload_data(self) -> None:
        self.is_power = await self.object.power
        self.is_swing_mode = await self.object.swing_mode
        self.is_anion = await self.object.anion
        self.is_physical_controls_locked = await self.object.physical_controls_locked
        self.is_alarm = await self.object.alarm

        self.power_source = await self.object.power_source

        self.temperature = await self.object.temperature
        self.humidity = await self.object.humidity
        self.speed_rpm = await self.object.speed_rpm

        self.level = await self.object.level
        self.swing_angle = await self.object.swing_angle
        self.mode_name = await self.object.mode_name
        self.power_off_time = await self.object.power_off_time
        self.speed_procent = await self.object.speed_procent
        self.brightness = await self.object.brightness

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    async def update_power(self):
        self.is_power = await self.object.power  

    async def update_swing_mode(self):
        self.is_swing_mode = await self.object.swing_mode

    async def update_anion(self):
        self.is_anion = await self.object.anion

    async def update_physical_controls_locked(self):
        self.is_physical_controls_locked = await self.object.physical_controls_locked

    async def update_alarm(self):
        self.is_alarm = await self.object.alarm

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    async def update_speed_rpm(self):
        self.speed_rpm = await self.object.speed_rpm

    async def update_battery_state(self):
        self.is_battery_state = await self.object.battery_state

    async def update_ac_state(self):
        self.is_ac_state = await self.object.ac_state

    async def update_power_source(self):
        self.power_source = await self.object.power_source

    async def update_temperature(self):
        self.temperature = await self.object.temperature

    async def update_humidity(self):
        self.humidity = await self.object.humidity



prefix_mdi = "mdi:"
@dataclass(frozen=True)
class Icon:

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @dataclass(frozen=True)
    class Power:
        on = f"{prefix_mdi}fan"
        off = f"{prefix_mdi}fan-off"
    
    @dataclass(frozen=True)
    class SwingMode:
        on = f"{prefix_mdi}autorenew"
        off = f"{prefix_mdi}autorenew-off"
    
    @dataclass(frozen=True)
    class Anion:
        on = f"{prefix_mdi}blur"
        off = f"{prefix_mdi}blur-off"
    
    @dataclass(frozen=True)
    class PhysicalControlsLocked:
        on = f"{prefix_mdi}lock-outline"
        off = f"{prefix_mdi}lock-open-variant-outline"

    @dataclass(frozen=True)
    class Alarm:
        on = f"{prefix_mdi}bell-outline"
        off = f"{prefix_mdi}bell-off-outline"
    
    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @dataclass(frozen=True)
    class SpeedRpm:
        off = f"{prefix_mdi}fan-off"
        
        fan_speed = 3
        fan_speed_1 = f"{prefix_mdi}fan-speed-1"
        fan_speed_2 = f"{prefix_mdi}fan-speed-2"
        fan_speed_3 = f"{prefix_mdi}fan-speed-3"

    @dataclass(frozen=True)
    class Humidity:
        water = f"{prefix_mdi}water-outline"

    @dataclass(frozen=True)
    class Temperature:
        thermometer = f"{prefix_mdi}thermometer-lines"

    @dataclass(frozen=True)
    class PowerSource:
        battery =    f"{prefix_mdi}battery-high"
        ac =         f"{prefix_mdi}power-plug-outline"
        battery_ac = f"{prefix_mdi}power-plug-battery-outline"

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

class FanZhimiZA5(FanZhimi):
    lavels_confines = (1, 2, 3, 4)
    swing_angle_confines = (30, 120)
    power_off_time_confines = (0, 36_000)
    speed_procent_confines = (0, 100)
    brightness_confines = (0, 100)
    
    mode_names = {
        1: "Стандартный",
        0: "Природный",
    }

    max_speed_rpm = 909

    def __init__(self, object: MiotDevice) -> None:
        super().__init__(object)
        self.name = "Fan Zhimi ZA5"
        self._entities = []
        self.environment = EnvironmentFanZA5(self)

        self._switchs_entities = [] 
        self._sensors_entities = []
    
    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #
    
    @property
    def switchs(self):
        return self._switchs_entities
    
    @property
    def sensors(self):
        return self._sensors_entities

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def power(self) -> bool:
        
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.power)

    @property
    def icon_power(self):
        return Icon.Power.on if self.environment.is_power else Icon.Power.off

    async def set_power(self, value: bool) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.Fan.power, value=value)

    async def set_power_on(self) -> None:
        await self.set_power(True)

    async def set_power_off(self) -> None:
        await self.set_power(False)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def level(self) -> LAVELS:
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.level)
    
    async def set_level(self, value: LAVELS) -> None:
        if value not in self.lavels_confines:
            raise ValueError(f"Level must be in {self.lavels_confines}; not {value}")
        await self._set(_command=SPIIDFanXiaomiZA5.Fan.level, value=value)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_swing_mode(self):
        return Icon.SwingMode.on if self.environment.is_swing_mode else Icon.SwingMode.off

    @property
    async def swing_mode(self) -> bool:
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.swing_mode)
    
    async def set_swing_mode(self, value: bool) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.Fan.swing_mode, value=value)
    
    async def set_swing_mode_on(self) -> None:
        await self.set_swing_mode(True)

    async def set_swing_mode_off(self) -> None:
        await self.set_swing_mode(False)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def swing_angle(self) -> int:
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.swing_mode_angle)
    
    async def set_swing_angle(self, value: int) -> None:
        if (
            (value < self.swing_angle_confines[0]) or 
            (value > self.swing_angle_confines[1])
        ):
            raise ValueError(
                "Swing angle must be between " + 
                f"{self.swing_angle_confines[0]} and " + 
                f"{self.swing_angle_confines[1]}; " + 
                f"current value: {value}"
            )
        await self._set(_command=SPIIDFanXiaomiZA5.Fan.swing_mode_angle, value=value)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def mode(self) -> MODES:
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.mode)
    
    async def set_mode(self, value: MODES) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.Fan.mode, value=value)

    @property
    async def mode_name(self) -> str:
        _mode = await self.mode
        mode_name = self.mode_names.get(_mode, None)
        if mode_name is None:
            raise Exception(f"Unknown mode: {_mode}")

        return mode_name 

    async def set_mode_name(self, value: str) -> None:
        _mode = self.mode_names.items()
        for _key, _value in _mode:
            if _value == value:
                await self.set_mode(_key)
                return
            
        raise Exception(f"Unknown mode name: {value}")

    async def set_mode_standart(self) -> None:
        await self.set_mode_name("Стандартный")

    async def set_mode_natural(self) -> None:
        await self.set_mode_name("Природный")
    
    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def power_off_time(self) -> int:
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.power_off_time)
    
    async def set_power_off_time(self, value: int) -> None:
        if (value < self.power_off_time_confines[0]) or (value > self.power_off_time_confines[1]):
            raise ValueError(
                "Power off time must be between " + 
                f"{self.power_off_time_confines[0]} and " + 
                f"{self.power_off_time_confines[1]}; " + 
                f"current value: {value}"
            )

        await self._set(_command=SPIIDFanXiaomiZA5.Fan.power_off_time, value=value)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_anion(self):
        return Icon.Anion.on if self.environment.is_anion else Icon.Anion.off

    @property
    async def anion(self) -> bool:
        return await self._get(_command=SPIIDFanXiaomiZA5.Fan.anion)
    
    async def set_anion(self, value: bool) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.Fan.anion, value=value)

    async def set_anion_on(self) -> None:
        await self.set_anion(True)

    async def set_anion_off(self) -> None:
        await self.set_anion(False)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def battery_state(self) -> bool:
        return await self._get(_command=SPIIDFanXiaomiZA5.CustomService.battery_state)

    @property
    async def ac_state(self):
        return await self._get(_command=SPIIDFanXiaomiZA5.CustomService.ac_state)
    
    @property
    async def power_source(self):
        battery = await self.battery_state
        ac = await self.ac_state
        if battery and not ac:
            return "battery"
        elif not battery and ac:
            return "ac"
        elif battery and ac:
            return "battery+ac"
        return "unknown"

    @property
    def icon_power_source(self):
        val = self.environment.power_source
        if val == "battery":
            return Icon.PowerSource.battery
        elif val == "ac":
            return Icon.PowerSource.ac
        elif val == "battery+ac":
            return Icon.PowerSource.battery_ac
        return "mdi:alert"

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    async def set_move(self, value: MOVE) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.CustomService.move, value=value)

    async def move_left(self) -> None:
        await self.set_move("left")

    async def move_right(self) -> None:
        await self.set_move("right")

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_speed_rpm(self):
        rpm = self.environment.speed_rpm

        if rpm == 0:
            return Icon.SpeedRpm.off
        
        icon = [(436, Icon.SpeedRpm.fan_speed_1), (731, Icon.SpeedRpm.fan_speed_2), (909 + 1, Icon.SpeedRpm.fan_speed_3)]

        step = self.max_speed_rpm / len(icon)

        for i, value in enumerate(icon):
            if rpm <= value[0]:
                return value[1]

    @property
    def unit_speed_rpm(self):
        return "RPM"

    @property
    async def speed_rpm(self) -> int:
        return await self._get(_command=SPIIDFanXiaomiZA5.CustomService.speed_rpm)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def speed_procent(self) -> int:
        return await self._get(_command=SPIIDFanXiaomiZA5.CustomService.speed_procent)
    
    async def set_speed_procent(self, value: int) -> None:
        if (value < self.speed_procent_confines[0]) or (value > self.speed_procent_confines[1]):
            raise ValueError(
                "Speed procent must be between " + 
                f"{self.speed_procent_confines[0]} and " + 
                f"{self.speed_procent_confines[1]}; " + 
                f"current value: {value}"
            )
        
        await self._set(_command=SPIIDFanXiaomiZA5.CustomService.speed_procent, value=value)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_temperature(self):
        return Icon.Temperature.thermometer

    @property
    async def temperature(self) -> float:
        return await self._get(_command=SPIIDFanXiaomiZA5.Environment.temperature)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_humidity(self):
        return Icon.Humidity.water

    @property
    async def humidity(self) -> float:
        return await self._get(_command=SPIIDFanXiaomiZA5.Environment.humidity)
    
    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_physical_controls_locked(self):
        return Icon.PhysicalControlsLocked.on if self.environment.is_physical_controls_locked else Icon.PhysicalControlsLocked.off

    @property
    async def physical_controls_locked(self) -> bool:
        return await self._get(_command=SPIIDFanXiaomiZA5.PhysicalControlLocked.physical_controls_locked)
    
    async def set_physical_controls_locked(self, value: bool) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.PhysicalControlLocked.physical_controls_locked, value=value)

    async def set_physical_controls_locked_on(self) -> None:
        await self.set_physical_controls_locked(True)

    async def set_physical_controls_locked_off(self) -> None:
        await self.set_physical_controls_locked(False)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    async def brightness(self) -> int:
        return await self._get(_command=SPIIDFanXiaomiZA5.IndicatorLight.brightness)
    
    async def set_brightness(self, value: int) -> None:
        if (value < self.brightness_confines[0]) or (value > self.brightness_confines[1]):
            raise ValueError(
                "Brightness must be between " + 
                f"{self.brightness_confines[0]} and " + 
                f"{self.brightness_confines[1]}; " + 
                f"current value: {value}"
        )
        await self._set(_command=SPIIDFanXiaomiZA5.IndicatorLight.brightness, value=value)

    # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- # ---- # -- #

    @property
    def icon_alarm(self):
        return Icon.Alarm.on if self.environment.is_alarm else Icon.Alarm.off

    @property
    async def alarm(self) -> bool:
        return await self._get(_command=SPIIDFanXiaomiZA5.Alarm.alarm)
    
    async def set_alarm(self, value: bool) -> None:
        await self._set(_command=SPIIDFanXiaomiZA5.Alarm.alarm, value=value)

    async def set_alarm_on(self) -> None:
        await self.set_alarm(True)

    async def set_alarm_off(self) -> None:
        await self.set_alarm(False)
