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
    def emergencyStop(self):
        pass

class MockRigHardware(AbstractRPiHardware):
    
    def __init__(self):
        self.position = [50.0, 50.0]
        self.homing = [False, False]
        self.homingTime = [0.0, 0.0]
    
    def _update(self, i):
        VEL = -10 # cm/s
        if self.homing[i]:
            dt = time.time() - self.homingTime[i]
            ds = VEL*dt
            s = self.position[i] + ds
            if s <= 0.0:
                self.homing[i] = False
                s = 0.0
            self.position[i] = s

    def getPosition(self):
        self._update(0)
        self._update(1)
        return self.current_pos

    def homeX(self):
        self.homing[0] = True
        self.homingTime[0] = time.time()
        
    def homeY(self):
        self.homing[1] = True
        self.homingTime[1] = time.time()
        
    def emergencyStop(self):
        self.homing[0] = False
        self.homing[1] = False

class RigHardware(AbstractRPiHardware):
    def homeX(self):
        pass

    def homeY(self):
        pass