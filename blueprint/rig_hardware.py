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
    
if not config.getboolean('Operating System', 'RunningInCoreSensorsRPi'):
    import HydrationServo

if config.getboolean('Operating System', 'RunningInRPi'):
    from gpiozero import PWMLED
    from gpiozero import CPUTemperature
    import RPi.GPIO as GPIO
    
Z1Cal = config.getfloat('Rig', 'Z1Cal')
Z2Cal = config.getfloat('Rig', 'Z2Cal')
XCal = config.getfloat('Rig', 'XCal')
YCal = config.getfloat('Rig', 'YCal')
HomingError =config.getfloat('Rig', 'HomingError') 

if config.getboolean('Mocks', 'MockRig'):
    iZ1 = 0
    iZ2 = 1
    iX = 2
    iY = 3
else:
    iZ1 = 0
    iZ2 = 1
    iX = -1
    iY = 2

NMotors = 3

# these indices are used for the current position variables
kZ1 = 0
kZ2 = 1
kX = 2
kY = 3

class AbstractRigHardware(ABC):
    
    def isHomeZ1(self):
        current_pos = self.getPosition()
        return (not self.isZ1Moving()) \
            and (numpy.abs(current_pos[kZ1]) < HomingError) 

    def isHomeY(self):
        current_pos = self.getPosition()
        return (not self.isYMoving()) \
            and (numpy.abs(current_pos[kY]) < HomingError) 

    def isHomeZ2(self):
        current_pos = self.getPosition()
        return (not self.isYMoving()) \
            and (numpy.abs(current_pos[kZ2]) < HomingError) 
    
    def movePositionZ1(self, delta, vel):
        cur_pos = self.getPosition().copy()
        new_z1 = cur_pos[kZ1] + delta
        return self.gotoPositionZ1(new_z1, vel)
    
    def movePositionZ2(self, delta, vel):
        cur_pos = self.getPosition().copy()
        new_z1 = cur_pos[kZ2] + delta
        return self.gotoPositionZ2(new_z1, vel)
    
    def movePositionY(self, delta, vel):
        cur_pos = self.getPosition().copy()
        new_y = cur_pos[kY] + delta
        return self.gotoPositionY(new_y, vel)
    
    @abstractmethod
    def motorStatus(self):
        pass

    @abstractmethod
    def clearAlert(self):
        pass

    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def homeX(self):
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
    def gotoPositionY(self, y, v):        
        pass
    
    @abstractmethod
    def gotoPositionZ1(self, z, v):        
        pass

    @abstractmethod
    def gotoPositionZ2(self, z, v):        
        pass

class MockRigHardware(AbstractRigHardware):
    def __init__(self):
        #self.position = [-0.4, -0.3, 0.0, 0.50]
        self.position = [-0.0, -0.00, 0.0, 0.00]
        self.target = [0.0, 0.0, 0.0, 0.0]
        self.vel = 0.05 # m/s
        self.homing = [False, False, False, False]
        self.homingTime = [0.0, 0.0, 0.0, 0.0]
        self.move_tolerance = config.getfloat(
            "Rig", "MoveDetectionTolerance")
    
    def _update(self, i):
        VEL = (self.target[i] - self.position[i])*self.vel
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
        self.vel = 0.05 # m/s
        self.homing[i] = True
        self.target[i] = 0.0
        self.homingTime[i] = time.time()

    def homeZ1(self):
        self._home(iZ1)
        return True
        
    def homeZ2(self):
        self._home(iZ2)
        return True
    
    def homeX(self):
        self._home(iX)
        return True
        
    def homeY(self):
        self._home(iY)
        return True
        
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
        return True
    
    def gotoPositionY(self, y, v):
        t = time.time()
        self.vel = v/5000.0
        self.target[3] = y
        self.homing[3] = True
        self.homingTime[3] = t
        return True

    def gotoPositionZ1(self, z, v): 
        self.vel = v/5000.0 
        self.target[0] = z    
        self.homing[0] = True
        self.homingTime[0] = time.time()
        return True
        
    def gotoPositionZ2(self, z, v):
        self.vel = v/5000.0 
        self.target[1] = z        
        self.homing[1] = True
        self.homingTime[1] = time.time()
        return True

    def setHomeZ1(self):
        print("Setting Home Z1")
        self.position[0] = 0.0

    def setHomeZ2(self):
        self.position[1] = 0.0

    def setHomeX(self):
        self.position[2] = 0.0

    def setHomeY(self):
        self.position[3] = 0.0

    def motorStatus(self):
        return [0, 0, 0, 0]

class FileWriterThread(threading.Thread):
    def __init__(self, rig_hardware):
        threading.Thread.__init__(self)
        self.rig_hardware = rig_hardware
        self.stopped = True

    def run(self):
        self.stopped = False
        time_start_s = time.time()
        fp = open(f"rig_{time_start_s}.csv", "w")
        for i in range(NMotors):
            fp.write(f"time_s,pos_{i}_m,torque_{i}_Percent,")
        fp.write("\n")
        sampling_time = config.getfloat("Rig", "SamplingTime")

        while not self.stopped: #read sensor continuously
            loop_start = time.time()
            position = self.rig_hardware.getPosition()
            fp.write(f"{loop_start},")
            for i in range(NMotors):
                fp.write(f"{position[i]},")
                fp.write(f"{self.rig_hardware.getTorque(i)},")
            fp.write("\n")
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < sampling_time):
                time.sleep(sampling_time - delta_time)
        fp.close()

    def stop(self):
        self.stopped = True

class RigHardware(AbstractRigHardware):
    
    def __init__(self):
        print("Initializing Rig Hardware ...")
        self.current_pos = [0.0, 0.0, 0.0, 0.0]
        self.getPosition()
        print(f"Position found {self.current_pos}")
        self.prev_pos = self.current_pos.copy()
        self.move_tolerance = config.getfloat(
            "Rig", "MoveDetectionTolerance")
        print("Done initializing rig hardware")
        self.file_writer_thread = FileWriterThread(self)
        self.file_writer_thread.start()

    def motorStatus(self): 
        responses = [] 
        for i in range(NMotors):
            responses.append(HydrationServo.motor_status(i))  #need to somehow make the motor status return into the error at hand  
        return responses

    def clearAlert(self):
        for i in range(NMotors): 
            HydrationServo.clear_alert(i) 
        return True 

    def homingMotorZ1(self):
        # ensure Z-poisions are zero within tolerance
        homing_error = config.getfloat("Rig", "HomingError")
        pos = self.getPosition()
        if (numpy.abs(pos[iZ1]) > homing_error):
            return False
        
        # stop existing moves
        self.emergencyStop()
        HydrationServo.homing_motor(iZ1)
        return True 

    def gotoPositionY(self, y, v):
        # ensure Z-poisions are zero within tolerance
        homing_error = config.getfloat("Rig", "HomingError")
        pos = self.getPosition()
        if (pos[kZ1] < -homing_error) or (pos[kZ2] < -homing_error):
            return False
        
        # stop existing moves
        self.emergencyStop()
        HydrationServo.set_position_unique(iY, y/YCal, v)
        return True

    def gotoPositionZ1(self, z, v):        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position_unique(iZ1, z/Z1Cal, v)
        return True
        
    def gotoPositionZ2(self, z, v):        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position_unique(iZ2, z/Z2Cal, v)
        return True

    def homeY(self):
        # ensure Z-poisions are zero within tolerance
        homing_error = config.getfloat("Rig", "HomingError")
        pos = self.getPosition()
        if (numpy.abs(pos[kZ1]) > homing_error) or \
            (numpy.abs(pos[kZ2]) > homing_error):
            return -1
        
        # stop existing moves
        self.emergencyStop()
        return HydrationServo.homing_motor(iY)

    def homeX(self):
        # ensure Z-poisions are zero within tolerance
        homing_error = config.getfloat("Rig", "HomingError")
        pos = self.getPosition()
        if (numpy.abs(pos[kZ1]) > homing_error) or \
            (numpy.abs(pos[kZ2]) > homing_error):
            return -1
        
        # stop existing moves
        self.emergencyStop()
        return HydrationServo.homing_motor(iX)
    
    def homeZ1(self):
        # stop existing moves
        self.emergencyStop()
        return HydrationServo.homing_motor(iZ1)
        
    def homeZ2(self):
        # stop existing moves
        self.emergencyStop()
        return HydrationServo.homing_motor(iZ2)
        
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
        HydrationServo.stop_all_motors()
        
    def isNMoving(self, n):   
        return numpy.abs(self.prev_pos[n] - self.current_pos[n]) > self.move_tolerance
    
    def isYMoving(self):
        if iY < 0:
            return False
        else:
            return self.isNMoving(kY)

    def isZ1Moving(self):
        if iZ1 < 0:
            return False
        else:
            return self.isNMoving(kZ1)

    def isZ2Moving(self):
        if iZ2 < 0:
            return False
        else:
            return self.isNMoving(kZ2)

    def getTorque(self, i):
        return HydrationServo.get_torque(i)    
    
    def setHomeZ1(self):
        HydrationServo.set_home(iZ1)

    def setHomeZ2(self):
        HydrationServo.set_home(iZ2)
    
    def setHomeY(self):
        HydrationServo.set_home(iY)

    def set_speed_rpm(self, i, rpm):
        HydrationServo.set_speed_rpm(i, rpm)
