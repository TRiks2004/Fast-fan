from custom_components.fast_fan.command import Command

class CommonFanZA5:

    class Fan:
        power = Command(2, 1)
        level = Command(2, 2)
        swing_mode = Command(2, 3)
        swing_mode_angle = Command(2, 5)
        mode = Command(2, 7)
        power_off_time = Command(2, 10)
        anion = Command(2, 11)

    class CustomService:
        button_press    = Command(6, 1) # not working
        battery_state   = Command(6, 2) 
        move            = Command(6, 3) # immplemented
        speed_rpm       = Command(6, 4) # immplemented
        ac_state        = Command(6, 5) 
        motor_status    = Command(6, 6)
        lp_enter_second = Command(6, 7)
        speed_procent   = Command(6, 8) # immplemented
        country_code    = Command(6, 9)
        temp_sens       = Command(6, 10) # immplemented

    class Environment:
        temperature = Command(7, 1)
        humidity = Command(7, 7)

    class PhysicalControlLocked:
        physical_controls_locked = Command(3, 1)

    class IndicatorLight:
        brightness = Command(4, 3)
    
    class Alarm:
        alarm = Command(5, 1)