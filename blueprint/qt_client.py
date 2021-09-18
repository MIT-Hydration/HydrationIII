import sys
from urllib.request import urlopen

import logging

import grpc

from .generated import mission_control_pb2, mission_control_pb2_grpc

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer, Signal

from qt_material import apply_stylesheet
from . import client_common

from datetime import datetime, timedelta
import time
import configparser

from . import mode_display, status_display, startup_diagnostics_display, limits_display
from . import hole_position_display, drillborehole_display
import blueprint

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
    log = Signal(object)
    limits_done = Signal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        limits_response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.HeartBeat (
                    mission_control_pb2.HeartBeatRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control HeartBeat received at: " + str(datetime.now()))
                print(response) #whats the response? the things in the HeartBeat in mission control returns?
                #self.log.emit("HeartBeat received at: " + str(datetime.now()))
                limits_response = stub.GetLimits (
                    mission_control_pb2.GetLimitRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                
        except Exception as e:
            info = f"Error connecting to Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            self.log.emit(info)

        self.done.emit(response) #what do these do? 
        self.limits_done.emit(limits_response)    

class EmergencyStopThread(QtCore.QThread):
    done = Signal(object)

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

        self.done.emit(response) 
        
class MainWindow(QtWidgets.QWidget):

    def _initEmergencyStop(self):
        self.emergency_button = QtWidgets.QPushButton('Emergency Stop [ESC]', self)
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

        self.mode_display = mode_display.ModeDisplay(self,
            self.mode_layout)
        self.heartbeat_receivers.append(self.mode_display)
  
    def _initStatusDisplay(self):
        self.status_groupbox = QtWidgets.QGroupBox("System Status")
        self.status_layout = QtWidgets.QVBoxLayout()
        self.status_groupbox.setLayout(self.status_layout)
        self.main_grid_layout.addWidget(
            self.status_groupbox, 4, 0, 10, 1)

        self.status_display = status_display.StatusDisplay(
            self.status_layout)
        self.heartbeat_receivers.append(self.status_display)
  

    def _initDiagnostics(self):
        self.startup_diagnostics_groupbox = QtWidgets.QGroupBox("P01 Startup and Diagnostics")
        
        self.major_mode_tab.addTab(
            self.startup_diagnostics_groupbox, "P01")
        self.startup_display = startup_diagnostics_display.StartupDiagnosticsDisplay(
            self, self.startup_diagnostics_groupbox)
        self.heartbeat_receivers.append(self.startup_display)

    def _initDiagnosticsBar(self):
        self.diagnostics_bar_groupbox = QtWidgets.QGroupBox(
            f"Log/Diagnostics (Client Version: {blueprint.HYDRATION_VERSION})")
        self.diagnostics_bar_layout = QtWidgets.QHBoxLayout()
        self.diagnostics_bar_groupbox.setLayout(self.diagnostics_bar_layout)
        self._log_display = QtWidgets.QPlainTextEdit()
        self._log_display.setMaximumBlockCount(100)
        self.diagnostics_bar_layout.addWidget(self._log_display, stretch=10)
        self._log_clear_button = QtWidgets.QPushButton("Clear Logs")
        self._log_clear_button.clicked.connect(self._clearLog)
        self.diagnostics_bar_layout.addWidget(self._log_clear_button, stretch=1)
        self._log_clear_alert = QtWidgets.QPushButton("Clear Alert")
        self._log_clear_alert.clicked.connect(self._clearAlert)
        self.diagnostics_bar_layout.addWidget(self._log_clear_alert, stretch=1)
        
        self.main_grid_layout.addWidget(
            self.diagnostics_bar_groupbox, 15, 0, 6, 11)
    
    @QtCore.Slot(object)
    def _clearLog(self):
        self._log_display.clear()

    @QtCore.Slot(object)
    def _clearAlert(self):
        timestamp = datetime.now()
        self.log(
            f"[{timestamp}] Clearing Alerts")
        client_thread = client_common.ClearAlert()
        client_thread.log.connect(self.on_log)
        self.threads.append(client_thread)
        client_thread.start()

    def log(self, text):
        self._log_display.insertPlainText(f"\n{text}")

    def _initLimits(self):
        self.limits_groupbox = QtWidgets.QGroupBox("P01 Limits")
        self.limits_layout = QtWidgets.QFormLayout()
        self.limits_groupbox.setLayout(self.limits_layout)
        self.main_grid_layout.addWidget(
            self.limits_groupbox, 0, 8, 3, 3)

        self.limits_display = limits_display.LimitsDisplay(self.limits_layout)  
        self.limit_receivers.append(self.limits_display)   

    def _initDrillBorehole(self):
        self.drillborehole_groupbox = QtWidgets.QGroupBox("P04 Drill Borehole")
        self.major_mode_tab.addTab(
            self.drillborehole_groupbox, "P04")

        self.drillborehole_display = drillborehole_display.DrillBoreholeDisplay(
            self, self.drillborehole_groupbox)

        self.heartbeat_receivers.append(self.drillborehole_display)
        
        
    def __init__(self):
        super(MainWindow, self).__init__()
        self.threads = []
        self.limit_receivers = []
        self.heartbeat_receivers = []

        self.main_grid_layout = QtWidgets.QGridLayout()
        self.major_mode_tab = QtGui.QTabWidget()
        self.main_grid_layout.addWidget(self.major_mode_tab, 0, 1, 3, 7)

        self._initEmergencyStop()
        self._initModeDisplay()
        self._initStatusDisplay()

        #self._initDiagnostics()
        #self._initDrillBorehole()
        
        self._initLimits()
        self._initHolePos()
        self._initDiagnosticsBar()
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
            self, self.hole_pos_layout
        )
        self.limit_receivers.append(self.hole_pos_display) 
        self.heartbeat_receivers.append(self.hole_pos_display) 

    def emergency_stop(self):
        client_thread = EmergencyStopThread()
        self.threads.append(client_thread)
        client_thread.done.connect(self.on_emergency_stop_done)
        client_thread.start()
        self.emergency_button.setText("Attempting Emergency Stop [ESC]")
        client_thread = client_common.RelayThread("Drill", False)
        self.threads.append(client_thread)
        client_thread.start() 
        client_thread = client_common.RelayThread("Heater", False)
        self.threads.append(client_thread)
        client_thread.start() 

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Escape):
            self.emergency_stop()
        return super().keyPressEvent(event)

    def on_emergency_stop_done(self):
        self.emergency_button.setText("Emergency Stop [ESC]")

    def onHeartBeat(self):
        client_thread = RPiHeartBeat()
        client_thread.done.connect(self.on_heartbeat_received)
        client_thread.log.connect(self.on_log)
        client_thread.limits_done.connect(self.on_limit_received)
        self.threads.append(client_thread)
        client_thread.start()


    @QtCore.Slot(object)
    def on_limit_received(self, response):
        for r in self.limit_receivers:
            r.update_limits(response)

    @QtCore.Slot(object)
    def on_heartbeat_received(self, response):
        if response != None:
            if response.major_mode == mission_control_pb2.MAJOR_MODE_DRILL_BOREHOLE:
                self.major_mode_tab.setCurrentIndex(1)
            else:
                self.major_mode_tab.setCurrentIndex(0)
        for r in self.heartbeat_receivers:
            try:
                r.update_status(response)
            except AttributeError as e:
                self.log("Missing attributte in update_status: " + str(e))
            except Exception as e:
                self.log(str(e))

    @QtCore.Slot(object)
    def on_log(self, text):
        self.log(text)

    def on_data_ready(self, data):
        print(data)
        self.list_widget.addItem(data)

    def startHeartBeatTimer(self):
        global HEARTBEAT_TIMEOUT
        self.heartbeat_timer.start(HEARTBEAT_TIMEOUT)
        
    def endHeartBeatTimer(self):
        self.heartbeat_timer.stop()

    def closeEvent(self, event):
        for th in self.threads:
            th.wait()
        event.accept() # let the window close
        
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    #apply_stylesheet(app, theme='light_blue.xml')
    apply_stylesheet(app, theme='dark_teal.xml')
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    window = MainWindow()
    window.resize(1500, 680)
    window.show()
    sys.exit(app.exec())