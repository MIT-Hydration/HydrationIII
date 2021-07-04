"""
rig_hardware.py
Hardware Interface and Mock Layers for Hydration project Rig subsystem.
"""

from abc import ABC, abstractmethod
import configparser
import time, threading
import numpy, serial
import re

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from . import hardware

config = configparser.ConfigParser()
config.read('config.ini')

if config.getboolean('Operating System', 'RunningInRPi'):
    import HydrationServo
    from gpiozero import PWMLED
    from gpiozero import CPUTemperature
    import RPi.GPIO as GPIO
    
Z1Cal = config.getfloat('Rig', 'Z1Cal')
Z2Cal = config.getfloat('Rig', 'Z2Cal')
XCal = config.getfloat('Rig', 'XCal')
YCal = config.getfloat('Rig', 'YCal')
HomingError =config.getfloat('Rig', 'HomingError') 
iZ1 = 0
iZ2 = -1
iX = -2
iY = 1

class AbstractRigHardware(ABC):
    
    def isHomeZ1(self):
        current_pos = self.getPosition()
        return (not self.isZ1Moving()) \
            and (numpy.abs(current_pos[iZ1]) < HomingError) 

    def isHomeY(self):
        current_pos = self.getPosition()
        return (not self.isYMoving()) \
            and (numpy.abs(current_pos[iY]) < HomingError) 

    def movePositionZ1(self, delta):
        cur_pos = self.getPosition().copy()
        new_z1 = cur_pos[iZ1] + delta
        self.gotoPositionZ1(new_z1)
    
    def movePositionY(self, delta):
        cur_pos = self.getPosition().copy()
        new_y = cur_pos[iY] + delta
        self.gotoPositionY(new_y)
    
    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def homeY(self):
        pass

    @abstractmethod
    def homeZ1(self):
        pass

    
    @abstractmethod
    def isYMoving(self):
        pass

    @abstractmethod
    def isZ1Moving(self):
        pass

    @abstractmethod
    def emergencyStop(self):
        pass

    @abstractmethod
    # Returns torque of motor i (0, 1, 2, 3) => (z1, z2, x, y)
    def getTorque(self, i):
        pass

    @abstractmethod
    def setHomeZ1(self):
        pass
    
    @abstractmethod
    def setHomeY(self):
        pass

    @abstractmethod
    def gotoPositionY(self, y):        
        pass
    
    @abstractmethod
    def gotoPositionZ1(self, z):        
        pass

class MockRigHardware(AbstractRigHardware):
    def __init__(self):
        self.position = [-0.4, -0.0, 0.25, 0.50]
        self.homing = [False, False, False, False]
        self.homingTime = [0.0, 0.0, 0.0, 0.0]
        self.target = [0.0, 0.0, 0.0, 0.0]
        self.move_tolerance = config.getfloat(
            "Rig", "HomingError")
    
    def _update(self, i):
        VEL = (self.target[i] - self.position[i])*0.05 # m/s
        if self.homing[i]:
            new_t = time.time()
            dt = new_t - self.homingTime[i]
            ds = VEL*dt
            s = self.position[i] + ds
            ds = self.target[i] - s
            if numpy.abs(ds) <= self.move_tolerance*100:
                self.homing[i] = False
                s = self.target[i]
            self.position[i] = s
            self.homingTime[i] = new_t
            
    def getPosition(self):
        N = len(self.position)
        for n in range(N):
            self._update(n)
        return self.position

    def _home(self, i):
        self.homing[i] = True
        self.target[i] = 0.0
        self.homingTime[i] = time.time()

    def homeZ1(self):
        self._home(iZ1)
        
    def homeZ2(self):
        self._home(iZ2)
    
    def homeX(self):
        self._home(iX)
        
    def homeY(self):
        self._home(iY)
        
    def emergencyStop(self):
        N = len(self.position)
        for n in range(N):
            self.homing[n] = False

    def isZ1Moving(self):
        #print(f"X is moving {self.homing[0]}")
        return self.homing[0]

    def isZ2Moving(self):
        #print(f"X is moving {self.homing[0]}")
        return self.homing[1]
    
    def getTorque(self, i):
        return 9 # maximum is 3.5, so if we see more it indicates simulated value
      
    def isXMoving(self):
        #print(f"X is moving {self.homing[0]}")
        return self.homing[2]

    def isYMoving(self):
        return self.homing[3]

    def gotoPosition(self, x, y):
        t = time.time()
        self.target[2] = x
        self.target[3] = y
        self.homing[2] = True
        self.homingTime[2] = t
        self.homing[3] = True
        self.homingTime[3] = t
    
    def gotoPositionY(self, y):
        t = time.time()
        self.target[iY] = y
        self.homing[iY] = True
        self.homingTime[iY] = t

    def gotoPositionZ1(self, z): 
        self.target[iZ1] = z    
        self.homing[iZ1] = True
        self.homingTime[iZ1] = time.time()
        
    def gotoPositionZ2(self, z):
        self.target[1] = z        
        self.homing[1] = True
        self.homingTime[1] = time.time()

    def setHomeZ1(self):
        print("Setting Home Z1")
        self.position[iZ1] = 0.0

    def setHomeZ2(self):
        self.position[iZ2] = 0.0

    def setHomeX(self):
        self.position[iX] = 0.0

    def setHomeY(self):
        self.position[iY] = 0.0


class RigHardware(AbstractRigHardware):
    
    def __init__(self):
        print("Initializing Rig Hardware ...")
        self.current_pos = [0.0, 0.0, 0.0, 0.0]
        self.getPosition()
        print(f"Position found {self.current_pos}")
        self.prev_pos = self.current_pos.copy()
        self.move_tolerance = config.getfloat(
            "Rig", "HomingError")

    def gotoPositionY(self, y):
        # ensure Z-poisions are zero within tolerance
        pos = self.getPosition()
        if (numpy.abs(pos[iZ1]) > self.move_tolerance) or \
            (numpy.abs(pos[iY]) > self.move_tolerance):
            return
        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position(iY, y/YCal)
        
    def gotoPositionZ1(self, z):        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position(iZ1, z/Z1Cal)
        
    def homeY(self):
        self.gotoPositionY(0.0)

    def homeZ1(self):
        self.gotoPositionZ1(0.0)

    def getPosition(self):
        self.prev_pos = self.current_pos.copy()
        z1 = z2 = x = y = 0.0
        if iZ1 >= 0:
            z1 = HydrationServo.get_position(iZ1)*Z1Cal
        if iZ2 >= 0:
            z2 = HydrationServo.get_position(iZ2)*Z2Cal
        if iX >= 0:
            x = HydrationServo.get_position(iX)*XCal
        if iY >= 0:
            y = HydrationServo.get_position(iY)*YCal
        self.current_pos = numpy.array([z1, z2, x, y])
        return self.current_pos
        
    def emergencyStop(self):
        N = HydrationServo.get_num_motors()
        for n in range(N):
            HydrationServo.set_speed_rpm(n, 0)
        
    def isNMoving(self, n):   
        return numpy.abs(self.prev_pos[n] - self.current_pos[n]) > self.move_tolerance
    
    def isYMoving(self):
        if iY < 0:
            return False
        else:
            return self.isNMoving(iY)

    def isZ1Moving(self):
        if iZ1 < 0:
            return False
        else:
            return self.isNMoving(iZ1)

    def getTorque(self, i):
        return HydrationServo.get_torque(i)    
    
    def setHomeZ1(self):
        HydrationServo.set_home(iZ1)

    def setHomeY(self):
        HydrationServo.set_home(iY)