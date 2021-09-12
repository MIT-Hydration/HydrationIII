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
from . import client_common

class RelayTriacControl:

    def __init__(self, groupbox):
        self.threads = []
        self.groupbox = groupbox
        self.layout = QtWidgets.QVBoxLayout()
        self.groupbox.setLayout(self.layout)
        self.layout.addWidget(QtWidgets.QLabel("Drill"))
        self.drill_on_button = QtWidgets.QPushButton("Drill On")
        self.drill_off_button = QtWidgets.QPushButton("Drill Off")
        self.layout.addWidget(self.drill_on_button)
        self.layout.addWidget(self.drill_off_button)
        self.layout.addWidget(QtWidgets.QLabel("Heater"))
        self.heater_on_button = QtWidgets.QPushButton("Heater On")
        self.heater_off_button = QtWidgets.QPushButton("Heater Off")
        self.layout.addWidget(self.heater_on_button)
        self.layout.addWidget(self.heater_off_button)
        self.layout.addWidget(QtWidgets.QLabel("Triac [0 to 1]"))
        
        self.triac_level_textbox = QtWidgets.QLineEdit("0.0")
        self.set_triac_button = QtWidgets.QPushButton("Set Triac")
        self.layout.addWidget(self.triac_level_textbox)
        self.layout.addWidget(self.set_triac_button)

        self.drill_on_button.clicked.connect(self._drill_on)
        self.drill_off_button.clicked.connect(self._drill_off)
        self.heater_on_button.clicked.connect(self._heater_on)
        self.heater_off_button.clicked.connect(self._heater_off)
        self.set_triac_button.clicked.connect(self._set_triac)
        
        
    def _drill_on(self):
        client_thread = client_common.RelayThread("Drill", True)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def _drill_off(self):
        client_thread = client_common.RelayThread("Drill", False)
        self.threads.append(client_thread)
        client_thread.start() 

    def _heater_on(self):
        client_thread = client_common.RelayThread("Heater", True)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def _heater_off(self):
        client_thread = client_common.RelayThread("Heater", False)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def _set_triac(self):
        client_thread = client_common.TriacThread(float(self.triac_level_textbox.text()))
        self.threads.append(client_thread)
        client_thread.start() 

    
        

    

