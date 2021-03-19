
from time import sleep # this lets us have a time delay
import RPi.GPIO as GPIO

from abc import ABC, abstractmethod #https://docs.python.org/3/library/abc.html

duration = 5000
delay = 0.0000001


class AbstractPump(ABC):
    
    #DIRECTIONS:    
    @abstractmethod
    def set_direction_forward(self):
        pass
      
    @abstractmethod
    def set_direction_reverse(self):
        pass

    @abstractmethod
    def get_direction(self):
        pass
      
    #SPEED (Liter per Minute):
    @abstractmethod
    def set_speed_LpM(self,speedLpM_value):
        pass
      
    @abstractmethod
    def get_speed_LpM(self):
        pass
    
    #FILTER CLEANING SEQUENCE:
    @abstractmethod
    def cleaning_sequence(self):
        pass
      
    #MAXSPEED (Percentage of the Max):
    @abstractmethod
    def get_max_speed(self):
        pass

    @abstractmethod
    def set_speed_PoM(self,speedPoM_value):
        pass
      
     @abstractmethod
    def get_speed_PoM(self):
        pass


class MockPump(AbstractPump):
    
    # init method or "constructor"
    def __init__(self, speedLpM,speedPoM, direction):
        self.set_speed_LPM(0)
        self.set_speed_PoM(0)
        self.set_direction_forward()
        
    @classmethod
    def cleaning_sequence():
        #does nothing
        pass 
    
    
class Pump(AbstractPump):
    
    # init method or "constructor"
    def __init__(self, speedLpM,speedPoM, direction):
        self.set_speed_LPM(speedLpM)
        self.set_speed_PoM(speedPoM)
        self.set_direction_forward()
        
    
    def run(self)
        GPIO.output(ENA, GPIO.LOW)
        #self.set_direction_ .....
           if direction ==1
              print("The pump is going forward")
           if direction ==0
              print("The pump is going backward")

        #will be a while loop later probably
           for x in range(duration): 
                GPIO.output(PUL, GPIO.HIGH)
                sleep(delay)
                GPIO.output(PUL, GPIO.LOW)
                sleep(delay)
           return

   #def stop() ?
   
    
    #The cls parameter is the class object, which allows @classmethod methods to easily instantiate the class, regardless of any inheritance going on.
    
    #DIRECTIONS:  
    @classmethod
    def set_direction_forward(cls):
        GPIO.output(DIR, GPIO.LOW)
        direction=1 
    
    @classmethod
    def set_direction_reverse(cls):
        GPIO.output(DIR, GPIO.HIGH)    
        direction=0
    
    
    @classmethod
    def get_direction(cls):
        return cls.direction
        pass         
   

   #SPEED (Liter per Minute):
    @classmethod
    def set_speed_LpM(cls,speedLpM_value):
        speedLpM=speedLpM_value 
        pass
        
    @classmethod
    def get_speed_LpM(cls):
        return speedLpM
        pass
      
    #FILTER CLEANING SEQUENCE:
    @classmethod
    def cleaning_sequence(cls):
        pass
      
    #MAXSPEED (Percentage of the Max):
    @classmethod
    def get_max_speed(cls):
        return 
        pass
    
    @classmethod
    def set_speed_PoM(cls,speedPoM_value):
        speedPoM=speedPoM_value
        pass
      
     @classmethod
    def get_speed_PoM(cls):
        return 
        pass

