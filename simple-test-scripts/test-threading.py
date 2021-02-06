"""
test-threading.py
Test threading concept
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "prakashm@alum.mit.edu"
__status__ = "Production"

from abc import ABC, abstractmethod
import time
import threading
import random

class AbstractDrill(ABC):

    @abstractmethod
    def start_sensor_readings(cls):
        pass

    @abstractmethod
    def start_sensor_readings(cls):
        pass
    
    @abstractmethod
    def set_drill_level(self, level):
        pass

    @abstractmethod
    def get_drill_level(self, level):
        pass

    @abstractmethod
    def get_speed_rpm(self):
        pass

    @abstractmethod
    def get_active_power_W(self):
        pass

    @abstractmethod
    def get_current_mA(self):
        pass
    
class Drill(AbstractDrill):

    class DrillPowerMeterThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = True
            self.sensor_readings = {
                    "active_power_W": 0.0,
                    "current_mA": 0.0,
                    "speed_rpm": 0.0,
                    "accel_x_g": 0.0,
                    "accel_y_g": 0.0,
                    "accel_z_g": 0.0,
                }
            
        def run(self):
            self.stopped = False
            while not self.stopped:
                loop_start = time.time()
                for k in self.sensor_readings:
                    self.sensor_readings[k] = random.random()
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.01):
                    time.sleep(0.01 - delta_time)
                
        def stop(self):
            self.stopped = True

    class FileWriterThread(threading.Thread):

        def __init__(self, drill_pm_thread):
            self.delay = 0.0027856988543367034
            self.sample_time = 0.02
            self.sleep_time = self.sample_time - self.delay
            threading.Thread.__init__(self)
            self.drill_pm_thread = drill_pm_thread
            self.stopped = True
            
        def run(self):
            self.stopped = False
            time_start_s = time.time()
            fp = open(f"{time_start_s}.csv", "w")
            fp.write("time_s,")
            for k in self.drill_pm_thread.sensor_readings:
                fp.write(f"{k},")
            fp.write("\n")
            while not self.stopped:
                loop_start = time.time()
                fp.write(f"{loop_start},")
                for k in self.drill_pm_thread.sensor_readings:
                    fp.write(f"{self.drill_pm_thread.sensor_readings[k]},")
                fp.write("\n")
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < self.sleep_time):
                    time.sleep(self.sleep_time - delta_time)

            fp.close()
                
        def stop(self):
            self.stopped = True
            
    drill_pm_thread = DrillPowerMeterThread()
    writer_thread = FileWriterThread(drill_pm_thread)
    
    @classmethod
    def start_sensor_readings(cls):
        cls.drill_pm_thread.start()
        cls.writer_thread.start()

    @classmethod
    def stop_sensor_readings(cls):
        cls.drill_pm_thread.stop()
        cls.writer_thread.stop()

    @classmethod
    def set_drill_level(cls, level):
        cls.motor.value = level

    @classmethod
    def get_drill_level(cls, level):
        return cls.motor.value

    @classmethod
    def get_speed_rpm(cls):
        return cls.drill_pm_thread.sensor_readings["speed_rpm"]
        pass

    @classmethod
    def get_active_power_W(cls):
        return cls.drill_pm_thread.sensor_readings["active_power_W"]
    
    @classmethod
    def get_current_mA(cls):
        return cls.drill_pm_thread.sensor_reading["current_mA"]


if __name__ == "__main__":
    drill = Drill()
    drill.start_sensor_readings()
    time.sleep(600)
    drill.stop_sensor_readings()