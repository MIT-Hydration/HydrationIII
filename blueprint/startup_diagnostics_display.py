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
from PySide6.QtCore import QTimer, Signal

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

class StartupNextThread(QtCore.QThread):    
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
                response = stub.StartupNext (
                    mcpb.EmergencyStopRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
                self.done.emit(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            self.log.emit(info)

class RestartThread(QtCore.QThread):    
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
                response = stub.EmergencyStop (
                    mcpb.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
                self.done.emit(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            self.log.emit(info)

class StartupDiagnosticsDisplay:

    def __init__(self, main_window, group_box):
        # Tuple (buttons display text, pointer to functions)     
        self.labels = [
            [mcpb.STARTUP_IDLE, QtWidgets.QLabel("1. Idle")],
            [mcpb.STARTUP_MISSION_CLOCK_STARTED, QtWidgets.QLabel("2. Mission Clock Started")],
            [mcpb.STARTUP_HOMING_Z1, QtWidgets.QLabel("3. Homing Z1")],
            [mcpb.STARTUP_HOME_Z1_COMPLETED, QtWidgets.QLabel("4. Home Z1 Completed")],
            [mcpb.STARTUP_HOMING_Z2, QtWidgets.QLabel("5. Homing Z2")],
            [mcpb.STARTUP_HOME_Z2_COMPLETED, QtWidgets.QLabel("6. Home Z2 Completed")],
            [mcpb.STARTUP_HOMING_Y, QtWidgets.QLabel("5. Homing Y")],
            [mcpb.STARTUP_HOME_Y_COMPLETED, QtWidgets.QLabel("6. Home Y Completed")],
        ]
        self.threads = []
        self.group_box = group_box
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout()
        self.group_box.setLayout(self.layout)
        self._initWidgets()
        
    def _initWidgets(self):
        i = 0
        for l in self.labels:
            if i%2 == 0:
                h_layout = QtWidgets.QHBoxLayout()
                h_layout.addWidget(l[1])
            else:
                h_layout.addWidget(l[1])
                self.layout.addLayout(h_layout)
            i += 1
        self.button_layout = QtWidgets.QHBoxLayout()
        self.next_button = QtWidgets.QPushButton("Next")
        self.next_button.clicked.connect(
            partial(self.next_button.setStyleSheet,"font-style: italic; color: '#ffc107'"))
        self.next_button.clicked.connect(self._next)
            
        self.restart_button = QtWidgets.QPushButton("Restart")
        self.restart_button.clicked.connect(self._restart)
        self.restart_button.clicked.connect(
            partial(self.restart_button.setStyleSheet,"font-style: italic; color: '#ffc107'"))
        
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
            if (response.state == mcpb.STARTUP_HOMING_Z1) or \
                    (response.state == mcpb.STARTUP_HOMING_Y) or \
                    (response.state == mcpb.STARTUP_HOME_Y_COMPLETED):
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)

            if (response.state == mcpb.STARTUP_HOME_Y_COMPLETED):
                self.next_button.setText("Goto P04 Drill Borehole")
            else:
                self.next_button.setText("Next")

    @QtCore.Slot(object)
    def _next(self):
        client_thread = StartupNextThread()
        self.threads.append(client_thread)
        client_thread.done.connect(self.on_done)
        client_thread.log.connect(self.log)
        client_thread.start()

    @QtCore.Slot(object)
    def _restart(self):
        client_thread = RestartThread()
        self.threads.append(client_thread)
        client_thread.done.connect(self.on_done)
        client_thread.log.connect(self.log)
        client_thread.start()    

    @QtCore.Slot(object)
    def on_done(self, response):
        if (response.status == mcpb.INVALID_STATE):
            self.main_window.log(f"[{str(datetime.now())}] Invalid State for Startup")
        self.next_button.setStyleSheet("font-style: normal; color: '#1de9b6'")
        self.restart_button.setStyleSheet("font-style: normal; color: '#1de9b6'")

    @QtCore.Slot(object)
    def log(self, message):
        self.main_window.log(message)
    