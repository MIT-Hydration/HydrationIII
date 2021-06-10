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

class MockRigHardware(AbstractRigHardware):
    
    def __init__(self):
        self.position = [-0.4, -0.5, 0.50, 0.50]
        self.homing = [False, False, False, False]
        self.homingTime = [0.0, 0.0, 0.0, 0.0]
    
    def _update(self, i):
        VEL = -0.02 # m/s
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
        N = len(self.position)
        for n in range(N):
            self._update(n)
        return self.position

    def homeZ1(self):
        self.homing[0] = True
        self.homingTime[0] = time.time()
        
    def homeZ2(self):
        self.homing[1] = True
        self.homingTime[1] = time.time()
    
    def homeX(self):
        self.homing[2] = True
        self.homingTime[2] = time.time()
        
    def homeY(self):
        self.homing[3] = True
        self.homingTime[3] = time.time()
        
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

    def isXMoving(self):
        #print(f"X is moving {self.homing[0]}")
        return self.homing[2]

    def isYMoving(self):
        return self.homing[3]

class RigMoveThread(threading.Thread):
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
                
                if (numpy.abs(delta_pos[0]) > HOMING_ERROR):
                    HydrationServo.set_speed_rpm(2, 0)
                
                if (numpy.abs(delta_pos[1]) > HOMING_ERROR):
                    HydrationServo.set_speed_rpm(3, 0)

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
        self.target_pos = numpy.array([
            HydrationServo.get_position(0), 
            HydrationServo.get_position(1),
            HydrationServo.get_position(2)*4.0, 
            HydrationServo.get_position(3)*4.0])
        self.prev_pos = self.target_pos.copy()
        self.current_pos = self.target_pos.copy()
        self.threads = []
        self.move_tolerance = config.getfloat(
            "Rig", "HomingError")

    def homeX(self):
        self.target_pos[2] = 0.0
        homing_thread = RigMoveThread(self)
        self.threads.append(homing_thread)
        homing_thread.start()

    def homeY(self):
        self.target_pos[3] = 0.0
        homing_thread = RigMoveThread(self)
        self.threads.append(homing_thread)
        homing_thread.start()

    def homeZ1(self):
        self.target_pos[0] = 0.0
        homing_thread = RigMoveThread(self)
        self.threads.append(homing_thread)
        homing_thread.start()

    def homeZ2(self):
        self.target_pos[1] = 0.0
        homing_thread = RigMoveThread(self)
        self.threads.append(homing_thread)
        homing_thread.start()

    def getPosition(self):
        self.prev_pos = self.current_pos.copy()
        z1 = HydrationServo.get_position(0)
        z2 = HydrationServo.get_position(1)
        x = HydrationServo.get_position(2)*4.0
        y = HydrationServo.get_position(3)*4.0
        self.current_pos = numpy.array([z1, z2, x, y])
        return self.current_pos
        
    def emergencyStop(self):
        N = HydrationServo.get_num_motors()
        for n in range(N):
            HydrationServo.set_speed_rpm(n, 0)
        for th in self.threads:
            th.stop()

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

    

