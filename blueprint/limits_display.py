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

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

class LimitsDisplay:

    def __init__(self, layout):
        self.threads = []
        self.layout = layout
        self._initWidgets()

    def _initWidgets(self):
        self.air_gap_edit = QtWidgets.QLineEdit()
        self.max_z1_edit = QtWidgets.QLineEdit()
        self.ice_start_edit = QtWidgets.QLineEdit()
        self.save_button = QtWidgets.QPushButton("Set Limits")
        
        self.layout.addRow(QtWidgets.QLabel("Air Gap to Regolith [m]: "), self.air_gap_edit)
        self.layout.addRow(QtWidgets.QLabel("Max Z1 (Drill Travel) [m]: "), self.max_z1_edit)
        self.layout.addRow(QtWidgets.QLabel("Ice Start Depth [m]: "), self.ice_start_edit)
        self.layout.addRow(self.save_button)

    def _updateDisplay(self, stub, timestamp, timeout):
        print("Updating limits display")
        response = stub.GetLimits (
                    mission_control_pb2.GetLimitRequest(request_timestamp = timestamp),
                    timeout = timeout )
        self.air_gap_edit.setText(f'{response.air_gap:.4f}')
        
        