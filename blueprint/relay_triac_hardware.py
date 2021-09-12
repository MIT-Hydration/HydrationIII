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

class AbstractRelayTriac(ABC):
    @abstractmethod
    # returns whether the heater is on or not
    def getHeater(self):
        pass
    
    @abstractmethod
    def setHeater(self, val):
        pass

    @abstractmethod    
    def getDrill(self):
        pass
    
    @abstractmethod
    def setDrill(self, val):
        pass
    
    @abstractmethod
    def getTraicLevel(self):
        pass

    @abstractmethod
    def setTraicLevel(self, val):
        pass

class MockRelayTriac(AbstractRelayTriac):

    def __init__(self):
        self.heater = False
        self.drill = False
        self.triacLevel = 0.0

    def getHeater(self):
        return self.heater
    
    def setHeater(self, val):
        if val:
            self.drill = False
        self.heater = val

    def getDrill(self):
        return self.drill
    
    def setDrill(self, val):
        if val:
            self.heater = False
        self.drill = val
    
    def getTraicLevel(self):
        return self.triacLevel

    def setTraicLevel(self, val):
        self.triacLevel = val
        
class FileWriterThread(threading.Thread): 
    def __init__(self, relay_traic):
        threading.Thread.__init__(self)
        self.relay_triac = relay_triac
        self.stopped = True
        
    def run(self):
        self.stopped = False
        time_start_s = time.time()
        fp = open(f"RelayTriac_{time_start_s}.csv", "w")
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
    
class RelayTriac(AbstractRelayTriac):    
    def __init__(self):
        self.file_writer_thread = FileWriterThread(self)
        self.file_writer_thread.start()

    def getHeater(self):
        return self.heater
    
    def setHeater(self, val):
        if val:
            self.drill = False
        self.heater = val

    def getDrill(self):
        return self.drill
    
    def setDrill(self, val):
        if val:
            self.heater = False
        self.drill = val
    
    def getTraicLevel(self):
        return self.triacLevel

    def setTraicLevel(self, val):
        self.triacLevel = val