"""
hardware.py
Hardware Interface and Mock Layers for Hydration project.
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

from abc import ABC, abstractmethod
import time
import threading

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if config.getboolean('Operating System', 'RunningInRPi'):
    from gpiozero import PWMLED
    from gpiozero import CPUTemperature

from . import RPiHardware, rig_hardware, WaterPumpHardware

class HardwareFactory:

    drill = None
    rpi = None
    rig = None
    water_pump = None

    @classmethod
    def getDrill(cls):
        if cls.drill is None:
            if (config.getboolean('Mocks', 'MockDrill')):
                cls.drill = MockDrill()
            else:
                cls.drill = Drill()
        return cls.drill

    @classmethod
    def getWaterPump(cls):
        if cls.drill is None:
            if (config.getboolean('Mocks', 'MockWaterPump')):
                cls.drill = MockPump()
            else:
                cls.drill = Pump()
        return cls.drill
    
    @classmethod
    def getMissionControlRPi(cls):
        if cls.rpi is None:
            if (config.getboolean('Mocks', 'MockMissionControlRPi')):
                cls.rpi = RPiHardware.MockRPiHardware()
            else:
                cls.rpi = RPiHardware.RPiHardware()
        return cls.rpi

    @classmethod
    def getRig(cls):
        if cls.rig is None:
            if (config.getboolean('Mocks', 'MockRig')):
                cls.rig = rig_hardware.MockRigHardware()
            else:
                cls.rig = rig_hardware.RigHardware()
        return cls.rig
    
class AbstractDrill(ABC):

    @abstractmethod
    def start_sensor_readings(cls):
        pass

    @abstractmethod
    def start_sensor_readings(cls):
        pass
    
    @abstractmethod
    def set_drill_level(self, level):
        pass

    @abstractmethod
    def get_drill_level(self):
        pass

    @abstractmethod
    def get_speed_rpm(self):
        pass

    @abstractmethod
    def get_active_power_W(self):
        pass

    @abstractmethod
    def get_current_mA(self):
        pass


class MockDrill(AbstractDrill):
    
    def __init__(self):
        self._set_time = time.time()
        self._current_level = 0.0
        self._set_level = 0.0

    def set_drill_level(self, level):
        self._set_time = time.time()
        self._set_level = level

    @classmethod
    def start_sensor_readings(cls):
        pass

    @classmethod
    def start_sensor_readings(cls):
        pass
    
    def get_drill_level(self, level):
        return self._set_level
        
    def get_speed_rpm(self):
        return -100.0

    def get_active_power_W(self):
        return -2000.0

    def get_current_mA(self):
        return -999.0
    
class Drill(AbstractDrill):

    class DrillThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = True
            self.sensor_readings = {
                    "active_power_W": 0.0,
                    "current_mA": 0.0,
                    "speed_rpm": 0.0,
                    "accel_x_g": 0.0,
                    "accel_y_g": 0.0,
                    "accel_z_g": 0.0,
                }
            self.client = ModbusSerialClient(port='/dev/ttyUSB0', method='rtu', baudrate=9600)

        def run(self):
            self.stopped = False
            while not self.stopped:
                loop_start = time.time()
                result  = self.client.read_holding_registers(address, count,  unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, 
                    wordorder = '>', byteorder = '>')
                current_mA = decoder.decode_32bit_float()
                power_W = decoder.decode_32bit_float()
                self.sensor_readings["active_power_W"] = power_W
                self.sensor_readings["current_mA"] =  current_mA
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.01):
                    time.sleep(0.01 - delta_time)
                
        def stop(self):
            self.stopped = True

    class FileWriterThread(threading.Thread):

        def __init__(self, drill_thread):
            threading.Thread.__init__(self)
            self.drill_thread = drill_thread
            self.stopped = True
            
        def run(self):
            self.stopped = False
            fp = open(f"{time_start_s}.csv", "w")
            fp.write("time_s,")
            keys = drill_thread.sensor_readings.keys
            for k in keys:
                fp.write(f"{k},")
            fp.write("\n")
            while not self.stopped:
                loop_start = time.time()
                fp.write(f"{loop_start},")
                for k in keys:
                    fp.write(f"{drill_thread.sensor_readings[k]},")
                fp.write("\n")
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.02):
                    time.sleep(0.02 - delta_time)

            fp.close()
                
        def stop(self):
            self.stopped = True
            
    modbus_reg_address = 75
    modbus_reg_count   = 4
    motor = HardwareFactory.getMissionControlRPi() \
        .connect_triac_pin(config.getint(
            'HardwareConnection', 'TriacGPIOPin'))
    drill_thread = DrillThread()
    writer_thread = FileWriterThread(drill_thread)
    
    @classmethod
    def start_sensor_readings(cls):
        cls.drill_thred.start()
        cls.writer_thread.start()

    @classmethod
    def stop_sensor_readings(cls):
        cls.drill_thread.stop()
        cls.writer_thread.stop()

    @classmethod
    def set_drill_level(cls, level):
        cls.motor.value = level

    @classmethod
    def get_drill_level(cls, level):
        return cls.motor.value

    @classmethod
    def get_speed_rpm(cls):
        return cls.drill_thread.sensor_readings["speed_rpm"]
        pass

    @classmethod
    def get_active_power_W(cls):
        return cls.drill_thread.sensor_readings["active_power_W"]
    
    @classmethod
    def get_current_mA(cls):
        return cls.drill_thread.sensor_reading["current_mA"]