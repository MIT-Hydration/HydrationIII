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
                response = stub.SetHomeY (
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
    
    def __init__(self, delta):
        QtCore.QThread.__init__(self)
        self.delta = delta
        
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

class GotoZ1Thread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.Z1Move (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta),
                    timeout = GRPC_CALL_TIMEOUT )

class GotoYThread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.YMove (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta),
                    timeout = GRPC_CALL_TIMEOUT )