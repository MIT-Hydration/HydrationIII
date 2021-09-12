"""
relay_triac_control_display.py
Control the relay and triac from the front end.
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

from PySide6 import QtCore, QtWidgets, QtGui

from datetime import datetime, timedelta
import time

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

class RelayTriacControl:

    def __init__(self, groupbox):
        self.groupbox = groupbox
        self.layout = QtWidgets.QVBoxLayout()
        self.groupbox.setLayout(self.layout)
        self.layout.addWidget(QtWidgets.QLabel("Drill"))
        self.drill_on_button = QtWidgets.QPushButton("Drill On")
        self.drill_off_button = QtWidgets.QPushButton("Drill Off")
        self.layout.addWidget(drill_on_button)
        self.layout.addWidget(drill_off_button)
        self.layout.addWidget(QtWidgets.QLabel("Heater"))
        self.heater_on_button = QtWidgets.QPushButton("Heater On")
        self.heater_off_button = QtWidgets.QPushButton("Heater Off")
        self.layout.addWidget(heater_on_button)
        self.layout.addWidget(heater_off_button)
        self.layout.addWidget(QtWidgets.QLabel("Triac [0 to 1]"))
        
        self.triac_level_textbox = QtWidgets.QLineEdit("0.0")
        self.set_triac_button = QtWidgets.QPushButton("Set Triac")
        self.layout.addWidget(triac_level_textbox)
        self.layout.addWidget(set_triac_button)
        
        
    def _update_bool(self, i, name, check_value):
        if (self.status_list[i][0] != name):
            raise IndexError(f"{name} not at right index")
        self.checkboxes[i].setChecked(check_value)
    
    def _update_value(self, i, v, fstr, name, check_value):
        if (self.status_list[i][0] != name):
            raise IndexError(f"{name} not at right index")
        self.checkboxes[i].setChecked(True)
        if (self.status_list[i][1]):
            self.values[i].setText(fstr%v)
            if check_value:
                if (v < self.status_list[i][2]):
                    self.values[i].setStyleSheet("font-weight: bold; color: '#17a2b8'")
                elif (v < self.status_list[i][3]):
                    self.values[i].setStyleSheet("font-weight: bold; color: '#ffc107'")
                else: 
                    self.values[i].setStyleSheet("font-weight: bold; color: '#dc3545'") 
        

    def update_status(self, response):
        if (response != None):
            self._update_bool(0, "System HeartBeat", True)
            for i in range(1, len(self.checkboxes)):
                self.checkboxes[i].setChecked(False)
            
            self._update_bool(1, "Z1 (Drill) servo", response.zdrill_servo_moving)
            self._update_bool(2, "Z2 (Drill) servo", response.zheater_servo_moving)
            self._update_bool(3, "Y servo", response.y_servo_moving)
            
            self._update_value(4, response.cpu_temperature_degC,
                                 "%0.2f [degC]", "CPU Temp (degC)", True)
            mission_time = timedelta(milliseconds=int(response.mission_time_ms / 1000)*1000)
            self._update_value(5, str(mission_time), "%s", "Mission Time (H:M:S)", False)
            rtt_time = response.timestamp - response.request_timestamp
            self._update_value(6, rtt_time, "%0.2f [ms]", "Round Trip Time (ms)", True)
            self._update_value(7, response.server_version, 
                "%s", "Server Version", False)
            
            
        else:
            for c in self.checkboxes:
                c.setChecked(False)

