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

class SensorsStatusDisplay:

    def __init__(self, layout):
        # status names, and whether they are boolean or a value
        # Tuple (description, need_value, 
        #           green_limit, orange_limit, red_limit)
        # True for needing LEDS, and false for values
        self.status_list = [
            ("Senosrs HeartBeat", False),
            ("Motor HeartBeat", False),
            ("Core Sensors CPU Temp (degC)", True, 60, 75),
            ("Motor CPU Temp (degC)", True, 60, 75),
            ("Drill On", False),
            ("Heater On", False),
            ("Triac Level", True, 0.25, 0.75),
            ("Mission Time (H:M:S)", True, 80*60*60*1000, 100*60*60*1000),
            ("Sensors Round Trip Time (ms)", True, 300, 5000),
            ("Motor Round Trip Time (ms)", True, 300, 5000),
            ("Sensors Server Version", True, 300, 5000),
            ("Motor Server Version", True, 300, 5000),
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
                    self.values[i].setStyleSheet("font-weight: bold; color: '#17a2b8'")
                elif (v < self.status_list[i][3]):
                    self.values[i].setStyleSheet("font-weight: bold; color: '#ffc107'")
                else: 
                    self.values[i].setStyleSheet("font-weight: bold; color: '#dc3545'") 
        

    def update_sensors_status(self, response):
        if (response != None):
            self._update_bool(0, "Senosrs HeartBeat", True)
            for i in range(1, len(self.checkboxes)):
                self.checkboxes[i].setChecked(False)
            
            self._update_value(2, response.cpu_temperature_degC,
                                 "%0.2f [degC]", "Core Sensors CPU Temp (degC)", True)

            self._update_bool(4, "Drill On", response.drill_on)
            self._update_bool(5, "Heater On", response.heater_on)
            self._update_value(6, response.triac_level, "Triac Level", True)

            rtt_time = response.timestamp - response.request_timestamp
            self._update_value(8, rtt_time, "%0.2f [ms]", "Sensors Round Trip Time (ms)", True)
            self._update_value(10, response.server_version, 
                "%s", "Sensors Server Version", False)
            
        else:
            for c in self.checkboxes:
                c.setChecked(False)
