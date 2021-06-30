import sys
from urllib.request import urlopen

import logging

import grpc

from .generated import mission_control_pb2, mission_control_pb2_grpc

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer, Signal

from qt_material import apply_stylesheet

from datetime import datetime, timedelta
import time
import configparser

from . import mode_display, status_display, startup_diagnostics_display, limits_display
from . import hole_position_display

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
    done = Signal(object)
    def __init__(self, limit_displays):
        QtCore.QThread.__init__(self)
        self.limit_displays = limit_displays
        
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
                limits_response = stub.GetLimits (
                    mission_control_pb2.GetLimitRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                if limits_response != None:
                    for d in self.limit_displays:
                        d._updateLimitDisplay(limits_response)
            
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

        self.done.emit(response)
            

class EmergencyStopThread(QtCore.QThread):
    
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
            
        
class MainWindow(QtWidgets.QWidget):

    def _initEmergencyStop(self):
        self.emergency_button = QtWidgets.QPushButton('EMERGENCY STOP [ESC]', self)
        self.emergency_button.setIcon(QtGui.QIcon('./blueprint/Big_Red_Button.png'))
        self.emergency_button.setIconSize(QtCore.QSize(30,30))
        self.emergency_button.setMinimumHeight(75)
        self.main_grid_layout.addWidget(
            self.emergency_button, 0, 0, 1, 1)
        self.emergency_button.clicked.connect \
            (self.emergency_stop)

    def _initModeDisplay(self):
        self.mode_groupbox = QtWidgets.QGroupBox("Mode Selection")
        self.mode_layout = QtWidgets.QVBoxLayout()
        self.mode_groupbox.setLayout(self.mode_layout)
        self.main_grid_layout.addWidget(
            self.mode_groupbox, 1, 0, 2, 1)

        self.mode_display = mode_display.ModeDisplay(
            self.mode_layout)
  
    def _initStatusDisplay(self):
        self.status_groupbox = QtWidgets.QGroupBox("System Status")
        self.status_layout = QtWidgets.QVBoxLayout()
        self.status_groupbox.setLayout(self.status_layout)
        self.main_grid_layout.addWidget(
            self.status_groupbox, 4, 0, 10, 1)

        self.status_display = status_display.StatusDisplay(
            self.status_layout)

    def _initDiagnostics(self):
        self.startup_diagnostics_groupbox = QtWidgets.QGroupBox("P01 Startup and Diagnostics")
        self.diagnostics_layout = QtWidgets.QGridLayout()
        self.startup_diagnostics_groupbox.setLayout(self.diagnostics_layout)
        self.main_grid_layout.addWidget(
            self.startup_diagnostics_groupbox, 0, 1, 3, 5)

        self.startup_display = startup_diagnostics_display.StartupDiagnosticsDisplay(self.diagnostics_layout)

    def _initLimits(self):
        self.limits_groupbox = QtWidgets.QGroupBox("P01 Limits")
        self.limits_layout = QtWidgets.QFormLayout()
        self.limits_groupbox.setLayout(self.limits_layout)
        self.main_grid_layout.addWidget(
            self.limits_groupbox, 0, 6, 3, 5)

        self.limits_display = limits_display.LimitsDisplay(self.limits_layout)  
        self.limit_displays.append(self.limits_display)     

    def __init__(self):
        super(MainWindow, self).__init__()
        self.threads = []
        self.limit_displays = []
        self.main_grid_layout = QtWidgets.QGridLayout()
        self._initEmergencyStop()
        self._initModeDisplay()
        self._initStatusDisplay()
        self._initDiagnostics()
        self._initLimits()
        self._initHolePos()
        self.setLayout(self.main_grid_layout)
        
        self.heartbeat_timer=QTimer()
        self.heartbeat_timer.timeout.connect(self.onHeartBeat)
        self.startHeartBeatTimer()

    # def closeEvent(self, event):
    #     for th in self.threads:
    #         th.wait()
    #     event.accept() # let the window close

    def _initHolePos(self):
        self.hole_pos_groupbox = QtWidgets.QGroupBox("Rig Holes and Position")
        self.hole_pos_layout = QtWidgets.QGridLayout()
        self.hole_pos_groupbox.setLayout(self.hole_pos_layout)
        self.main_grid_layout.addWidget(
            self.hole_pos_groupbox, 4, 1, 10, 10)

        self.hole_pos_display = hole_position_display.HolePositionDisplay(
            self.hole_pos_layout
        )

    def emergency_stop(self):
        client_thread = EmergencyStopThread()
        self.threads.append(client_thread)
        client_thread.start()
        self.emergency_button.setText("ATTEMPTING EMERGENCY STOP [ESC]")

    def on_emergency_stop_done(self):
        pass

    def onHeartBeat(self):
        client_thread = RPiHeartBeat(self.limit_displays)
        client_thread.done.connect(self.on_heartbeat_received)
        self.threads.append(client_thread)
        client_thread.start()

    @QtCore.Slot(object)
    def on_heartbeat_received(self, response):
        if (response != None):
            self.mode_display.update_mode(response.mode)
        self.status_display.update_status(response)
        self.hole_pos_display.update_display(response)
            
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
    #apply_stylesheet(app, theme='light_blue.xml')
    apply_stylesheet(app, theme='dark_teal.xml')
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    window = MainWindow()
    window.resize(1500, 680)
    window.show()
    sys.exit(app.exec_())