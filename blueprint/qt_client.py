import sys
from urllib.request import urlopen

import logging

import grpc

from .generated import mission_control_pb2, mission_control_pb2_grpc

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QDateTime

from QLed import QLed

from datetime import datetime, timedelta
import time
import configparser

from . import mode_display, status_display, startup_diagnostics_display

config = configparser.ConfigParser()
config.read('config.ini')

RPI_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

HEARTBEAT_TIMEOUT   = \
    config.getint('Network', 'HeartbeatTimeout')
GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')


class RPiHeartBeat(QtCore.QThread):
    heartbeat_done = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.HeartBeat (
                    mission_control_pb2.HeartBeatRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi HeartBeat received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.heartbeat_done.emit(response)


class EmergencyStopThread(QtCore.QThread):
    command_done = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.EmergencyStop (
                    mission_control_pb2.EmergencyStopRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)

class MainWindow(QtWidgets.QWidget):

    def _initEmergencyStop(self):
        self.emergency_button = QtWidgets.QPushButton('EMERGENCY STOP [ESC]', self)
        self.emergency_button.setIcon(QtGui.QIcon('./blueprint/Big_Red_Button.png'))
        self.emergency_button.setIconSize(QtCore.QSize(50,50))
        self.emergency_button.setMinimumHeight(75)
        self.main_grid_layout.addWidget(
            self.emergency_button, 0, 0, 1, 1)
        self.emergency_button.clicked.connect \
            (self.emergency_stop)

    
    def _initStatusDisplay(self):
        self.status_groupbox = QtWidgets.QGroupBox("System Status")
        self.status_layout = QtWidgets.QVBoxLayout()
        self.status_groupbox.setLayout(self.status_layout)
        self.main_grid_layout.addWidget(
            self.status_groupbox, 3, 0, 2, 1)

        self.status_display = status_display.StatusDisplay(
            self.status_layout)

    def _initDiagnostics(self):
        self.startup_diagnostics_groupbox = QtWidgets.QGroupBox("P01 Startup and Diagnostics")
        layout = QtWidgets.QVBoxLayout()
        self.startup_diagnostics_groupbox.setLayout(layout)
        self.main_grid_layout.addWidget(
            self.startup_diagnostics_groupbox, 0, 1, 3, 5)

        self.startup_display = startup_diagnostics_display.StartupDiagnosticsDisplay(layout)

    def _initModeDisplay(self):
        self.mode_groupbox = QtWidgets.QGroupBox("Mode Selection")
        self.mode_layout = QtWidgets.QVBoxLayout()
        self.mode_groupbox.setLayout(self.mode_layout)
        self.main_grid_layout.addWidget(
            self.mode_groupbox, 1, 0, 2, 1)

        self.mode_display = mode_display.ModeDisplay(
            self.mode_layout)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_grid_layout = QtWidgets.QGridLayout()
        self._initEmergencyStop()
        self._initModeDisplay()
        self._initStatusDisplay()
        self._initDiagnostics()
        self.setLayout(self.main_grid_layout)
        
        self.heartbeat_timer=QTimer()
        self.heartbeat_timer.timeout.connect(self.onHeartBeat)
        self.startHeartBeatTimer()

    def emergency_stop(self):
        self.threads = []
        client_thread = EmergencyStopThread()
        self.threads.append(client_thread)
        client_thread.start()
        self.emergency_button.setText("ATTEMPTING EMERGENCY STOP [ESC]")

    def on_emergency_stop_done(self):
        pass

    def onHeartBeat(self):
        self.threads = []
        client_thread = RPiHeartBeat()
        client_thread.heartbeat_done.connect(self.on_heartbeat_received)
        self.threads.append(client_thread)
        client_thread.start()

    def on_heartbeat_received(self, response):
        if (response != None):
            self.mode_display.update_mode(response.mode)
        self.status_display.update_status(response)
            
    def on_data_ready(self, data):
        print(data)
        self.list_widget.addItem(data)

    def startHeartBeatTimer(self):
        global HEARTBEAT_TIMEOUT
        self.heartbeat_timer.start(HEARTBEAT_TIMEOUT)
        
    def endHeartBeatTimer(self):
        self.heartbeat_timer.stop()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(1500, 740)
    window.show()
    sys.exit(app.exec_())