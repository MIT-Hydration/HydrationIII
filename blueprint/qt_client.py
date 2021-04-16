import sys
from urllib.request import urlopen

import logging

import grpc

from .generated import echo_pb2
from .generated import echo_pb2_grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QDateTime

from QLed import QLed

from datetime import datetime, timedelta
import time
import configparser

from . import mode_display, status_display

config = configparser.ConfigParser()
config.read('config.ini')

RPI_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

HEARTBEAT_TIMEOUT   = \
    config.getint('Network', 'HeartbeatTimeout')
GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.pyqtSignal(object)

    def __init__(self, url):
        QtCore.QThread.__init__(self)
        self.url = url

    def run(self):
        try:
            info = urlopen(self.url).info()   
        except:
            info = f"Error opening URL: {self.url}"
        self.data_downloaded.emit('%s\n%s' % (self.url, info))

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


class RPiFanThread(QtCore.QThread):
    fan_done = QtCore.pyqtSignal(object)
    state = False

    def __init__(self, state):
        QtCore.QThread.__init__(self)
        self.state = state
        
    def run(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.FanCommand (
                    mission_control_pb2.FanCommandRequest(
                        request_timestamp = timestamp, fan_on = self.state),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi FanCommandResponse received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.fan_done.emit(response)

class RPiCommandThread(QtCore.QThread):
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
                response = stub.StartMissionClock (
                    mission_control_pb2.StartMissionClockRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi Start Mission Control Command received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.command_done.emit(response)


class RPiServerThread(QtCore.QThread):
    echo_done = QtCore.pyqtSignal(object)

    def __init__(self, echo_text):
        QtCore.QThread.__init__(self)
        self.echo_text = echo_text

    def run(self):
        global RPI_IP_ADDRESS_PORT
        try:
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = echo_pb2_grpc.EchoStub(channel)
                response = stub.Reply(echo_pb2.EchoRequest(message=self.echo_text))
                info = "Echo client received: " + response.message   
        except:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}"
        self.echo_done.emit(f'Response from {RPI_IP_ADDRESS_PORT}\n{info}')

class MainWindow(QtWidgets.QWidget):

    def _initEmergencyStop(self):
        self.emergency_button = QtWidgets.QPushButton('EMERGENCY STOP [ESC]', self)
        self.emergency_button.setIcon(QtGui.QIcon('./blueprint/Big_Red_Button.png'))
        self.emergency_button.setIconSize(QtCore.QSize(50,50))
        self.emergency_button.setMinimumHeight(75)
        self.main_grid_layout.addWidget(
            self.emergency_button, 0, 0, 1, 1)

    
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

        self.start_mission_clock_button = \
             QtWidgets.QPushButton("Start Mission Clock")
        self.start_mission_clock_button.setMinimumWidth(1000)
        layout.addWidget(
            self.start_mission_clock_button)
        self.start_mission_clock_button.clicked.connect \
            (self.start_mission_clock)

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

    def start_download(self):
        urls = ['http://google.com', 'http://twitter.com', 'http://yandex.ru',
                'http://stackoverflow.com/', 'http://www.youtube.com/'
                ]
        self.threads = []
        for url in urls:
            downloader = DownloadThread(url)
            downloader.data_downloaded.connect(self.on_data_ready)
            self.threads.append(downloader)
            downloader.start()

    def start_echo(self):
        self.threads = []
        client_thread = RPiServerThread(self.echo_textedit.toPlainText())
        client_thread.echo_done.connect(self.on_data_ready)
        self.threads.append(client_thread)
        client_thread.start()

    def start_mission_clock(self):
        self.threads = []
        client_thread = RPiCommandThread()
        self.threads.append(client_thread)
        client_thread.start()

    def set_fan(self, state):
        self.threads = []
        client_thread = RPiFanThread(state)
        client_thread.fan_done.connect(self.on_fan_done)
        self.threads.append(client_thread)
        client_thread.start()

    def turn_fan_on(self):
        self.set_fan(True)
    
    def turn_fan_off(self):
        self.set_fan(False)

    def on_fan_done(self):
        return

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