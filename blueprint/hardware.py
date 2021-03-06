"""
hardware.py
Hardware Interface and Mock Layers for Hydration project.
"""

__author__      = "Prakash Manandhar, Tao Sevigny"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar, Tao Sevigny"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

from abc import ABC, abstractmethod
import time
import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
if config.getboolean('Operating System', 'RunningInRPi'):
    from pymodbus.client.sync import ModbusSerialClient
    from pymodbus.payload import BinaryPayloadDecoder

    from gpiozero import PWMLED
    from gpiozero import CPUTemperature

class HardwareFactory:
    
    is_mock = {
        "drill": True
    }

    mock_load_profile_simple = {
        "drill_ramp_delay_ms": 10,
        "drill_ramp_slope_rpm_per_ms": 10 
    }

    current_load_profile = mock_load_profile_simple

    @classmethod
    def getDrill(cls):
        if (cls.is_mock["drill"]):
            return MockDrill()
        else:
            return Drill()


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
    def get_drill_level(self, level):
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
    
    
    def start_sensor_readings(cls):
        pass

    
    def start_sensor_readings(cls):
        pass
    
    
    def set_drill_level(self, level):
        pass

    
    def get_drill_level(self, level):
        pass

    
    def get_speed_rpm(self):
        pass

    
    def get_active_power_W(self):
        pass

    
    def get_current_mA(self):
        pass

if config.getboolean('Operating System', 'RunningInRPi'):

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
        motor = PWMLED(12)
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
