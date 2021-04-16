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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QDateTime

from QLed import QLed
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
        self.leds = [None] * len(self.status_list)
        self.values = [None] * len(self.status_list)
        self.layout = layout
        self._initStatusWidgets()
        
    def _addStatus(self, i):
        h_layout = QtWidgets.QHBoxLayout()
        led = QLed(onColour=QLed.Green, shape=QLed.Circle)
        self.leds[i] = led
        led.setMaximumHeight(20)
        led.setMaximumWidth(20)
        h_layout.addWidget(led)
        description = self.status_list[i][0]
        if self.status_list[i][1]:
            description += ":"
        h_layout.addWidget(QtWidgets.QLabel(description))
        if self.status_list[i][1]:
            self.values[i] = QtWidgets.QLabel("N/A")
            h_layout.addWidget(self.values[i])
        
        h_layout.addStretch(5)
        self.layout.addLayout(h_layout)

    def _initStatusWidgets(self):
        for i in range(len(self.status_list)):
            self._addStatus(i)
        self.layout.addStretch(5)


    def _update_value(self, i, v, fstr, name, check_value):
        if (self.status_list[i][0] != name):
            raise IndexError(f"{name} not at right index")
        self.leds[i].value = True
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
            self._update_value(0, True, "", "System HeartBeat", False)
            self._update_value(12, response.cpu_temperature_degC,
                                 "%0.2f [degC]", "CPU Temp (degC)", True)
            mission_time = timedelta(milliseconds=int(response.mission_time_ms / 1000)*1000)
            self._update_value(13, str(mission_time), "%s", "Mission Time (H:M:S)", False)
            rtt_time = response.timestamp - response.request_timestamp
            self._update_value(14, rtt_time, "%0.2f [ms]", "Round Trip Time (ms)", True)
            

        else:
            for l in self.leds:
                l.value = False

