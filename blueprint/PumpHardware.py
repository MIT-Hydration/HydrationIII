from time import sleep  # this lets us have a time delay
import time
from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html


import RPi.GPIO as GPIO

PUL = 17  # Stepper Drive Pulses
# Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
DIR = 27
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)


class AbstractPump(ABC):

    # DIRECTIONS:
    @abstractmethod
    def set_direction_forward(self):
        pass

    @abstractmethod
    def set_direction_reverse(self):
        pass

    @abstractmethod
    def get_direction(self):
        pass

    # SPEED (Liter per Minute):
    @abstractmethod
    def set_speed_lpm(self, speedlpm_value):
        pass

    @abstractmethod
    def get_speed_lpm(self):
        pass

    # FILTER CLEANING SEQUENCE:
    @abstractmethod
    def cleaning_sequence(self):
        pass

    # MAXSPEED (Percentage of the Max):
    @abstractmethod
    def get_max_speed(self):
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
        self.speedlpm = 0
        self.speedpom = 0
        self.direction = 0

    @staticmethod
    def run_pump():
        cycles = 1
        cyclecount = 0
        while cyclecount < cycles:
            for x in range(MockPump.duration):
                print("pulse high")
                sleep(MockPump.delay)
                print("pulse low")
                sleep(MockPump.delay)
                print(cyclecount)
                cyclecount = cyclecount + 1
        pass

    def set_direction_forward(self):
        self.direction = 1
        pass

    def set_direction_reverse(self):
        self.direction = 0
        pass

    def get_direction(self):
        return self.direction

    def set_speed_lpm(self, speedlpm_value):
        self.speedlpm = speedlpm_value
        pass

    def get_speed_lpm(self):
        return self.speedlpm

    # FILTER CLEANING SEQUENCE:

    def cleaning_sequence(self):
        pass

    # MAXSPEED (Percentage of the Max):

    def get_max_speed(self):
        pass

    def set_speed_pom(self, speedpom_value):
        self.speedpom = speedpom_value
        pass

    def get_speed_pom(self):
        return self.speedpom


class Pump(AbstractPump):
    duration = 400
    delay = 0.0000001

    def __init__(self):
        self.speedlpm = 0
        self.speedpom = 0
        self.direction = 0

    @staticmethod
    def run_pump():
        cycles = 20
        cyclecount = 0
        while cyclecount < cycles:
            GPIO.setup(ENA, GPIO.OUT)
            GPIO.output(ENA, GPIO.LOW)
            for x in range(Pump.duration):
                GPIO.output(PUL, GPIO.HIGH)
                sleep(Pump.delay)
                GPIO.output(PUL, GPIO.LOW)
                sleep(Pump.delay)
                cyclecount = (cyclecount + 1)
        GPIO.cleanup()

    # The cls parameter is the class object, which allows @classmethod methods to easily instantiate the class,
    # regardless of any inheritance going on.

    # DIRECTIONS:

    def set_direction_forward(self):
        GPIO.output(DIR, GPIO.LOW)
        self.direction = 1

    def set_direction_reverse(self):
        GPIO.output(DIR, GPIO.HIGH)
        self.direction = 0

    def get_direction(self):
        return self.direction

        # SPEED (Liter per Minute):

    def set_speed_lpm(self, speedlpm_value):
        self.speedlpm = speedlpm_value
        pass

    def get_speed_lpm(self):
        return self.speedlpm

    # Stop pump 5 sec, reverse pump 5 sec, stop pump 10 sec to let debris settle /
    # be diluted, normal pump 10 sec, reverse pump 5 sec, stop pump 5 sec, back to normal    pumping
    # FILTER CLEANING SEQUENCE:

    def cleaning_sequence(self):
        time.sleep(5)
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.set_direction_reverse()
            self.run_pump()
            if elapsed_time > seconds:
                print("Finished iterating in:" + str(int(elapsed_time)))
                break
        time.sleep(10)
        start_time = time.time()
        seconds = 10
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.set_direction_forward()
            self.run_pump()
            if elapsed_time > seconds:
                print("Finished iterating in:" + str(int(elapsed_time)))
                break
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.set_direction_reverse()
            self.run_pump()
            if elapsed_time > seconds:
                print("Finished iterating in:" + str(int(elapsed_time)))
                break
        time.sleep(5)

    # MAXSPEED (Percentage of the Max):

    def get_max_speed(self):
        # in rpm  or lpm? is it really needed? (limitation of the pump is 300 rpm)
        pass

    def set_speed_pom(self, speedpom_value):
        # delay for the setting 400 pulse/rev
        # to test
        if speedpom_value == 0:
            Pump.delay = 1
            self.speedpom = 0
        # 100 rpm
        if speedpom_value == 33:
            Pump.delay = 0.00063
            self.speedpom = 33
        # 200 rpm
        if speedpom_value == 66:
            Pump.delay = 0.000265
            self.speedpom = 66
        # 300 rpm
        if speedpom_value == 100:
            Pump.delay = 0.00015
            self.speedpom = 100

    def get_speed_pom(self):
        return self.speedpom

