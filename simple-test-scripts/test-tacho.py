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
        self.port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1,
                bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE)
        self.pattern = re.compile(b'TS = ([0-9]+) ms, TACHO = ([-0-9.]+) RPM, IMU = \(([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\) g')
        self.sensor_readings = {
                    "arduino_timestamp_ms": 0.0,
                    "tacho_rpm": 0.0,
                    "imu_x_g": 0.0,
                    "imu_y_g": 0.0,
                    "imu_z_g": 0.0,
                }
        self.arduino_primed = False

    def sensor_values(self):
        if not self.arduino_primed:
            self.port.flush()
            self.port.write(b"START_STREAM\n")
        str_rcv = self.port.readline()
        print(str_rcv)
        m = self.pattern.match(str_rcv)
        if m is not None:
            self.sensor_readings["arduino_timestamp_ms"] = int(m.group(1))
            self.sensor_readings["tacho_rpm"] =  float(m.group(2))
            self.sensor_readings["imu_x_g"] = float(m.group(3))
            self.sensor_readings["imu_y_g"] = float(m.group(4))
            self.sensor_readings["imu_z_g"] = float(m.group(5))
            self.arduino_primed = True
        return self.sensor_readings


if __name__ == "__main__":

    tacho = TachoTest()
    time_s = 0

    time_start_s = time.time()

    tach_fp = open(f"{time_start_s}_tachmoeter.csv", "w")
    tach_fp.write("time_s,arduino_timestamp_ms,tacho_rpm,imu_x_g,imu_y_g,imu_z_g")

    while time_s < 600:
        s = tacho.sensor_values()
        abs_time_s = time.time()
        tach_fp.write(f"{abs_time_s},")
        for k in s.sensor_readings:
            tach_fp.write(f"{k},")
        tach_fp.write(f"\n")
        print(s)
        time.sleep(0.01)
        time_s += 0.01
