"""
test-servo-data-collection-integration.py
Test simulataneous data collection and servo motor control
"""

__author__      = "Prakash Manandhar, Palak Patel, Tao Sevigny"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar, Palak Patel, Tao Sevigny"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "prakashm@alum.mit.edu"
__status__ = "Production"

from abc import ABC, abstractmethod
import time
import threading
import re
import numpy

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder

from gpiozero import PWMLED
from gpiozero import CPUTemperature

import serial
import HydrationServo

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    import hx711
else:
    from emulated_hx711 import HX711

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
    
class Drill(AbstractDrill):

    motor = PWMLED(12)
    cpu_temperature_degC = CPUTemperature()

    class DrillArduinoThread(threading.Thread):

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

    
    class DrillPowerMeterThread(threading.Thread):

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

    class DrillWeightOnBitThread(threading.Thread):

        referenceUnit = 1 #610900.0/1324.0 # display units per graph
        hx = hx711.HX711(5, 6)

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = True
            self.sensor_readings = {
                    "WeightOnBit": 0.0
                }
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(self.referenceUnit)
            self.hx.reset()
            self.hx.tare()

        def run(self):
            self.stopped = False
            while not self.stopped:
                loop_start = time.time()
                try:
                    val = self.hx.get_weight(5)
                    self.sensor_readings["WeightOnBit"] = val
                    self.hx.power_down()
                    self.hx.power_up()
                except Exception as e:
                    print(e)
                    pass
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.01):
                    time.sleep(0.01 - delta_time)
                
        def stop(self):
            if not EMULATE_HX711:
                GPIO.cleanup()
            self.stopped = True

    class DrillZ1ServoThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = True
            self.sensor_readings = {
                    "DrillZ1Position_m": 0.0
                }
            
        def run(self):
            self.stopped = False
            while not self.stopped:
                loop_start = time.time()
                try:
                    current_position = HydrationServo.get_drill_position()
                    self.sensor_readings["DrillZ1Position_m"] = current_position
                except Exception as e:
                    print(e)
                    pass
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.01):
                    time.sleep(0.01 - delta_time)
                
        def stop(self):
            self.stopped = True
    
    class FileWriterThread(threading.Thread):

        def __init__(self, drill_pm_thread, 
                drill_ad_thread, drill_wob_thread,
                drill_z1_thread):
            self.delay = 0.0007856988543367034
            self.sample_time = 0.02
            self.sleep_time = self.sample_time - self.delay
            threading.Thread.__init__(self)
            self.drill_pm_thread = drill_pm_thread
            self.drill_ad_thread = drill_ad_thread
            self.drill_wob_thread = drill_wob_thread
            self.drill_z1_thread = drill_z1_thread
            self.stopped = True
            
        def run(self):
            self.stopped = False
            time_start_s = time.time()
            fp = open(f"{time_start_s}.csv", "w")
            fp.write("time_s,cpu_t_degC,motor_command,")
            for k in self.drill_pm_thread.sensor_readings:
                fp.write(f"{k},")
            for k in self.drill_ad_thread.sensor_readings:
                fp.write(f"{k},") 
            for k in self.drill_wob_thread.sensor_readings:
                fp.write(f"{k},")
            for k in self.drill_z1_thread.sensor_readings:
                fp.write(f"{k},")
             
            fp.write("\n")
            while not self.stopped:
                loop_start = time.time()
                fp.write(f"{loop_start},")
                fp.write(f"{Drill.cpu_temperature_degC.temperature},")
                fp.write(f"{Drill.motor.value},")
                for k in self.drill_pm_thread.sensor_readings:
                    fp.write(f"{self.drill_pm_thread.sensor_readings[k]},")
                for k in self.drill_ad_thread.sensor_readings:
                    fp.write(f"{self.drill_ad_thread.sensor_readings[k]},")
                for k in self.drill_wob_thread.sensor_readings:
                    fp.write(f"{self.drill_wob_thread.sensor_readings[k]},")
                for k in self.drill_z1_thread.sensor_readings:
                    fp.write(f"{self.drill_z1_thread.sensor_readings[k]},")
                
                fp.write("\n")
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < self.sleep_time):
                    time.sleep(self.sleep_time - delta_time)

            fp.close()
                
        def stop(self):
            self.stopped = True
            
    drill_pm_thread = DrillPowerMeterThread()
    drill_ad_thread = DrillArduinoThread()
    drill_wob_thread = DrillWeightOnBitThread()
    drill_z1_thread = DrillZ1ServoThread()
    writer_thread = FileWriterThread(
        drill_pm_thread, drill_ad_thread, drill_wob_thread,
        drill_z1_thread)

    
    @classmethod
    def start_sensor_readings(cls):
        cls.drill_pm_thread.start()
        cls.drill_ad_thread.start()
        cls.drill_wob_thread.start()
        cls.drill_z1_thread.start()
        cls.writer_thread.start()

    @classmethod
    def stop_sensor_readings(cls):
        cls.drill_pm_thread.stop()
        cls.drill_ad_thread.stop()
        cls.drill_wob_thread.stop()
        cls.drill_z1_thread.stop()
        cls.writer_thread.stop()

    @classmethod
    def set_drill_level(cls, level):
        cls.motor.value = level

    @classmethod
    def get_drill_level(cls, level):
        return cls.motor.value

    @classmethod
    def get_speed_rpm(cls):
        return cls.drill_pm_thread.sensor_readings["speed_rpm"]
        pass

    @classmethod
    def get_active_power_W(cls):
        return cls.drill_pm_thread.sensor_readings["active_power_W"]
    
    @classmethod
    def get_current_mA(cls):
        return cls.drill_pm_thread.sensor_readings["current_mA"]

def move_to_target_position(target, drill):
    PID_P = 100000
    TOLERANCE = 0.001 # m
    MAX_SPEED = 250 # rpm
    HydrationServo.set_drill_speed(0)
    current_position = HydrationServo.get_drill_position()
    while (abs(current_position - target) > TOLERANCE):
        speed = PID_P * (target - current_position)
        if (abs(speed) > MAX_SPEED):
            speed = numpy.sign(speed)*MAX_SPEED
        HydrationServo.set_drill_speed(speed)
        time.sleep(0.1)
        current_position = HydrationServo.get_drill_position()
        print(drill.drill_pm_thread.sensor_readings)
        print(drill.drill_ad_thread.sensor_readings)
        print(drill.drill_wob_thread.sensor_readings)
        print(drill.drill_z1_thread.sensor_readings)
    HydrationServo.set_drill_speed(0)

if __name__ == "__main__":
    
    drill = Drill()
    drill.set_drill_level(0.0)
    drill.start_sensor_readings()
    print ("Init Done!")
 
    time.sleep(10)
    time_start_s = time.time()
    time_s = time.time()
    drill.set_drill_level(1.0) # turn to maximum drill speed
    target = -4 * 25.4/1000 # -2 inches to m
    try:
        move_to_target_position(0, drill) # home
        time.sleep(1)
        move_to_target_position(target, drill)
        time.sleep(1)
        move_to_target_position(0, drill) # home

    except Exception as e:
        print("Exception!")
        print(e)
        HydrationServo.set_drill_speed(0)
    HydrationServo.set_drill_speed(0)

    drill.set_drill_level(0)
    time.sleep(10)

    drill.stop_sensor_readings()
