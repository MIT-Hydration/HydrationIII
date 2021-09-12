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
    
PUL = 13  # Stepper Drive Pulses to GPIO 13 (PWM-1)
# Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
DIR = 27
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
SIG = 26  # Pin receiving the Hall Effect signal

if config.getboolean('Operating System', 'RunningInRPi') \
    and not config.getboolean('Operating System', 'RunningInCoreSensorsRPi'):
    GPIO.setmode(GPIO.BCM)

    #GPIO.setup(PUL, GPIO.OUT)
    #GPIO.setup(DIR, GPIO.OUT)
    #GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(SIG, GPIO.IN)

class PumpMode:
    MANUAL = 0  # manually set speed, direction, cleaning sequence, stop
    AUTOMATIC = 1  # run continuously, clean if required, stop

    # when starting manual mode from automatic, always start from 0 speed (stop)
    # emergency stop is always possible, and returns to manual mode


class AbstractPump(ABC):

    # @abstractmethod
    # def emergency_stop(self):
    #     pass

    # @abstractmethod
    # def get_flow_mlps(self):
    #     pass

    # DIRECTIONS:
    @abstractmethod
    def set_direction(self, direction):
        pass

    @abstractmethod
    def get_direction(self):
        pass

    # SPEED (Milli-liter per seconds):
    @abstractmethod
    def set_speed_lpm(self, speed_lpm):
        pass

    @abstractmethod
    def get_speed_lpm(self):
        pass

    # @abstractmethod
    # def get_mode(self):
    #     pass
    #
    # @abstractmethod
    # def set_mode(self, mode):
    #     pass

    # FILTER CLEANING SEQUENCE:
    # @abstractmethod
    # def cleaning_sequence(self):
    #     pass

    # MAXSPEED (Percentage of the Max):
    @abstractmethod
    def get_max_speed_rpm(self):
        pass

    @abstractmethod
    def set_speed_pom(self, speedpom_value):
        pass

    @abstractmethod
    def get_speed_pom(self):
        pass

class MockPump(AbstractPump):
    duration = 400
    delay = 0.0000001

    def __init__(self):
        self.speedmlps = 0
        self.speedpom = 0
        self.direction = 0

    @staticmethod
    def run_pump():
        pass

    def set_direction(self, direction):
        pass

    # def set_direction_forward(self):
    #     self.direction = 1
    #     pass
    #
    # def set_direction_reverse(self):
    #     self.direction = 0
    #     pass

    def get_direction(self):
        return self.direction

    def set_speed_mlps(self, speedmlps_value):
        self.speedmlps = speedmlps_value
        pass

    def get_speed_mlps(self):
        return self.speedmlps

    # FILTER CLEANING SEQUENCE:

    def cleaning_sequence(self):
        pass

    # MAXSPEED (Percentage of the Max):

    def get_max_speed(self):
        pass

    def set_speed_pom(self, speedpom_value):
        self.speedpom = speedpom_value
        print(f"Setting Mock Speed to {speedpom_value} % of Max")
        pass

    def get_speed_pom(self):
        return self.speedpom

    def set_sensor(self):
        pass

    def add_flow(self):
        pass

    # def get_mode(self):
    #     pass
    #
    # def set_mode(self, mode):
    #     pass

class Pump(AbstractPump):
    duration = 400
    delay = 0.0000001
    if config.getboolean('Operating System', 'RunningInRPi'):
        pump_pwm = PWMLED(PUL)
    speed_rpm = 0
    MAX_RPM = 250
    MOTOR_PULSES_PER_REV = 400
    LITERS_PER_REV = 0.055
    if config.getboolean('Operating System', 'RunningInRPi'):
        direction_pin = DigitalOutputDevice(DIR)
        
    class FlowSensorThread(threading.Thread):
        N = 1000

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = True
            # to store data for 1 s at 1 ms sample time
            self.pulse_array = numpy.zeros(self.N, dtype=int)

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
                if (delta_time < 0.001):
                    time.sleep(0.001 - delta_time)
                
        def stop(self):
            self.stopped = True

        def get_flow_rate_lpm(self):
            array_shift = self.pulse_array[1:]
            array = self.pulse_array[0:-1]
            delta = array - array_shift
            count = numpy.count_nonzero(delta < 0.0)
            #print(count)
            PULSES_PER_LITER = 10500.0
            ARRAY_TIME = 1 # second
            liters_per_second = (count/PULSES_PER_LITER)/ARRAY_TIME
            liters_per_minute = liters_per_second * 60
            print(liters_per_minute)
            return liters_per_minute
    
    sensor_thread = FlowSensorThread()
    
    
    def set_direction(self, direction):
        if direction == 1:
            self.direction_pin.value = 1
            self.direction = 1
        if direction == 0:
            self.direction_pin.value = 0
            self.direction = 0

    def get_direction(self):
        return self.direction

    # SPEED (Liter per Minute):
    def set_speed_lpm(self, speed_lpm):
        self.set_speed_rpm(speed_lpm / self.LITERS_PER_REV)

    def get_speed_lpm(self):
        return self.speed_rpm * self.LITERS_PER_REV

    def get_max_speed_rpm(self):
        return 240

    def __init__(self):
        self.pump_pwm.value = 0.0
        self.set_direction(1)
        self.sensor_thread.start()

    def set_speed_pom(self, speedpom):
        if speedpom>0:
            self.set_direction(1)
            speed_rpm = speedpom*self.MAX_RPM/100
            self.set_speed_rpm(speed_rpm)            
        elif speedpom<0:
            self.set_direction(0)
            speed_rpm = -1*speedpom*self.MAX_RPM/100
            self.set_speed_rpm(speed_rpm)
    
    def set_speed_rpm(self, speed_rpm):
        self.speed_rpm = speed_rpm
        if speed_rpm < 1.0:
            self.pump_pwm.value = 0.0
            self.speed_rpm = 0
        else:
            PULSE_PER_REV = 400.0
            speed_rps = speed_rpm/60.0
            pulse_per_second = speed_rps*self.MOTOR_PULSES_PER_REV
            self.pump_pwm.frequency = pulse_per_second
            self.pump_pwm.value = 0.2

    def get_speed_rpm(self):
        return self.speed_rpm

    def get_speed_pom(self):
        return (self.speed_rpm/self.MAX_RPM)*100

    def get_flow_rate_lpm(self):
        return self.sensor_thread.get_flow_rate_lpm()
