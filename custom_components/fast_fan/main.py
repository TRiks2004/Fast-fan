import time
from miio import MiotDevice

from typing import Literal

FAN_LEVEL = Literal[1, 2, 3, 4]



class Command:
    def __init__(self, siid, piid):
        self.siid = siid
        self.piid = piid

class FanCommand:
    power = Command(2, 1)
    level = Command(2, 2)
    swing_mode = Command(2, 3)
    swing_mode_angle = Command(2, 5)
    mode = Command(2, 7)
    power_off_time = Command(2, 10)
    anion = Command(2, 11)

class PhysicalControlLockedCommand:
    physical_controls_locked = Command(3, 1)

class IndicatorLightCommand:
    brightness = Command(4, 3)

class AlarmCommand:
    alarm = Command(5, 1)

class CustomServiceCommand:
    move = Command(6, 3)
    speed_rpm = Command(6, 4) 
    speed_procent = Command(6, 8)
    
class EnvironmentCommand:
    temperature = Command(7, 1)
    humidity = Command(7, 7)


class Fan:
    def __init__(self, ip, token):
        self.device = MiotDevice(
            ip=ip, 
            token=token
        )

    def command(
        self, 
        value: int | float | bool | str, 
        command: Command,
        *, 
        timeout: int = 3
    ):
        self.device.set_property_by(
            siid=command.siid,
            piid=command.piid,
            value=value,
        )

    def power(self, value: bool, command: Command = FanCommand.power):
        return self.command(value, command)

    def power_on(self):
        return self.power(True)

    def power_off(self):
        return self.power(False)
    
    def lavel(self, value: int, command: Command = FanCommand.level):
        # 1: Cлабый 
        # 2: Средний
        # 3: Быстрый
        # 4: Максимальный 
        return self.command(value, command)

    def swing_mode(self, value: bool, command: Command = FanCommand.swing_mode):
        return self.command(value, command)
    
    def swing_mode_on(self):
        return self.swing_mode(True)
    
    def swing_mode_off(self):
        return self.swing_mode(False)
    
    def swing_angle(self, value: int, command: Command = FanCommand.swing_mode_angle):
        if not (30 >= value <= 120):
            raise ValueError('Angle must be between 30 and 120 degrees')
        return self.command(value, command)

    def mode(self, value: int, command: Command = FanCommand.mode):
        # 0: Cтандартный 
        # 1: Природный
        return self.command(value, command)
    
    def anion(self, value: bool, command: Command = FanCommand.anion):
        return self.command(value, command)
    
    def anion_on(self):
        return self.anion(True)
    
    def anion_off(self):
        return self.anion(False)
    
    # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

    def move(self, value: Literal['left', 'right'], command: Command = CustomServiceCommand.move):
        return self.command(value, command)

    def move_left(self):
        return self.move('left')
    
    def move_right(self):
        return self.move('right')
    
    def speed_procent(self, value: int, command: Command = CustomServiceCommand.speed_procent):
        return self.command(value, command)

fan = Fan(
    ip='192.168.31.51', 
    token='a0dfd0f7f42ac0e9d1fef4b991558c40'
)

power = fan.device.get_property_by(siid=2, piid=5)
print(power)
# fan.turn_on()  # Включаем вентилятор
# time.sleep(5)  # Ждем 5 секунд
# fan.turn_off()  # Выключаем вентилятор