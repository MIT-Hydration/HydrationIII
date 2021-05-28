from ..hardware import HardwareFactory
import time

if __name__ == "__main__":
    pump = HardwareFactory.getWaterPump()   
    for i in range(10): 
        pump.set_direction(0)
        pump.set_speed_pom(100)
        time.sleep(1)
    pump.set_speed_rpm(0)

    
