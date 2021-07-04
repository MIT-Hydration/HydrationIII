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


class ArduinoThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = True
        self.sensor_readings = {
                "arduino_timestamp_ms": 0.0,
                "tacho_rpm": 0.0,
                "imu_x_g": 0.0,
                "imu_y_g": 0.0,
                "imu_z_g": 0.0,
            }
        self.port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=5,
            bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE)
        self.arduino_primed = False
        self.pattern = re.compile(
            b'TS = ([0-9]+) ms, TACHO = ([-0-9.]+) RPM, IMU = \(([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\) g')

    def run(self):
        self.stopped = False
        while not self.stopped:
            loop_start = time.time()
            if not self.arduino_primed:
                self.port.flush()
                written = self.port.write(b"START_STREAM\n")
                self.port.flush()
                print(f"wrote {written}")
            rcv = self.port.readline()
            #print(str(rcv))
            m = self.pattern.match(rcv)
            if m is not None:    
                self.sensor_readings["arduino_timestamp_ms"] = int(m.group(1))
                self.sensor_readings["tacho_rpm"] =  float(m.group(2))
                self.sensor_readings["imu_x_g"] = float(m.group(3))
                self.sensor_readings["imu_y_g"] = float(m.group(4))
                self.sensor_readings["imu_z_g"] = float(m.group(5))
                self.arduino_primed = True  
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < 0.01):
                time.sleep(0.01 - delta_time)
            
    def stop(self):
        self.stopped = True

class PowerMeterThread(threading.Thread):

    modbus_reg_address = 75
    modbus_reg_count   = 4

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = True
        self.sensor_readings = {
                "active_power_W": 0.0,
                "current_mA": 0.0,
            }
        self.client = ModbusSerialClient(port='/dev/ttyUSB0', method='rtu', baudrate=9600)
        
    def run(self):
        self.stopped = False
        while not self.stopped:
            loop_start = time.time()
            result  = self.client.read_holding_registers(
                self.modbus_reg_address, self.modbus_reg_count,  unit=1)
            try:
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, 
                    wordorder = '>', byteorder = '>')
                current_mA = decoder.decode_32bit_float()
                power_W = decoder.decode_32bit_float()
                self.sensor_readings["active_power_W"] = power_W
                self.sensor_readings["current_mA"] =  current_mA
            except:
                pass
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < 0.01):
                time.sleep(0.01 - delta_time)
            
    def stop(self):
        self.stopped = True

class FileWriterThread(threading.Thread):

    def __init__(self, drill_pm_thread, drill_ad_thread, rig):
        self.delay = 0.0007856988543367034
        self.sample_time = 0.02
        self.sleep_time = self.sample_time - self.delay
        threading.Thread.__init__(self)
        self.drill_pm_thread = drill_pm_thread
        self.drill_ad_thread = drill_ad_thread
        self.rig = rig
        self.wob_sensor = hardware.HardwareFactory.getWOBSensor()
        self.stopped = True
        
    def run(self):
        rig = self.rig
        self.stopped = False
        time_start_s = time.time()
        fp = open(f"all_data_{time_start_s}.csv", "w")
        fp.write("time_s,cpu_t_degC,motor_command,Z1_m,Z2_m,X_m,Y_m,TZ1,TZ2,TX,TY,WOB_ts,WOB_N,")
        for k in self.drill_pm_thread.sensor_readings:
            fp.write(f"{k},")
        for k in self.drill_ad_thread.sensor_readings:
            fp.write(f"{k},")    
        fp.write("\n")
        while not self.stopped:
            loop_start = time.time()
            fp.write(f"{loop_start},")
            fp.write(f"{rig.cpu_temperature_degC.temperature},")
            fp.write(f"{rig.motor.value},")
            pos = rig.getPosition()
            fp.write(f"{pos[0]},{pos[1]},{pos[2]},{pos[3]},")
            for n in range(4):
                fp.write(f"{rig.getTorque(n)},") 
            force_N = self.wob_sensor.get_force_N()
            fp.write(f"{force_N[0]},")       
            fp.write(f"{force_N[1]},")
            for k in self.drill_pm_thread.sensor_readings:
                fp.write(f"{self.drill_pm_thread.sensor_readings[k]},")
            for k in self.drill_ad_thread.sensor_readings:
                fp.write(f"{self.drill_ad_thread.sensor_readings[k]},")
            fp.write("\n")
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < self.sleep_time):
                time.sleep(self.sleep_time - delta_time)

        fp.close()
            
    def stop(self):
        self.stopped = True

print("Here Before RigHardware")

class RigHardware(AbstractRigHardware):
    
    def __init__(self):
        print("Initializing Rig Hardware ...")
        self.current_pos = numpy.array([
            HydrationServo.get_position(iZ1)*Z1Cal, 
            HydrationServo.get_position(iZ2)*Z2Cal,
            HydrationServo.get_position(iX)*XCal, 
            HydrationServo.get_position(iY)*YCal])
        print(f"Position found {self.current_pos}")
        self.prev_pos = self.current_pos.copy()
        self.move_tolerance = config.getfloat(
            "Rig", "HomingError")

        #self.motor = PWMLED(12)
        #self.motor = 0
        self.cpu_temperature_degC = CPUTemperature()

        #self.pm_thread = PowerMeterThread()
        #self.ad_thread = ArduinoThread()
        #self.writer_thread = FileWriterThread(
        #    self.pm_thread, self.ad_thread, self)

        #self.pm_thread.start()
        #self.ad_thread.start()
        #self.writer_thread.start()

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
        if iZ1 < 0:
            z1 = HydrationServo.get_position(iZ1)*Z1Cal
        if iZ2 < 0:
            z2 = HydrationServo.get_position(iZ2)*Z2Cal
        if iX < 0:
            x = HydrationServo.get_position(iX)*XCal
        if iY < 0:
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