from ..hardware import HardwareFactory
import time

if __name__ == "__main__":
    pump = HardwareFactory.getWaterPump()
    pump.set_speed_pom(50)
    time.sleep(10)
    pump.set_speed_pom(0)