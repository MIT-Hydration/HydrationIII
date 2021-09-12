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
        self.threads = []
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
        client_thread = client_common.TriacThread(float(self.triac_level_textbox.text()))
        self.threads.append(client_thread)
        client_thread.start() 

    
        

    

