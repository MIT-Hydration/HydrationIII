"""
rig_hardware.py
Hardware Interface and Mock Layers for Hydration project Rig subsystem.
"""

from abc import ABC, abstractmethod
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

class AbstractRigHardware(ABC):
    current_pos = [0, 0]
    
    def getPosition(self):
        return self.current_pos

    @abstractmethod
    def homeX(self):
        pass

    @abstractmethod
    def homeY(self):
        pass

    @abstractmethod
    def isXMoving(self):
        pass

    @abstractmethod
    def isYMoving(self):
        pass

    @abstractmethod
    def emergencyStop(self):
        pass

class MockRigHardware(AbstractRigHardware):
    
    def __init__(self):
        self.position = [50.0, 50.0]
        self.homing = [False, False]
        self.homingTime = [0.0, 0.0]
    
    def _update(self, i):
        VEL = -2 # cm/s
        if self.homing[i]:
            new_t = time.time()
            dt = new_t - self.homingTime[i]
            ds = VEL*dt
            s = self.position[i] + ds
            if s <= 0.0:
                self.homing[i] = False
                s = 0.0
            self.position[i] = s
            self.homingTime[i] = new_t
            
    def getPosition(self):
        self._update(0)
        self._update(1)
        return self.position

    def homeX(self):
        self.homing[0] = True
        self.homingTime[0] = time.time()
        
    def homeY(self):
        self.homing[1] = True
        self.homingTime[1] = time.time()
        
    def emergencyStop(self):
        self.homing[0] = False
        self.homing[1] = False

    def isXMoving(self):
        #print(f"X is moving {self.homing[0]}")
        return self.homing[0]

    def isYMoving(self):
        return self.homing[1]

class RigHardware(AbstractRigHardware):
    def homeX(self):
        pass

    def homeY(self):
        pass