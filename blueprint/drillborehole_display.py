"""
drillborehole_display.py
Settings and state for drilling borehole
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
from PySide6.QtCore import QTimer, Signal

from datetime import datetime, timedelta
import time
import configparser

from functools import partial

import grpc
from .generated import mission_control_pb2_grpc
from .generated import mission_control_pb2 as mcpb

config = configparser.ConfigParser()
config.read('config.ini')

MC_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class DrillBoreholeDisplay(QtWidgets.QWidget):
    def __init__(self, main_window, group_box):
        # Tuple (buttons display text, pointer to functions)  
        self.threads = []
        self.group_box = group_box
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout()
        self.group_box.setLayout(self.layout)
        self._initWidgets()

    def _initWidgets(self):
        self.hole_label = QtWidgets.QLabel("Next Hole: ")
        self.layout.addWidget(self.hole_label)

    def update_status(self, response):
        if (response != None):
            holes = response.holes
            self.hole_label.setText(f"Next Hole: {len(holes) + 1}")