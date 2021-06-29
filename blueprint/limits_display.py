"""
limits_display.py
The P01 panel for limits display for the mission control client.
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

class SetThread(QtCore.QThread):
    def __init__(self, value):
        QtCore.QThread.__init__(self)
        self.value = value
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            print(f"Setting value {self.value} at " + str(datetime.now()))
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = self._get_response(stub, timestamp)
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
    
    def _get_response(self, stub, timestamp):
        return stub.SetAirGap(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetThread(QtCore.QThread):
    def __init__(self, edit):
        QtCore.QThread.__init__(self)
        self.edit = edit
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            print(f"Getting value at " + str(datetime.now()))
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = response = self._get_response(stub, timestamp)
                self.edit.setText(str(response.value))
                print(response)
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

    def _get_response(self, stub, timestamp):
        return stub.GetAirGap(
                    mission_control_pb2.GetLimitRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class LimitsDisplay:

    def __init__(self, layout):
        self.threads = []
        self.layout = layout
        self._initWidgets()

    def _initWidgets(self):
        self.air_gap_edit = QtWidgets.QLineEdit()
        self.max_z1_edit = QtWidgets.QLineEdit()
        self.ice_start_edit = QtWidgets.QLineEdit()
        self.save_button = QtWidgets.QPushButton("Set Limits")
        
        self.layout.addRow(QtWidgets.QLabel("Air Gap to Regolith [m]: "), self.air_gap_edit)
        self.layout.addRow(QtWidgets.QLabel("Max Z1 (Drill Travel) [m]: "), self.max_z1_edit)
        self.layout.addRow(QtWidgets.QLabel("Ice Start Depth [m]: "), self.ice_start_edit)
        self.layout.addRow(self.save_button)

    def _updateDisplay(self, stub, timestamp, timeout):
        response = stub.GetLimits (
                    mission_control_pb2.GetLimitRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
        self.air_gap_edit.text = reponse.air_gap
        
        