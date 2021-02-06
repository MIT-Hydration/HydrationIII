"""
test-threading.py
Tests tachometer output
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "prakashm@alum.mit.edu"
__status__ = "Production"

import serial
import time
import re

class TachoTest:

    def __init__(self):
        self.port = serial.Serial("/dev/ttyACM0", baudrate=38400, timeout=3.0)
        rcv = self.port.readline()
        self.pattern = re.compile(r'TS = ([0-9]+) ms, TACHO = ([-0-9.]+) RPM, IMU = \(([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\) g')
        self.sensor_readings = {
                    "arduino_timestamp_ms": 0.0,
                    "tacho_rpm": 0.0,
                    "imu_x_g": 0.0,
                    "imu_y_g": 0.0,
                    "imu_z_g": 0.0,
                }
        
    def sensor_values(self):
        rcv = self.port.readline()
        m = self.pattern.match(rcv)
        if m is not None:    
            self.sensor_readings["arduino_timestamp_ms"] = int(m.group(1))
            self.sensor_readings["tacho_rpm"] =  float(m.group(2))
            self.sensor_readings["imu_x_g"] = float(m.group(3))
            self.sensor_readings["imu_y_g"] = float(m.group(4))
            self.sensor_readings["imu_z_g"] = float(m.group(5))
        return self.sensor_readings


if __name__ == "__main__":
    
    tacho = TachoTest()
    time_s = 0
    while time_s < 60:
        s = tacho.sensor_values()
        print(s)
        time.sleep(1)
        time_s += 1 

    
