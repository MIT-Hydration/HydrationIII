from time import sleep  # this lets us have a time delay
import time
from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html

import numpy

import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if config.getboolean('Operating System', 'RunningInRPi'):
    from gpiozero import PWMLED, DigitalOutputDevice
    
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
    def getTriacLevel(self):
        pass

    @abstractmethod
    def setTriacLevel(self, val):
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
    
    def getTriacLevel(self):
        return self.triacLevel

    def setTriacLevel(self, val):
        self.triacLevel = val
        
class FileWriterThread(threading.Thread): 
    def __init__(self, relay_triac):
        threading.Thread.__init__(self)
        self.relay_triac = relay_triac
        self.stopped = True
        
    def run(self):
        self.stopped = False
        time_start_s = time.time()
        fp = open(f"RelayTriac_{time_start_s}.csv", "w")
        keys = ["time_s", "triac_level", "drill", "heater"]
        for k in keys:
            fp.write(f"{k},")
        fp.write("\n")
        sampling_time = config.getfloat("RelayAndTriac", "SamplingTime")
        
        while not self.stopped:
            loop_start = time.time()
            fp.write(f"{loop_start},{self.relay_triac.getTriacLevel()}," \
                     f"{self.relay_triac.getDrill()},{self.relay_triac.getHeater()}\n")
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

        self.triac = PWMLED(config.getint('RelayAndTriac', 'TriacGPIOPin'))
        self.drill = DigitalOutputDevice(config.getint('RelayAndTriac', 'DrillRelayPin'))
        self.heater = DigitalOutputDevice(config.getint('RelayAndTriac', 'HeaterRelayPin'))
        self.triac.value = 0.0
        self.drill.off()
        self.heater.off()
        print("Finished initializing RelayTriac...")

    def getHeater(self):
        return self.heater.value
    
    def setHeater(self, val):
        if val:
            self.drill.off()
            self.heater.on()
        else:
            self.heater.off()

    def getDrill(self):
        return False #self.drill.value
    
    def setDrill(self, val):
        if val:
            self.drill.on()
            self.heater.off()
        else:
            self.heater.on()

    def getTriacLevel(self):
        return 0.0 #self.triac.value

    def setTriacLevel(self, val):
        self.triac.value = val