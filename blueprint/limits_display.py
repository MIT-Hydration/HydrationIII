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

class SetAirGapThread(QtCore.QThread):
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
                response = stub.SetAirGap(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

class LimitsDisplay:

    def __init__(self, layout):
        # Tuple (buttons display text, pointer to functions)     
        self.limits_list = [
            ("AIR GAP TO REGOLITH (in cm): ", self.set_air_gap, False),
            ("MAX Z1 TRAVEL LENGTH  (in cm): ", self.set_max_Z1, False),  
            ("CURRENT LIMITS (in A) - Lower: ", self.set_current_limit_lower, True,
                " Upper: ", self.set_current_limit_upper), 
            ("WOB LIMIT (in N) - Lower: ", self.set_WOB_limit_lower, True,
                " Upper: ", self.set_WOB_limit_upper), 
            ("RPM LIMIT (in %) - Lower: ", self.set_RPM_limit_lower, True,
                " Upper: ", self.set_RPM_limit_upper), 
            ("Z1 SERVO TORQUE LIMIT (in %): ", self.set_Z1_servo_torque, True,
                "Z2 SERVO TORQUE LIMIT (in %): ", self.set_Z2_servo_torque),
            ("X SERVO TORQUE LIMIT (in %): ", self.set_X_servo_torque, True,
                "Y SERVO TORQUE LIMIT (in %): ", self.set_Y_servo_torque),         
        ]
        
        self.layout = layout
        self._initWidgets()
        layout.setSpacing(0.5)

    def _addLimits(self, i):
        label1 = QtWidgets.QLabel(self.limits_list[i][0])
        if (self.limits_list[i][2]):
            edit1 = QtWidgets.QLineEdit()
            edit1.editingFinished.connect(
                partial(self.limits_list[i][1], edit1))
            edit1.setValidator(QtGui.QDoubleValidator())
            edit2 = QtWidgets.QLineEdit()
            edit2.editingFinished.connect(
                partial(self.limits_list[i][4], edit1))
            edit2.setValidator(QtGui.QDoubleValidator())
            
            label2 = QtWidgets.QLabel(self.limits_list[i][3])        
            hboxlayout = QtWidgets.QHBoxLayout()

            hboxlayout.addWidget(edit1)
            hboxlayout.addWidget(label2)
            hboxlayout.addWidget(edit2)

            self.layout.addRow(label1, hboxlayout)
        else:
            edit1 = QtWidgets.QLineEdit()
            self.layout.addRow(label1, edit1)
            edit1.editingFinished.connect(
                partial(self.limits_list[i][1], edit1))
            edit1.setValidator(QtGui.QDoubleValidator())
            
    def _initWidgets(self):
        for i in range(len(self.limits_list)):
            self._addLimits(i)      

    def set_air_gap(self, air_gap):
        self.threads = []
        client_thread = SetAirGapThread(float(air_gap.text()))
        self.threads.append(client_thread)
        client_thread.start() 

    def set_max_Z1(self, max_Z1):
        self.threads = []

    def set_current_limit_lower(self, current_limit_lower):
        self.threads = []

    def set_current_limit_upper(self, current_limit_upper):
        self.threads = []

    def set_WOB_limit_lower(self, WOB_limit_lower):
        print("I am here!")
        print(WOB_limit_lower.text())
        
    def set_WOB_limit_upper(self, WOB_limit_upper):
        self.threads = []

    def set_RPM_limit_lower(self, RPM_limit_lower):
        self.threads = []

    def set_RPM_limit_upper(self, RPM_limit_upper):
        self.threads = []

    def set_Z1_servo_torque(self, Z1_servo_torque):
        self.threads = []

    def set_Z2_servo_torque(self, Z2_servo_torque):
        self.threads = []

    def set_X_servo_torque(self, X_servo_torque):
        self.threads = []

    def set_Y_servo_torque(self, Y_servo_torque):
        self.threads = []