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
    from . import hx711

class AbstractWOB(ABC):

    @abstractmethod
    # returns a timestamped force reading
    def get_force_N(self):
        pass

class MockWOBSensor(AbstractWOB):

    def get_force_N(self):
      return [time.time(), -5.0]

if config.getboolean('Operating System', 'RunningInRPi'):

    class WOBThread(threading.Thread):

        def __init__(self): 
            self.DTPin = config.getint('WOBSensor', 'DTPin')
            self.SCKPin = config.getint('WOBSensor', 'SCKPin')
            self.wob_sensor = hx711.HX711(self.DTPin, self.SCKPin)
            self.referenceWOBUnit = \
                config.getfloat('WOBSensor', 'CalReading') / config.getfloat('WOBSensor', 'CalNewtons')
            self.wob_sensor.set_reading_format("MSB", "MSB")
            self.wob_sensor.set_reference_unit(self.referenceWOBUnit)
            self.wob_sensor.reset()
            self.wob_sensor.tare()
            self.sampling_time = config.getfloat('WOBSensor', 'SamplingTime')
            self.reading = 0.0
            self.last_reading = 0.0

            threading.Thread.__init__(self)
            self.stopped = True

        def run(self):
            self.stopped = False
            
            while not self.stopped:
                loop_start = time.time()
                self.reading = self.wob_sensor.get_weight(self.DTPin)
                loop_end = time.time()
                self.last_reading = loop_end
                delta_time = loop_end - loop_start
                if (delta_time < self.sampling_time):
                    time.sleep(self.sampling_time - delta_time)

        def stop(self):
            self.stopped = True

        def get_force_N(self):
            return [self.last_reading, self.reading]
        
        
   
    class WOBSensor(AbstractWOB):
            
        def __init__(self):
            self.sensor_thread = WOBThread()
            self.sensor_thread.start()

        def get_force_N(self):
            return self.sensor_thread.get_rpm()
        
    
