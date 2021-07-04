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
from .generated import mission_control_pb2_grpc
from .generated import mission_control_pb2 as mcpb

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

    def __init__(self, group_box):
        # Tuple (buttons display text, pointer to functions)     
        self.labels = [
            [mcpb.STARTUP_IDLE, QtWidgets.QLabel("1. Idle")],
            [mcpb.STARTUP_MISSION_CLOCK_STARTED, QtWidgets.QLabel("2. Mission Clock Started")],
            [mcpb.STARTUP_HOMING_Z1, QtWidgets.QLabel("3. Homing Z1")],
            [mcpb.STARTUP_HOME_Z1_COMPLETED, QtWidgets.QLabel("4. Home Z1 Completed")],
            [mcpb.STARTUP_HOMING_Y, QtWidgets.QLabel("4. Homing Y")],
            [mcpb.STARTUP_HOME_Y_COMPLETED, QtWidgets.QLabel("5. Home Y Completed")],
        ]
        self.threads = []
        self.group_box = group_box
        self.layout = QtWidgets.QVBoxLayout()
        self.group_box.setLayout(self.layout)
        self._initWidgets()
        
    def _initWidgets(self):
        for l in self.labels:
            self.layout.addWidget(l[1])
        self.button_layout = QtWidgets.QHBoxLayout()
        self.next_button = QtWidgets.QPushButton("Next")
        self.restart_button = QtWidgets.QPushButton("Restart")
        self.button_layout.addWidget(self.next_button)
        self.button_layout.addWidget(self.restart_button)
        self.layout.addLayout(self.button_layout)

    def update_status(self, response):
        if (response != None):
            for l in self.labels:
                if l[0] == response.state:
                    l[1].setStyleSheet("font-style: italic; color: '#ffc107'")
                else:
                    l[1].setStyleSheet("font-style: normal; color: '#ffffff'")

    def start_mission_clock(self):
        client_thread = StartMissionClockThread()
        self.threads.append(client_thread)
        client_thread.start()      

    def start_home_Z1(self):
        client_thread = StartHomeZ1Thread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_home_Z2(self):
        client_thread = StartHomeZ2Thread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_home_X(self):
        client_thread = StartHomeXThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_home_Y(self):
        client_thread = StartHomeYThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_spin_drill_motor(self):
        client_thread = StartSpinDrillMotorThread()
        self.threads.append(client_thread)
        client_thread.start()

    def stop_spin_drill_motor(self):
        client_thread = StopSpinDrillMotorThread()
        self.threads.append(client_thread)
        client_thread.start()  

    def start_spin_pump(self):
        client_thread = StartSpinPumpThread()
        self.threads.append(client_thread)
        client_thread.start()

    def stop_spin_pump(self):
        client_thread = StopSpinPumpThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def start_heater(self):
        client_thread = StartHeaterThread()
        self.threads.append(client_thread)
        client_thread.start()
   
    def stop_heater(self):
        client_thread = StopHeaterThread()
        self.threads.append(client_thread)
        client_thread.start() 