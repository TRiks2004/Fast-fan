from dataclasses import dataclass
from custom_components.fast_fan.model.spiid import SPIID

@dataclass(frozen=True)
class SPIIDFanXiaomiZA5:

    @dataclass(frozen=True)
    class Fan:
        siid               = 2
        power              = SPIID(siid,  1) # +
        level              = SPIID(siid,  2) # +
        swing_mode         = SPIID(siid,  3) # +
        swing_mode_angle   = SPIID(siid,  5) # +
        mode               = SPIID(siid,  7) # +
        power_off_time     = SPIID(siid, 10) # +
        anion              = SPIID(siid, 11) # +

    @dataclass(frozen=True)
    class CustomService:
        siid               = 6
        button_press       = SPIID(siid,  1) # ----
        battery_state      = SPIID(siid,  2) # +
        move               = SPIID(siid,  3) # +
        speed_rpm          = SPIID(siid,  4) # +
        ac_state           = SPIID(siid,  5) # +
        motor_status       = SPIID(siid,  6) # ?
        lp_enter_second    = SPIID(siid,  7) # ?
        speed_procent      = SPIID(siid,  8) # +
        country_code       = SPIID(siid,  9) # ----
        temp_sens          = SPIID(siid, 10) # ?

    @dataclass(frozen=True)
    class Environment:
        siid               = 7
        temperature        = SPIID(siid, 1) # +
        humidity           = SPIID(siid, 7) # +

    @dataclass(frozen=True)
    class PhysicalControlLocked:
        siid               = 3
        physical_controls_locked = SPIID(siid, 1)

    @dataclass(frozen=True)
    class IndicatorLight:
        siid               = 4
        brightness         = SPIID(siid, 3) # +

    @dataclass(frozen=True)
    class Alarm:
        siid               = 5
        alarm              = SPIID(siid, 1) # +

