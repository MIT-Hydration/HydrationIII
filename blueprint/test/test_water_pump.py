from ..hardware import HardwareFactory
import time

if __name__ == "__main__":
    pump = HardwareFactory.getWaterPump()
    pump.set_speed_rpm(50)
    for i in range(180):
        print(f'Pump Speed = {pump.get_speed_rpm()} RPM,'\
               ' Flow = {pump.get_flow_rate_lpm()} LPM')
        time.sleep(1)
    pump.set_speed_rpm(0)