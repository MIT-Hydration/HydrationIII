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

from PySide6 import QtCore, QtWidgets, QtGui

from datetime import datetime, timedelta
import time
import configparser

from functools import partial

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
            
class StartHomeZ1Thread(QtCore.QThread):    
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

class StartHomeZ2Thread(QtCore.QThread):    
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
            
class StartHomeXThread(QtCore.QThread):    
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
            
class StartHomeYThread(QtCore.QThread):    
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
            
class StartSpinDrillMotorThread(QtCore.QThread):    
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
            
class StopSpinDrillMotorThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StopSpinDrillMotor (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
class StartSpinPumpThread(QtCore.QThread):
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

class StopSpinPumpThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StopSpinPump (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

class StartHeaterThread(QtCore.QThread):
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

class StopHeaterThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.StopHeater (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

def _changeStyle(button):
    button.setStyleSheet("color: '#dc3545'")
    #button.setText(button.text() + " [x]")
    #button.setChecked(True)

class StartupDiagnosticsDisplay:

    def __init__(self, layout):
        # Tuple (buttons display text, pointer to functions)     
        self.startup_list = [
            ("Start mission clock", self.start_mission_clock),
            ("Home Z1 axis servo", self.start_home_Z1),  
            ("Home Z2 axis servo", self.start_home_Z2), 
            ("Home X axis servo", self.start_home_X), 
            ("Home Y axis servo", self.start_home_Y), 
            ("Start Spin Drill motor", self.start_spin_drill_motor),
            ("Stop Spin Drill motor", self.stop_spin_drill_motor), 
            ("Start Spin pump", self.start_spin_pump),
            ("Stop Spin pump", self.stop_spin_pump), 
            ("Start heater", self.start_heater),
            ("Stop heater", self.stop_heater),        
        ]
        
        self.buttons = [None] * len(self.startup_list)
        self.layout = layout
        self._initWidgets()

    def _initWidgets(self):
        i = 0
        line = 0
        while (i < len(self.startup_list)):
            if (("Start" in self.startup_list[i][0]) and ("Stop" in self.startup_list[i+1][0])):
                sub1 = self.startup_list[i][0].replace("Start", "")
                sub2 = self.startup_list[i+1][0].replace("Stop", "")
                if (sub1 == sub2):
                    self.buttons[i] = QtWidgets.QPushButton(self.startup_list[i][0])
                    self.layout.addWidget(self.buttons[i], line, 0)
                    self.buttons[i].clicked.connect(self.startup_list[i][1])
                    self.buttons[i].clicked.connect(partial(_changeStyle, self.buttons[i]))
                    self.buttons[i+1] = QtWidgets.QPushButton(self.startup_list[i+1][0])
                    self.layout.addWidget(self.buttons[i+1], line, 1)
                    self.buttons[i+1].clicked.connect(self.startup_list[i+1][1])
                    self.buttons[i+1].clicked.connect(partial(_changeStyle, self.buttons[i+1]))
                    i += 2
                    line += 1
            else:
                    self.buttons[i] = QtWidgets.QPushButton(self.startup_list[i][0])
                    self.layout.addWidget(self.buttons[i], line, 0, 1, 2)
                    self.buttons[i].clicked.connect(self.startup_list[i][1])
                    self.buttons[i].clicked.connect(partial(_changeStyle, self.buttons[i]))
                    i += 1
                    line += 1
        self.layout.rowStretch(5)

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

    def stop_spin_drill_motor(self):
        self.threads = []
        client_thread = StopSpinDrillMotorThread()
        self.threads.append(client_thread)
        client_thread.start()  

    def start_spin_pump(self):
        self.threads = []
        client_thread = StartSpinPumpThread()
        self.threads.append(client_thread)
        client_thread.start()

    def stop_spin_pump(self):
        self.threads = []
        client_thread = StopSpinPumpThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_heater(self):
        self.threads = []
        client_thread = StartHeaterThread()
        self.threads.append(client_thread)
        client_thread.start()
   
    def stop_heater(self):
        self.threads = []
        client_thread = StopHeaterThread()
        self.threads.append(client_thread)
        client_thread.start() 