"""
startup_diagnostics_display.py
The P01 panel for startup and diagnostics display for the mission control client.
"""

__author__      = "Prakash Manandhar, and Marcellin Feasson"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar, and Marcellin Feasson"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Marcellin Feasson"
__email__ = "feasson.marcellin@gmail.com"
__status__ = "Production"

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QDateTime

from QLed import QLed
from datetime import datetime, timedelta
import time
import configparser

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

config = configparser.ConfigParser()
config.read('config.ini')

MC_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class StartMissionClockThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartMissionClock (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartHomeZ1Thread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartHomeZ1 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartHomeZ2Thread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartHomeZ2 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartHomeXThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartHomeX (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartHomeYThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartHomeY (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartSpinDrillMotorThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartSpinDrillMotor (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartSpinPumpThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartSpinPump (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartHeaterThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StartHeater (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class StartupDiagnosticsDisplay:

    def __init__(self, layout):
        # Tuple (buttons display text, pointer to functions)     
        self.startup_list = [
            ("Start mission clock", self.start_mission_clock),
            ("Home Z1 axis servo", self.start_home_Z1),  
            ("Home Z2 axis servo", self.start_home_Z2), 
            ("Home X axis servo", self.start_home_X), 
            ("Home Y axis servo", self.start_home_Y), 
            ("Spin Drill motor", self.start_spin_drill_motor), 
            ("Spin pump", self.start_spin_pump), 
            ("Start heater", self.start_heater),        
        ]
        
        self.buttons = [None] * len(self.startup_list)
        self.layout = layout
        self._initWidgets()

    def _initWidgets(self):
        for i in range(len(self.startup_list)):
            self.buttons[i] = QtWidgets.QPushButton(self.startup_list[i][0])
            self.layout.addWidget(self.buttons[i])
            self.buttons[i].clicked.connect(self.startup_list[i][1])
        self.layout.addStretch(5)

    def start_mission_clock(self):
        self.threads = []
        client_thread = StartMissionClockThread()
        self.threads.append(client_thread)
        client_thread.start()      

    def start_home_Z1(self):
        self.threads = []
        client_thread = StartHomeZ1Thread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_home_Z2(self):
        self.threads = []
        client_thread = StartHomeZ2Thread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_home_X(self):
        self.threads = []
        client_thread = StartHomeXThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_home_Y(self):
        self.threads = []
        client_thread = StartHomeYThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_spin_drill_motor(self):
        self.threads = []
        client_thread = StartSpinDrillMotorThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_spin_pump(self):
        self.threads = []
        client_thread = StartSpinPumpThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_heater(self):
        self.threads = []
        client_thread = StartHeaterThread()
        self.threads.append(client_thread)
        client_thread.start() 