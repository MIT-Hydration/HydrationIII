"""
power_meter_hardware.py
"__"

"""

__author__      = "Prakash Manandhar, and Sophie Yang"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar, and Sophie Yang"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Sophie Yang"
__email__ = "scyang@mit.edu"
__status__ = "Production"

from time import sleep  # this lets us have a time delay
import time
from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html

import numpy

import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
        
from pymodbus.client.sync import ModbusSerialClient
    
class AbstractPowerMeter(ABC):

    @abstractmethod
    # returns a timestamped power reading
    def get_active_power_W(self):
        pass

    @abstractmethod
    def get_current_mA(self):
        pass


class MockPowerMeterSensor(AbstractPowerMeter):

    def get_active_power_W(self):
        return [time.time(), -2000.0]

    def get_current_mA(self):
        return [time.time(), -999.0]

class PowerMeterThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = True
        self.sensor_readings = {
                "time_s": 0.0,
                "active_power_W": 0.0,
                "current_mA": 0.0,
            }

        self.client = ModbusSerialClient(port=config.get('PowerMeter', 'port'), method='rtu', baudrate=config.getint('PowerMeter', 'baudrate'))

    def run(self):
        self.stopped = False
        address = config.getint("PowerMeter", "address")
        count = config.getint("PowerMeter", "count")
        sampling_time = config.getfloat("PowerMeter", "SamplingTime")

        while not self.stopped:
            loop_start = time.time()
            result  = self.client.read_holding_registers(address, count,  unit=1)
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                wordorder = '>', byteorder = '>')
            current_mA = decoder.decode_32bit_float()
            power_W = decoder.decode_32bit_float()
            self.sensor_readings["time_s"] = loop_start
            self.sensor_readings["active_power_W"] = power_W
            self.sensor_readings["current_mA"] =  current_mA
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < sampling_time):
                time.sleep(sampling_time - delta_time)

    def stop(self):
        self.stopped = True

class FileWriterThread(threading.Thread):

    def __init__(self, power_meter_thread):
        threading.Thread.__init__(self)
        self.power_meter_thread = power_meter_thread
        self.stopped = True

    def run(self):
        self.stopped = False
        fp = open(f"power_meter_{time_start_s}.csv", "w")
        keys = power_meter_thread.sensor_readings.keys
        for k in keys:
            fp.write(f"{k},")
        fp.write("\n")
        sampling_time = config.getfloat("PowerMeter", "SamplingTime")

        while not self.stopped: #read sensor continuously
            loop_start = time.time()
            for k in keys:
                fp.write(f"{power_meter_thread.sensor_readings[k]},")
            fp.write("\n")
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < sampling_time):
                time.sleep(sampling_time - delta_time)
        fp.close()

    def stop(self):
        self.stopped = True

class PowerMeter(AbstractPowerMeter):

    def __init__(self):
        self.power_meter_thread = PowerMeterThread()
        self.file_writer_thread = FileWriterThread(self.power_meter_thread)
        self.power_meter_thread.start()
        self.file_writer_thread.start()

    def get_active_power_W(self):
        return [self.power_meter_thread.sensor_readings["time_s"],
                self.power_meter_thread.sensor_readings["active_power_W"]]

    def get_current_mA(self):
        return [self.power_meter_thread["time_s"],
                self.power_meter_thread["current_mA"]]
