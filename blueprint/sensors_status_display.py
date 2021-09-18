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
import time, numpy

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

class SensorsStatusDisplay:

    def __init__(self, groupbox):
        # status names, and whether they are boolean or a value
        # Tuple (description, need_value, 
        #           green_limit, orange_limit, red_limit)
        # True for needing LEDS, and false for values
        self.status_list = [
            ("Sens HeartBeat", False),
            ("Motor HeartBeat", False),
            ("Sens CPU T", True, 60, 75),
            ("Motor CPU T", True, 60, 75),
            ("Sens Ser Ver", True, 300, 5000),
            ("Motor Ser Ver", True, 300, 5000),
            ("Mission Time (H:M:S)", True, 80*60*60*1000, 100*60*60*1000),
            ("Sensors RTT", True, 300, 5000),
            ("Motor RTT", True, 300, 5000),
            ("Drill On", False),
            ("Heater On", False),
            ("Triac Level", True, 0.25, 0.75),
            ("WOB Drill", True, 100, 140),
            ("WOB Heater", True, 30, 50),
            ("Current", True, 6000, 8000),
            ("Accel", True, 1.2, 4.0),
        ]
        self.groupbox = groupbox
        self.checkboxes = [None] * len(self.status_list)
        self.values = [None] * len(self.status_list)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout_left = QtWidgets.QVBoxLayout()
        self.layout_mid = QtWidgets.QVBoxLayout()
        self.layout_right = QtWidgets.QVBoxLayout()
        
        self.layout.addLayout(self.layout_left)
        self.layout_left.addItem(QtWidgets.QSpacerItem(400, 0, QtWidgets.QSizePolicy.Fixed))
        
        self.layout.addLayout(self.layout_mid)
        self.layout_mid.addItem(QtWidgets.QSpacerItem(400, 0, QtWidgets.QSizePolicy.Fixed))
        
        self.layout.addLayout(self.layout_right)
        self.layout_right.addItem(QtWidgets.QSpacerItem(400, 0, QtWidgets.QSizePolicy.Fixed))
        
        self.groupbox.setLayout(self.layout)
        self._initStatusWidgets()
        
    def _addStatus(self, i, layout):
        h_layout = QtWidgets.QHBoxLayout()
        description = self.status_list[i][0]
        if self.status_list[i][1]:
            description += ":     "
        checkbox = QtWidgets.QCheckBox(description)
        checkbox.setStyleSheet("font-size: 25pt;")
        self.checkboxes[i] = checkbox
        h_layout.addWidget(checkbox)
        if self.status_list[i][1]:
            self.values[i] = QtWidgets.QLabel("N/A")
            h_layout.addWidget(self.values[i])
        layout.addLayout(h_layout)

    def _initStatusWidgets(self):
        for i in range(len(self.status_list)):
            if (i <= 5):
                self._addStatus(i, self.layout_left)
            elif (i <= 10):
                self._addStatus(i, self.layout_mid)
            else:
                self._addStatus(i, self.layout_right)

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
                    self.values[i].setStyleSheet("font-weight: bold; color: '#17a2b8'; font-size: 25pt;")
                elif (v < self.status_list[i][3]):
                    self.values[i].setStyleSheet("font-weight: bold; color: '#ffc107'; font-size: 25pt;")
                else: 
                    self.values[i].setStyleSheet("font-weight: bold; color: '#dc3545'; font-size: 25pt;") 
        

    def update_sensors_status(self, response):
        if (response != None):
            self._update_bool(0, "Sens HeartBeat", True)
            for i in [2, 4, 7, 9, 10, 11, 12, 14, 15]:
                self.checkboxes[i].setChecked(False)
            
            self._update_value(2, response.cpu_temperature_degC,
                                 "%0.1f [degC]", "Sens CPU T", True)

            
            rtt_time = response.timestamp - response.request_timestamp
            self._update_value(4, response.server_version, 
                "%s", "Sens Ser Ver", False)
            
            self._update_value(7, rtt_time, "%04.0f [ms]", "Sensors RTT", True)
            self._update_bool(9, "Drill On", response.drill_on)
            self._update_bool(10, "Heater On", response.heater_on)
            
            self._update_value(11, response.triac_level, "%0.2f", 
                "Triac Level", True)
            self._update_value(12, response.weight_on_bit_drill_N,
                 "%04.0f [N]", "WOB Drill", True)
            self._update_value(14, response.total_current_mA,
                 "%05.0f [mA]", "Current", True)

            accel = numpy.sqrt(
                response.imu_ax_g*response.imu_ax_g + \
                response.imu_ay_g*response.imu_ay_g + \
                response.imu_az_g*response.imu_az_g )

            self._update_value(15, accel,
                 "%03.2f [g]", "Accel", True)
            
        else:
            for c in self.checkboxes:
                c.setChecked(False)


    def update_motor_status(self, response):
        if (response != None):
            self._update_bool(1, "Motor HeartBeat", True)
            
            for i in [3, 5, 8, 13]:
                self.checkboxes[i].setChecked(False)
            
            self._update_value(3, response.cpu_temperature_degC,
                                 "%0.1f [degC]", "Motor CPU T", True)
            
            rtt_time = response.timestamp - response.request_timestamp
            self._update_value(5, response.server_version, 
                "%s", "Motor Ser Ver", False)
            
            self._update_value(8, rtt_time, "%04.0f [ms]", "Motor RTT", True)
            self._update_value(13, response.weight_on_bit_heater_N,
                  "%04.0f [N]", "WOB Heater", True)
            
        else:
            for c in self.checkboxes:
                c.setChecked(False)

