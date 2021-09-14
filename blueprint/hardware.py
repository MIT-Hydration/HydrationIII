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
from . import relay_triac_hardware, wob_hardware, power_meter_hardware
from . import AccelGyroHardware


class HardwareFactory:

    #drill = None
    rpi = None
    rig = None
    pump = None
    wob = None
    tachometer = None
    power_meter = None
    relay_triac = None
    imu = None
    _lock = threading.Lock()

    #@classmethod
    #def getDrill(cls):
    #    cls._lock.acquire()
    #    if cls.drill is None:
    #        if (config.getboolean('Mocks', 'MockDrill')):
    #            cls.drill = DrillHardware.MockDrill()
    #        else:
    #            cls.drill = DrillHardware.Drill()
    #    cls._lock.release()
    #    return cls.drill
        
    @classmethod
    def getWaterPump(cls):
        cls._lock.acquire()
        if cls.pump is None:
            if (config.getboolean('Mocks', 'MockWaterPump') or \
                config.getboolean('Operating System', 'RunningInCoreSensorsRPi')):
                cls.pump = PumpHardware.MockPump()
            else:
                cls.pump = PumpHardware.Pump()
        cls._lock.release()
        return cls.pump
    
    @classmethod
    def getWOBSensor(cls):
        cls._lock.acquire()
        if cls.wob is None:
            if (config.getboolean('Mocks', 'MockWOBSensor')):
                cls.wob = wob_hardware.MockWOBSensor()
            else:
                cls.wob = wob_hardware.WOBSensor()
        cls._lock.release()
        return cls.wob

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
    def getPowerMeter(cls):
        cls._lock.acquire()
        if cls.power_meter is None:
            if (config.getboolean('Mocks', 'MockPowerMeter')):
                cls.power_meter = power_meter_hardware.MockPowerMeterSensor()
            else:
                cls.power_meter = power_meter_hardware.PowerMeter()
        cls._lock.release()
        return cls.power_meter

    @classmethod
    def getRelayTriac(cls):
        cls._lock.acquire()
        if cls.relay_triac is None:
            if (config.getboolean('Mocks', 'MockRelayTriac')):
                cls.relay_triac = relay_triac_hardware.MockRelayTriac()
            else:
                print("Getting actual RelayTriac...")
                cls.relay_triac = relay_triac_hardware.RelayTriac()
        cls._lock.release()
        return cls.relay_triac

    @classmethod
    def getIMU(cls):
        cls._lock.acquire()
        if cls.imu is None:
            cls.imu = AccelGyroHardware.AccelGyro()
        cls._lock.release()
        return cls.imu

    
    

