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
##use another GPIO     

# Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
SIG = config.getint('Tachometer', 'InputPin')  # Pin receiving the Hall Effect signal

if config.getboolean('Operating System', 'RunningInRPi'):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SIG, GPIO.IN)

class AbstractTachometer(ABC):

    @abstractmethod
    def get_rpm(self):
        pass

    # MAXSPEED (Percentage of the Max):
    def get_max_rpm(self):
        return 2000 ##not abstract bc known

class MockTachometer(AbstractTachometer):

    def get_rpm(self):
      return 500
    
class Tachometer(AbstractTachometer):
    speed_rpm = 0 
    MAX_RPM = 150
        
    class TachometerThread(threading.Thread):

        def __init__(self):
            self.N = config.getint('Tachometer', 'AveragingNumSamples')
            threading.Thread.__init__(self)
            self.stopped = True
            # to store data for 1 s at 1 ms sample time
            self.pulse_array = numpy.zeros(self.N, dtype=int)
            self.sampling_time = config.getfloat('Tachometer', 'SamplingTime')

        def run(self):
            self.stopped = False
            while not self.stopped:
                loop_start = time.time()
                v = GPIO.input(SIG)
                #print(v)
                #v = 0
                self.pulse_array = numpy.roll(self.pulse_array, -1)
                self.pulse_array[-1] = v
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < self.sampling_time):
                    time.sleep(self.sampling_time - delta_time)
                
        def stop(self):
            self.stopped = True

        def get_rpm(self):
            num_strips = config.getint("Tachometer", "NumStrips")
            array_shift = self.pulse_array[1:]
            array = self.pulse_array[0:-1]
            delta = array - array_shift
            count = numpy.count_nonzero(delta < 0.0)
            #print(count)
            PULSES_PER_REVOLUTION = num_strips
            ARRAY_TIME = self.N*self.sampling_time 
            revolutions_per_second = (count/PULSES_PER_REVOLUTION)/ARRAY_TIME
            revolutions_per_minute = revolutions_per_second * 60
            return revolutions_per_minute
    
    tachometer_thread = TachometerThread()
    
    def __init__(self):
        cls.tachometer_thread.start()
        
    def get_rpm(self):
        return cls.tachometer_thread.get_rpm()

      
