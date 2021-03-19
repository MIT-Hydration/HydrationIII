
from time import sleep # this lets us have a time delay
import RPi.GPIO as GPIO


class AbstractPump:
#DIRECTIONS:    
    @abstractmethod
    def set_direction_forward():
        pass
      
    @abstractmethod
    def set_direction_reverse():
        pass

    @abstractmethod
    def get_direction():
        pass
      
#SPEED (Liter per Minute):
    @abstractmethod
    def set_speed_LpM(speedLpM_value):
        pass
      
    @abstractmethod
    def get_speed_LpM():
        pass
#FILTER CLEANING SEQUENCE:

    @abstractmethod
    def cleaning_sequence():
        pass
      
#MAXSPEED (Percentage of the Max):

    @abstractmethod
    def get_max_speed():
        pass

    @abstractmethod
    def set_speed_PoM(speedPoM_value):
        pass
      
     @abstractmethod
    def get_speed_PoM():
        pass


class MockPump(AbstractPump):
    
    def __init__():
        speedLpM.set_speed_LPM(0)
        speedPoM.set_speed_PoM(0)
        direction.set_direction_forward()
        
    @classmethod
    def cleaning_sequence():
        pass 
    
    
class Pump(AbstractPump):
    #DIRECTIONS:  
    @classmethod
    def set_direction_forward():
    GPIO.output(DIR, GPIO.LOW)
    direction=1 
    
    @classmethod
    def set_direction_reverse():
    GPIO.output(DIR, GPIO.HIGH)    
    direction=0
    
    
    @classmethod
    def get_direction():
        return direction
        pass         
   

   #SPEED (Liter per Minute):
    @classmethod
    def set_speed_LpM(speedLpM_value):
        speedLpM=speedLpM_value 
        
    @classmethod
    def get_speed_LpM():
        return speedLpM
        pass
      
    #FILTER CLEANING SEQUENCE:
    @classmethod
    def cleaning_sequence():
        pass
      
    #MAXSPEED (Percentage of the Max):
    @classmethod
    def get_max_speed():
        return 
        pass
    
    @classmethod
    def set_speed_PoM(speedPoM_value):
        speedPoM=speedPoM_value
        pass
      
     @classmethod
    def get_speed_PoM():
        return 
        pass

