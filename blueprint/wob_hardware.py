from time import sleep  # this lets us have a time delay
import time
from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html

import numpy

import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if config.getboolean('Operating System', 'RunningInRPi'):
    from gpiozero import PWMLED, DigitalInputDevice, DigitalOutputDevice
    import RPi.GPIO as GPIO

if config.getboolean('Operating System', 'RunningInCoreSensorsRPi'):
    import hx711
elif config.getboolean('WOBSensor', 'WOBZ1ConnectedToMotionControlRPi'):
    from . import hx711

class AbstractWOB(ABC):
    @abstractmethod
    # returns a timestamped force reading
    def get_force_N(self):
        pass
    
    def get_force_heater_N(self):
        pass

class MockWOBSensor(AbstractWOB):
    def get_force_N(self):
      return [time.time(), -5.0]

    def get_force_heater_N(self):
      return [time.time(), -15.0]


if config.getboolean('Operating System', 'RunningInCoreSensorsRPi') or \
   config.getboolean('WOBSensor', 'WOBZ1ConnectedToMotionControlRPi'):

    class WOBThread(threading.Thread):
        def __init__(self): 
            #self.DTPin = config.getint('WOBSensor', 'DTPin')
            #self.SCKPin = config.getint('WOBSensor', 'SCKPin')
            self.DTPinHeater = config.getint('WOBSensor', 'DTPinHeater')
            self.SCKPinHeater = config.getint('WOBSensor', 'SCKPinHeater')
            
            #self.wob_sensor = hx711.HX711(self.DTPin, self.SCKPin)
            self.wob_sensor_heater = hx711.HX711(self.DTPinHeater, self.SCKPinHeater)
            
            self.referenceWOBUnit = \
                config.getfloat('WOBSensor', 'CalReading') \
                    / config.getfloat('WOBSensor', 'CalNewtons')
            self.referenceWOBUnitHeater = \
                config.getfloat('WOBSensor', 'CalReadingHeater') \
                    / config.getfloat('WOBSensor', 'CalNewtonsHeater')
            
            # self.wob_sensor.set_reading_format("MSB", "MSB")
            # self.wob_sensor.set_reference_unit(self.referenceWOBUnit)
            # self.wob_sensor.reset()
            # self.wob_sensor.tare()
            self.wob_sensor_heater.set_reading_format("MSB", "MSB")
            self.wob_sensor_heater.set_reference_unit(self.referenceWOBUnit)
            self.wob_sensor_heater.reset()
            self.wob_sensor_heater.tare()
            
            self.sampling_time = config.getfloat('WOBSensor', 'SamplingTime')
            self.sensor_readings = {
                "time_s": 0.0,
                "wob_n": 0.0,  
                "wob_heater_n": 0.0, 
            }

            threading.Thread.__init__(self)
            self.stopped = True

        def run(self):
            self.stopped = False
            
            while not self.stopped:
                loop_start = time.time()
                #self.sensor_readings["wob_n"] = self.wob_sensor.get_weight(self.DTPin)
                self.sensor_readings["wob_n"] = 0
                
                self.sensor_readings["wob_heater_n"] = \
                    self.wob_sensor_heater.get_weight(self.DTPinHeater)
                #self.sensor_readings["wob_heater_n"] = 0
                loop_end = time.time()
                self.sensor_readings["time_s"] = loop_start
                delta_time = loop_end - loop_start
                if (delta_time < self.sampling_time):
                    time.sleep(self.sampling_time - delta_time)

        def stop(self):
            self.stopped = True

            
    class FileWriterThread(threading.Thread): 
        def __init__(self, WOB_thread):
            threading.Thread.__init__(self)
            self.WOB_thread = WOB_thread
            self.stopped = True
            
        def run(self):
            self.stopped = False
            time_start_s = time.time()
            fp = open(f"WOB_{time_start_s}.csv", "w")
            keys = self.WOB_thread.sensor_readings.keys()
            for k in keys:
                fp.write(f"{k},")
            fp.write("\n")
            sampling_time = config.getfloat("WOBSensor", "SamplingTime")
            
            while not self.stopped:
                loop_start = time.time()
                for k in keys:
                    fp.write(f"{self.WOB_thread.sensor_readings[k]},")
                fp.write("\n")
                loop_start_int = (int(loop_start))%10
                if loop_start_int == 0:
                    print(f"[t (s), WOB (N), WOBHEATER (N)] = "\
                          f"{self.WOB_thread.sensor_readings['time_s']}, "\
                          f"{self.WOB_thread.sensor_readings['wob_n']}," \
                          f"{self.WOB_thread.sensor_readings['wob_heater_n']}")
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < sampling_time):
                    time.sleep(sampling_time - delta_time)
            
            fp.close()
          
        def stop(self):
            self.stopped = True
        
    class WOBSensor(AbstractWOB):    
        def __init__(self):
            self.sensor_thread = WOBThread()
            self.file_writer_thread = FileWriterThread(self.sensor_thread)
            self.sensor_thread.start()
            self.file_writer_thread.start()

        def get_force_N(self):
            return [self.sensor_thread.sensor_readings["time_s"],
                    self.sensor_thread.sensor_readings["wob_n"]]

        def get_force_heater_N(self):
            return [self.sensor_thread.sensor_readings["time_s"],
                    self.sensor_thread.sensor_readings["wob_heater_n"]]
