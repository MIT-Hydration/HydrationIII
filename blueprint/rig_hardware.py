"""
rig_hardware.py
Hardware Interface and Mock Layers for Hydration project Rig subsystem.
"""

from abc import ABC, abstractmethod
import configparser
import time, threading
import numpy

config = configparser.ConfigParser()
config.read('config.ini')

if config.getboolean('Operating System', 'RunningInRPi'):
    import HydrationServo

Z1Cal = config.getfloat('Rig', 'Z1Cal')
Z2Cal = config.getfloat('Rig', 'Z2Cal')
XCal = config.getfloat('Rig', 'XCal')
YCal = config.getfloat('Rig', 'YCal')

class AbstractRigHardware(ABC):
    
    def getPosition(self):
        return self.current_pos

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
    def homeZ2(self):
        pass

    @abstractmethod
    def isXMoving(self):
        pass

    @abstractmethod
    def isYMoving(self):
        pass

    @abstractmethod
    def isZ1Moving(self):
        pass

    @abstractmethod
    def isZ2Moving(self):
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
    def setHomeZ2(self):
        pass

    @abstractmethod
    def setHomeX(self):
        pass

    @abstractmethod
    def setHomeY(self):
        pass

    @abstractmethod
    def gotoPosition(self, x, y):
        pass
    
    @abstractmethod
    def gotoPositionZ1(self, z):        
        pass

    @abstractmethod
    def gotoPositionZ2(self, z):        
        pass

class MockRigHardware(AbstractRigHardware):
    def __init__(self):
        self.position = [-0.4, -0.5, 0.50, 0.50]
        self.homing = [False, False, False, False]
        self.homingTime = [0.0, 0.0, 0.0, 0.0]
        self.target = [0.0, 0.0, 0.0, 0.0]
        self.move_tolerance = config.getfloat(
            "Rig", "HomingError")
    
    def _update(self, i):
        VEL = (self.target[i] - self.position[i])*0.02 # m/s
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
        self._home(0)
        
    def homeZ2(self):
        self._home(1)
    
    def homeX(self):
        self._home(2)
        
    def homeY(self):
        self._home(2)
        
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
    
    def gotoPositionZ1(self, z): 
        self.target[0] = z    
        self.homing[0] = True
        self.homingTime[0] = time.time()
        
    def gotoPositionZ2(self, z):
        self.target[1] = z        
        self.homing[1] = True
        self.homingTime[1] = time.time()

    def setHomeZ1(self):
        self.position[0] = 0.0

    def setHomeZ2(self):
        self.position[1] = 0.0

    def setHomeX(self):
        self.position[2] = 0.0

    def setHomeY(self):
        self.position[3] = 0.0

class FileWriterThread(threading.Thread):
    def __init__(self, rig):
            super().__init__()
            self.rig = rig

    def run(self):
        self.stopped = False
        CONTROL_LOOP_TIME = config.getfloat(
            "Rig", "MoveControlLoopTime")
        HOMING_SPEED = config.getfloat(
            "Rig", "HomingSpeed")
        HOMING_ERROR = config.getfloat(
            "Rig", "HomingError")

        current_pos = numpy.array(self.rig.getPosition())
        delta_pos = current_pos - self.rig.target_pos
        N = HydrationServo.get_num_motors()
        
        if numpy.max(numpy.abs(delta_pos)) > HOMING_ERROR:
            
            for n in range(N):
                if (delta_pos[n] > 0) and (numpy.abs(delta_pos[n]) > HOMING_ERROR):
                    HydrationServo.set_speed_rpm(n, -HOMING_SPEED)
                elif (delta_pos[n] < 0) and (numpy.abs(delta_pos[n]) > HOMING_ERROR):
                    HydrationServo.set_speed_rpm(n, HOMING_SPEED)
        
            while (not self.stopped) and numpy.max(numpy.abs(delta_pos)) > HOMING_ERROR:

                loop_start = time.time()
                current_pos = numpy.array(self.rig.getPosition())
                delta_pos = current_pos - self.rig.target_pos
                
                for n in range(N):
                    if (numpy.abs(delta_pos[n]) < HOMING_ERROR):
                        HydrationServo.set_speed_rpm(n, 0)

                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < CONTROL_LOOP_TIME):
                    time.sleep(CONTROL_LOOP_TIME - delta_time)

        for n in range(N):
            HydrationServo.set_speed_rpm(n, 0)
        
        self.stopped = True

    def stop(self):
        HydrationServo.set_speed_rpm(3, 0)
        self.stopped = True

class RigHardware(AbstractRigHardware):

    def __init__(self):
        self.current_pos = numpy.array([
            HydrationServo.get_position(0)*Z1Cal, 
            HydrationServo.get_position(1)*Z2Cal,
            HydrationServo.get_position(2)*XCal, 
            HydrationServo.get_position(3)*YCal])
        self.prev_pos = self.current_pos.copy()
        self.move_tolerance = config.getfloat(
            "Rig", "HomingError")

    def gotoPosition(self, x, y):
        # ensure Z-poisions are zero within tolerance
        pos = self.getPosition()
        if (numpy.abs(pos[0]) > self.move_tolerance) or \
            (numpy.abs(pos[1]) > self.move_tolerance):
            return
        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position(2, x/XCal)
        HydrationServo.set_position(3, y/YCal)
        
    def gotoPositionZ1(self, z):        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position(0, z/Z1Cal)
        
    def gotoPositionZ2(self, z):        
        # stop existing threads
        self.emergencyStop()
        HydrationServo.set_position(1, z/Z2Cal)
        
    def homeX(self):
        pos = self.getPosition()
        self.gotoPosition(0, pos[3])

    def homeY(self):
        pos = self.getPosition()
        self.gotoPosition(pos[2], 0)

    def homeZ1(self):
        self.gotoPositionZ1(0)

    def homeZ2(self):
        self.gotoPositionZ2(0)

    def getPosition(self):
        self.prev_pos = self.current_pos.copy()
        z1 = HydrationServo.get_position(0)*Z1Cal
        z2 = HydrationServo.get_position(1)*Z2Cal
        x = HydrationServo.get_position(2)*XCal
        y = HydrationServo.get_position(3)*YCal
        self.current_pos = numpy.array([z1, z2, x, y])
        return self.current_pos
        
    def emergencyStop(self):
        N = HydrationServo.get_num_motors()
        for n in range(N):
            HydrationServo.set_speed_rpm(n, 0)
        
    def isNMoving(self, n):   
        return numpy.abs(self.prev_pos[n] - self.current_pos[n]) > self.move_tolerance
    
    def isXMoving(self):
        return self.isNMoving(2)

    def isYMoving(self):
        return self.isNMoving(3)

    def isZ1Moving(self):
        return self.isNMoving(0)

    def isZ2Moving(self):
        return self.isNMoving(1)

    def getTorque(self, i):
        return HydrationServo.get_torque(i)    
    
    def setHomeZ1(self):
        HydrationServo.set_home(0)

    def setHomeZ2(self):
        HydrationServo.set_home(1)

    def setHomeX(self):
        HydrationServo.set_home(2)

    def setHomeY(self):
        HydrationServo.set_home(3)
    
   

