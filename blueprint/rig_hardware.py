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

class RigMoveThread(threading.Thread):
    def __init__(self, rig):
            super().__init__()
            self.rig = rig

    def run(self):
        self.stopped = False
        CONTROL_LOOP_TIME = configparser.getfloat(
            "Rig", "MoveControlLoopTime")
        HOMING_SPEED = configparser.getfloat(
            "Rig", "HomingSpeed")
        HOMING_ERROR = configparser.getfloat(
            "Rig", "HomingError")

        current_pos = numpy.array(self.rig.getPosition())
        delta_pos = current_pos - self.rig.target_pos
        
        if numpy.abs(delta_pos[1]) > HOMING_ERROR:
            if delta_pos[1] > 0:
                HydrationServo.set_speed_rpm(3, -HOMING_SPEED)
            else:
                HydrationServo.set_speed_rpm(3, HOMING_SPEED)
        
            while (not self.stopped) and \
                    (numpy.abs(delta_pos[1]) > HOMING_ERROR):
                loop_start = time.time()
                current_pos = numpy.array(self.rig.getPosition())
                delta_pos = current_pos - self.rig.target_pos
                
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < CONTROL_LOOP_TIME):
                    time.sleep(CONTROL_LOOP_TIME - delta_time)

        self.stopped = True

    def stop(self):
        HydrationServo.set_speed_rpm(3, 0)
        self.stopped = True

class RigHardware(AbstractRigHardware):

    def __init__(self):
        self.target_pos = numpy.array([
            HydrationServo.get_position(2), 
            HydrationServo.get_position(3)])
        self.threads = []

    def homeX(self):
        pass

    def homeY(self):
        self.target_pos[1] = 0.0
        homing_thread = RigMoveThread(self)
        self.threads.append(homing_thread)
        homing_thread.start()

    def getPosition(self):
        x = HydrationServo.get_position(2)/4.0
        y = HydrationServo.get_position(3)/4.0
        return [x, y]
        
    def emergencyStop(self):
        N = HydrationServo.get_num_motors()
        for n in range(N):
            HydrationServo.set_speed_rpm(n, 0)
        for th in self.threads:
            th.stop()
        