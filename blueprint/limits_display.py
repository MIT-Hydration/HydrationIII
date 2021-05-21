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
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetAirGapThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetAirGap(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetAirGapThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetAirGap(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )


class SetMaxZ1Thread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetMaxZ1Travel(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetMaxZ1Thread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetMaxZ1Travel(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetLowerCurrentLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetLowerCurrentLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetLowerCurrentLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetLowerCurrentLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetUpperCurrentLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetUpperCurrentLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetUpperCurrentLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetUpperCurrentLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetLowerWOBLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetLowerWOBLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetLowerWOBLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetLowerWOBLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetUpperWOBLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetUpperWOBLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetUpperWOBLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetUpperWOBLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetLowerRPMLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetLowerRPMLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetLowerRPMLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetLowerRPMLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetUpperRPMLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetUpperRPMLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetUpperRPMLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetUpperRPMLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetZ1ServoTorqueLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetZ1ServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetZ1ServoTorqueLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetZ1ServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetZ2ServoTorqueLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetZ2ServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetZ2ServoTorqueLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetZ2ServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetXServoTorqueLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetXServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetXServoTorqueLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetXServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class SetYServoTorqueLimitThread(SetThread):

    def _get_response(self, stub, timestamp):
        return stub.SetYServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp, value = self.value),
                    timeout = GRPC_CALL_TIMEOUT )

class GetYServoTorqueLimitThread(GetThread):
    
    def _get_response(self, stub, timestamp):
        return stub.GetYServoTorqueLimit(
                    mission_control_pb2.LimitChangeRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

class LimitsDisplay:

    def __init__(self, layout):
        self.threads = []
        # Tuple (buttons display text, pointer to functions)     
        self.limits_list = [
            ("AIR GAP TO REGOLITH (in cm): ", self.set_air_gap, False, self.get_air_gap),
            ("MAX Z1 TRAVEL LENGTH  (in cm): ", self.set_max_Z1, False, self.get_max_Z1),  
            ("CURRENT LIMITS (in A) - Lower: ", self.set_current_limit_lower, True, self.get_current_limit_lower,
                " Upper: ", self.set_current_limit_upper, self.set_current_limit_upper), 
            ("WOB LIMIT (in N) - Lower: ", self.set_WOB_limit_lower, True, self.get_WOB_limit_lower,
                " Upper: ", self.set_WOB_limit_upper, self.get_WOB_limit_upper), 
            ("RPM LIMIT (in %) - Lower: ", self.set_RPM_limit_lower, True, self.get_RPM_limit_lower,
                " Upper: ", self.set_RPM_limit_upper, self.get_RPM_limit_upper), 
            ("Z1 SERVO TORQUE LIMIT (in %): ", self.set_Z1_servo_torque, True, self.get_Z1_servo_torque,
                "Z2 SERVO TORQUE LIMIT (in %): ", self.set_Z2_servo_torque, self.get_Z2_servo_torque),
            ("X SERVO TORQUE LIMIT (in %): ", self.set_X_servo_torque, True, self.get_X_servo_torque,
                "Y SERVO TORQUE LIMIT (in %): ", self.set_Y_servo_torque, self.get_Y_servo_torque),         
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
                partial(self.limits_list[i][5], edit1))
            edit2.setValidator(QtGui.QDoubleValidator())
            self.limits_list[i][3](edit1)
            self.limits_list[i][-1](edit2)

            label2 = QtWidgets.QLabel(self.limits_list[i][4])        
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
            self.limits_list[i][-1](edit1)
            
    def _initWidgets(self):
        for i in range(len(self.limits_list)):
            self._addLimits(i)      

    def set_air_gap(self, edit):
        self.threads = []
        client_thread = SetAirGapThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_air_gap(self, edit):
        client_thread = GetAirGapThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 

    def set_max_Z1(self, edit):
        self.threads = []
        client_thread = SetMaxZ1Thread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_max_Z1(self, edit):
        client_thread = GetMaxZ1Thread(edit)
        self.threads.append(client_thread)
        client_thread.start() 

    def set_current_limit_lower(self, edit):
        self.threads = []
        client_thread = SetLowerCurrentLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_current_limit_lower(self, edit):
        client_thread = GetLowerCurrentLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 

    def set_current_limit_upper(self, edit):
        self.threads = []
        client_thread = SetUpperCurrentLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_current_limit_upper(self, edit):
        client_thread = GetUpperCurrentLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 

    def set_WOB_limit_lower(self, edit):
        self.threads = []
        client_thread = SetLowerWOBLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_WOB_limit_lower(self, edit):
        client_thread = GetLowerWOBLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 
        
    def set_WOB_limit_upper(self, edit):
        self.threads = []
        client_thread = SetUpperWOBLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_WOB_limit_upper(self, edit):
        client_thread = GetUpperWOBLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 

    def set_RPM_limit_lower(self, edit):
        self.threads = []
        client_thread = SetLowerRPMLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_RPM_limit_lower(self, edit):
        client_thread = GetLowerRPMLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def set_RPM_limit_upper(self, edit):
        self.threads = []
        client_thread = SetUpperRPMLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_RPM_limit_upper(self, edit):
        client_thread = GetUpperRPMLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def set_Z1_servo_torque(self, edit):
        self.threads = []
        client_thread = SetZ1ServoTorqueLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_Z1_servo_torque(self, edit):
        client_thread = GetZ1ServoTorqueLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def set_Z2_servo_torque(self, edit):
        self.threads = []
        client_thread = SetZ2ServoTorqueLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_Z2_servo_torque(self, edit):
        client_thread = GetZ2ServoTorqueLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start()

    def set_X_servo_torque(self, edit):
        self.threads = []
        client_thread = SetXServoTorqueLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_X_servo_torque(self, edit):
        client_thread = GetXServoTorqueLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start()

    def set_Y_servo_torque(self, edit):
        self.threads = []
        client_thread = SetYServoTorqueLimitThread(float(edit.text()))
        self.threads.append(client_thread)
        client_thread.start()

    def get_Y_servo_torque(self, edit):
        client_thread = GetYServoTorqueLimitThread(edit)
        self.threads.append(client_thread)
        client_thread.start()
