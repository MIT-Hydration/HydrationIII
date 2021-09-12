"""
client_common.py
Common classes for the client
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

import configparser
from datetime import datetime, timedelta
import time
from PySide6 import QtCore
from PySide6.QtCore import QTimer, Signal

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

config = configparser.ConfigParser(
    converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config.read('config.ini')

MC_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

CS_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'CoreSensorsRPiAddress')}:" \
    f"{config.get('Network', 'CoreSensorsGRPCPort')}"


GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class ModeChangeThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    def __init__(self, new_mode):
        QtCore.QThread.__init__(self)
        self.new_mode = new_mode
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.GotoMajorMode (
                    mission_control_pb2.GotoMajorModesRequest(
                        request_timestamp = timestamp,
                        new_mode = self.new_mode),
                    timeout = GRPC_CALL_TIMEOUT )      
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

        self.done.emit(response)

class NewHoleThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartDrillHole (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )      
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

        self.done.emit(response)

class StartMeltThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartMelting (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )      
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

        self.done.emit(response)


class EndMeltThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.EndMelting (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )      
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

        self.done.emit(response)

class EndHoleThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.EndDrillHole (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )      
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

        self.done.emit(response)

class SetHomeThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.SetHomeZ1 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
                response = stub.SetHomeZ2 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
                response = stub.SetHomeY (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
                
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)
        self.done.emit(response)

class AlignHeaterThread(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.AlignHeater (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
                
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)
        self.done.emit(response)

class GotoThread(QtCore.QThread):   
    done = Signal(object)
    log = Signal(object)
    
    def __init__(self, delta, vel):
        QtCore.QThread.__init__(self)
        self.delta = delta
        self.vel = vel 
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        #print(f"Moving to {self.z}")
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = self._request_response(stub, timestamp)
                
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)
        if response != None:
            self.log.emit(response)
        self.done.emit(response)

    def _request_response(self, stub):
        pass


class RelayThread(QtCore.QThread):   
    done = Signal(object)
    log = Signal(object)
    
    def __init__(self, drill_or_heater, val):
        QtCore.QThread.__init__(self)
        self.drill_or_heater = (drill_or_heater == "Drill")
        self.val = val 
        
    def run(self):
        global CS_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        #print(f"Moving to {self.z}")
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(CS_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.CoreSensorsStub(channel)
                if self.drill_or_heater:
                    if self.val:
                        response = stub.DrillOn (
                            mission_control_pb2.StartCommandRequest(
                                request_timestamp = timestamp),
                                timeout = GRPC_CALL_TIMEOUT )   
                    else:
                        response = stub.DrillOff (
                            mission_control_pb2.StartCommandRequest(
                                request_timestamp = timestamp),
                                timeout = GRPC_CALL_TIMEOUT ) 
                else:
                    if self.val:
                        response = stub.HeaterOn (
                            mission_control_pb2.StartCommandRequest(
                                request_timestamp = timestamp),
                                timeout = GRPC_CALL_TIMEOUT )   
                    else:
                        response = stub.HeaterOff (
                            mission_control_pb2.StartCommandRequest(
                                request_timestamp = timestamp),
                                timeout = GRPC_CALL_TIMEOUT ) 
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)
        if response != None:
            self.log.emit(response)
        self.done.emit(response)

class TriacThread(QtCore.QThread):   
    done = Signal(object)
    log = Signal(object)
    
    def __init__(self, val):
        QtCore.QThread.__init__(self)
        self.val = val 
        
    def run(self):
        global CS_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(CS_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.CoreSensorsStub(channel)
                response = stub.SetTriacLevel (
                    mission_control_pb2.TriacRequest(
                        request_timestamp = timestamp),
                        value = self.val,
                        timeout = GRPC_CALL_TIMEOUT ) 
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)
        if response != None:
            self.log.emit(response)
        self.done.emit(response)

class ClearAlert(QtCore.QThread):    
    done = Signal(object)
    log = Signal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
       

    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.ClearAlerts (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )     
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

        self.done.emit(response)
        #do we have to return anything? probably in the emit response stuff
 
class GotoZ1Thread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.Z1Move (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta, 
                        vel = self.vel),
                    timeout = GRPC_CALL_TIMEOUT )

class GotoZ2Thread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.Z2Move (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta, 
                        vel = self.vel),
                    timeout = GRPC_CALL_TIMEOUT )

class GotoYThread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.YMove (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta, 
                        vel = self.vel),
                    timeout = GRPC_CALL_TIMEOUT )