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
from . import client_common
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
                response = stub.GetMajorModes (
                    mission_control_pb2.GetMajorModesRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
            self.done.emit(response)
        except Exception as e:
            info = f"[Error] {str(e)}"
            self.log.emit(info)

class ModeDisplay(QtWidgets.QWidget):
    def __init__(self, main_window, layout):
        self.threads = []
        self.modes = []
        self.main_window = main_window
        self.layout = layout
        
    def _initStatusWidgets(self):
        print("Initializing Status Widgets")
        self.mode_radios = []
        for i in range(len(self.modes)):
            b = QtWidgets.QRadioButton(self.mode_labels[i])
            self.mode_radios.append(b)
            b.toggled.connect(lambda:self._on_mode_change(b))
            self.layout.addWidget(self.mode_radios[i])
        
    @QtCore.Slot(object)
    def _on_modes_fetch_done(self, response):
        self.modes = response.modes
        self.mode_labels = response.mode_labels
        self._initStatusWidgets()

    @QtCore.Slot(object)
    def _on_mode_change(self, b):
        if b.isChecked() == True:
            timestamp = datetime.now()
            self.main_window.log(f"[{timestamp}] Attempting mode change to {b.text()}")
            client_thread = client_common.ModeChangeThread(self._get_button_mode(b))
            client_thread.log.connect(self.main_window.on_log)
            self.threads.append(client_thread)
            client_thread.start()
    
    def _get_button_mode(self, b):
        for i in range(len(self.mode_radios)):
            if self.mode_radios[i] == b:
                return self.modes[i]
        return 0
        
    def update_status(self, response):
        if response != None:
            if len(self.modes) == 0:
                client_thread = ModesFetchThread()
                self.threads.append(client_thread)
                client_thread.done.connect(self._on_modes_fetch_done)
                client_thread.log.connect(self.main_window.on_log)
                client_thread.start()
        
            mode = response.major_mode
            for i in range(len(self.modes)):
                if (self.modes[i] == mode):
                    self.mode_radios[i].setChecked(True)
                else:
                    self.mode_radios[i].setChecked(False)