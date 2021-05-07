"""
system_status_display.py
The system status display widget for the mission control client.
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

from datetime import datetime, timedelta
import time

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

class StatusDisplay:

    def __init__(self, layout):
        # status names, and whether they are boolean or a value
        # Tuple (description, need_value, 
        #           green_limit, orange_limit, red_limit)
        # True for needing LEDS, and false for values
        self.status_list = [
            ("System HeartBeat", False),
            ("AC supply (VRms)", True, 120, 130),         
            ("24VDC bus", False),
            ("75VDC bus", False),
            ("Z1 (Drill) servo", False),
            ("Z2 (Water) servo", False),
            ("X servo", False),
            ("Y servo", False),
            ("Drill motor (0->1)", True, 0.8, 1.1),
            ("Heater (0->1)", True, 0.8, 1.1),
            ("Pump", False),
            ("Current (A)", True, 6.0, 8.5),
            ("CPU Temp (degC)", True, 60, 75),
            ("Mission Time (H:M:S)", True, 80*60*60*1000, 100*60*60*1000),
            ("Round Trip Time (ms)", True, 300, 5000),
        ]
        self.checkboxes = [None] * len(self.status_list)
        self.values = [None] * len(self.status_list)
        self.layout = layout
        self.layout.setSpacing(0.5)
        self._initStatusWidgets()
        
    def _addStatus(self, i):
        h_layout = QtWidgets.QHBoxLayout()
        description = self.status_list[i][0]
        if self.status_list[i][1]:
            description += ":     "
        checkbox = QtWidgets.QCheckBox(description)
        self.checkboxes[i] = checkbox
        h_layout.addWidget(checkbox)
        if self.status_list[i][1]:
            self.values[i] = QtWidgets.QLabel("N/A")
            h_layout.addWidget(self.values[i])
        self.layout.addLayout(h_layout)

    def _initStatusWidgets(self):
        for i in range(len(self.status_list)):
            self._addStatus(i)

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
                    self.values[i].setStyleSheet("color: green")
                elif (v < self.status_list[i][3]):
                    self.values[i].setStyleSheet("color: orange")
                else: 
                    self.values[i].setStyleSheet("color: red") 
        

    def update_status(self, response):
        if (response != None):
            self._update_bool(0, "System HeartBeat", True)
            for i in [1, 2, 3, 4, 5, 8, 9, 10, 11]:
                self.checkboxes[i].setChecked(False)
            
            self._update_bool(6, "X servo", response.x_servo_moving)
            self._update_bool(7, "Y servo", response.y_servo_moving)
            
            self._update_value(12, response.cpu_temperature_degC,
                                 "%0.2f [degC]", "CPU Temp (degC)", True)
            mission_time = timedelta(milliseconds=int(response.mission_time_ms / 1000)*1000)
            self._update_value(13, str(mission_time), "%s", "Mission Time (H:M:S)", False)
            rtt_time = response.timestamp - response.request_timestamp
            self._update_value(14, rtt_time, "%0.2f [ms]", "Round Trip Time (ms)", True)
            
        else:
            for c in self.checkboxes:
                c.setChecked(False)

