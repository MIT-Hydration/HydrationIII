
from time import sleep  # this lets us have a time delay
#import RPi.GPIO as GPIO

from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html


# Abstract Base Class


class AbstractPump(ABC):

    # class variables ?
    duration = 5000
    delay = 0.0000001
    max_speed= 18

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
    def set_speed_LpM(self, speedLpM_value):
        pass

    @abstractmethod
    def get_speed_LpM(self):
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
    def set_speed_PoM(self, speedPoM_value):
        pass

    @abstractmethod
    def get_speed_PoM(self):
        pass


# Child Class
class MockPump(AbstractPump):
    #To directly invoke a method from the abstract class super()._____
    # init method or "constructor" Dunder method
    def __init__(self, speedlpm, speedpom, direction):
        self.speedlpm = speedlpm
        self.speedpom = speedpom
        self.direction = direction


    def run(self):
        speedvalue= input("What speed ?")
        print(speedvalue)
        self.set_speed_LpM(speedvalue)
        print("speed set : ")
        print(self.speedlpm)

    # def set_direction_forward(cls):
    #     cls.get_direction=1
    #     pass
    #
    # def set_direction_reverse(cls):
    #     cls.direction = 0
    #     pass
    #
    # def get_direction(cls):
    #     return cls.__direction
    #     pass
    #     # SPEED (Liter per Minute):
    def set_speed_LpM(self, speedLpM_value):
        self.speedlpm = speedLpM_value
        pass

    def get_speed_LpM(self):
        return self.speedlpm


    # FILTER CLEANING SEQUENCE:
    def cleaning_sequence(self):
        pass

    # MAXSPEED (Percentage of the Max):

    def get_max_speed(self):
        pass


    def set_speed_PoM(self, speedPoM_value):
        self.speedpom = speedPoM_value
        pass

    def get_speed_PoM(self):
        return
        pass


class Pump(AbstractPump):

    # init method or "constructor"
    def __init__(self, speedlpm, speedpom, direction):
        self.speedlpm = speedlpm
        self.speedpom = speedpom
        self.direction = direction

    def run(self)
        GPIO.output(ENA, GPIO.LOW)
        self.set_direction_forward()
        # will be a while loop later probably
        for x in range(duration):
            GPIO.output(PUL, GPIO.HIGH)
            sleep(delay)
            GPIO.output(PUL, GPIO.LOW)
            sleep(delay)
        return


# The cls parameter is the class object, which allows @classmethod methods to easily instantiate the class, regardless of any inheritance going on.

# DIRECTIONS:
    @classmethod
    def set_direction_forward(cls):
        GPIO.output(DIR, GPIO.LOW)
        cls.direction = 1


    @classmethod
    def set_direction_reverse(cls):
        GPIO.output(DIR, GPIO.HIGH)
        cls.direction = 0


    @classmethod
    def get_direction(cls):
        return cls.direction
        pass

        # SPEED (Liter per Minute):


    # @classmethod
    # def set_speed_LpM(cls, speedLpM_value):
    #     speedLpM = speedLpM_value
    #     pass
    #
    #
    # @classmethod
    # def get_speed_LpM(cls):
    #     return speedLpM
    #     pass

    #Stop pump 5 sec, reverse pump 5 sec, stop pump 10 sec to let debris settle /
    #be diluted, normal pump 10 sec, reverse pump 5 sec, stop pump 5 sec, back to normal pumping
    # FILTER CLEANING SEQUENCE:
    @classmethod
    def cleaning_sequence(cls):
        pass


    # MAXSPEED (Percentage of the Max):
    # @classmethod
    # def get_max_speed(cls):
    #     return
    #     pass
    #
    #
    # @classmethod
    # def set_speed_PoM(cls, speedPoM_value):
    #     speedPoM = speedPoM_value
    #     pass
    #
    #
    # @classmethod
    # def get_speed_PoM(cls):
    #     return
    #     pass



Pump1=MockPump(1,1,1)
Pump1.run()
