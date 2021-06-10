"""
mode_display.py
The major mode display widget for the mission control client.
"""

__author__      = "Prakash Manandhar, and Marcellin Feasson"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar, and Marcellin Feasson"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Signal

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

class ModesFetchThread(QtCore.QThread):
    done = Signal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.GetMajorModes (
                    mission_control_pb2.GetMajorModesRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Major Modes received at: " + str(datetime.now()))
                print(response)
            self.done.emit(response)
        except Exception as e:
            info = f"Error connecting to Mission Control Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

class ModeDisplay(QtWidgets.QWidget):
    def __init__(self, layout):
        self.threads = []
        client_thread = ModesFetchThread()
        self.threads.append(client_thread)
        client_thread.done.connect(self._on_modes_fetch_done)
        client_thread.start()
        self.modes = []
        self.layout = layout
        layout.setSpacing(0.5)
        
    def _initStatusWidgets(self):
        print("Initializing Status Widgets")
        self.mode_radios = []
        for i in range(len(self.modes)):
            self.mode_radios.append(
                     QtWidgets.QRadioButton(self.mode_labels[i])
                 )
            self.layout.addWidget(self.mode_radios[i])
        self.layout.addStretch(5)

    @QtCore.Slot(object)
    def _on_modes_fetch_done(self, response):
        self.modes = response.modes
        self.mode_labels = response.mode_labels
        self._initStatusWidgets()

    def update_mode(self, mode):
        for i in range(len(self.modes)):
             if (self.modes[i] == mode):
                 self.mode_radios[i].setChecked(True)
             else:
                 self.mode_radios[i].setChecked(False)