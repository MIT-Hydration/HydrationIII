"""
hardware.py
Hardware Interface and Mock Layers for Hydration project.
"""

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

from . import RPiHardware, rig_hardware, PumpHardware, TachometerHardware

class HardwareFactory:

    drill = None
    rpi = None
    rig = None
    pump = None
    tachometer = None
    _lock = threading.Lock()

    @classmethod
    def getDrill(cls):
        cls._lock.acquire()
        if cls.drill is None:
            if (config.getboolean('Mocks', 'MockDrill')):
                cls.drill = MockDrill()
            else:
                cls.drill = Drill()
        cls._lock.release()
        return cls.drill
        
    @classmethod
    def getWaterPump(cls):
        cls._lock.acquire()
        if cls.pump is None:
            if (config.getboolean('Mocks', 'MockWaterPump')):
                cls.pump = MockPump()
            else:
                cls.pump = Pump()
        cls._lock.release()
        return cls.pump
    
            
    @classmethod
    def getTachometer(cls):
        cls._lock.acquire()
        if cls.tachometer is None:
            if (config.getboolean('Mocks', 'MockTachometer')):
                cls.tachometer = MockTachometer()
            else:
                cls.tachometer = Tachometer()
        cls._lock.release()
        return cls.tachometer
        
    @classmethod
    def getMissionControlRPi(cls):
        cls._lock.acquire()
        if cls.rpi is None:
            if (config.getboolean('Mocks', 'MockMissionControlRPi')):
                cls.rpi = RPiHardware.MockRPiHardware()
            else:
                cls.rpi = RPiHardware.RPiHardware()
        cls._lock.release()
        return cls.rpi
        
    @classmethod
    def getRig(cls):
        cls._lock.acquire()
        if cls.rig is None:
            if (config.getboolean('Mocks', 'MockRig')):
                cls.rig = rig_hardware.MockRigHardware()
            else:
                cls.rig = rig_hardware.RigHardware()
        cls._lock.release()
        return cls.rig

    @classmethod
    def getWaterPump(cls):
        cls._lock.acquire()
        if cls.drill is None:
            if (config.getboolean('Mocks', 'MockWaterPump')):
                cls.drill = PumpHardware.MockPump()
            else:
                cls.drill = PumpHardware.Pump()
        cls._lock.release()
        return cls.drill
    

