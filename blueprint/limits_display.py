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

from .generated import mission_control_pb2, mission_control_pb2_grpc

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer, Signal

import configparser
import threading, time, grpc, numpy

config = configparser.ConfigParser()
config.read('config.ini')

RPI_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')


class LimitsDisplay:

    def __init__(self, layout):
        self.threads = []
        self.layout = layout
        self._initWidgets()

    def _initWidgets(self):
        self.first_widget_fill = True
        self.air_gap_label = QtWidgets.QLabel("Air Gap to Regolith [m]: ")
        self.max_z1_label = QtWidgets.QLabel("Max Z1 (Drill Travel) [m]: ")
        self.ice_depth_label = QtWidgets.QLabel("Ice Start Depth [m]: ")
        
        self.air_gap_edit = QtWidgets.QLineEdit()
        self.air_gap_edit.setValidator(QtGui.QDoubleValidator())
        self.max_z1_edit = QtWidgets.QLineEdit()
        self.max_z1_edit.setValidator(QtGui.QDoubleValidator())
        self.ice_depth_edit = QtWidgets.QLineEdit()
        self.ice_depth_edit.setValidator(QtGui.QDoubleValidator())
        self.save_button = QtWidgets.QPushButton("Set Limits")
        self.save_button.clicked.connect(self._on_save)
        
        self.layout.addRow(self.air_gap_label, self.air_gap_edit)
        self.layout.addRow(self.max_z1_label, self.max_z1_edit)
        self.layout.addRow(self.ice_depth_label, self.ice_depth_edit)
        self.layout.addRow(self.save_button)

    @QtCore.Slot(object)
    def _on_save(self):
        th = threading.Thread(target=self._save)
        th.start()
        self.threads.append(th)

    def _save(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.SetLimits (
                    mission_control_pb2.Limits(
                        request_timestamp = timestamp,
                        air_gap = float(self.air_gap_edit.text()),
                        max_z1 = float(self.max_z1_edit.text()),
                        ice_depth = float(self.ice_depth_edit.text()),
                        ),
                    timeout = GRPC_CALL_TIMEOUT )
                
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

    def _setDisplayLine(self, label, edit, label_text, value):
        new_value = float(edit.text())
        if numpy.abs(value - new_value) > 0.0005:
            new_text = label_text + f"(changed to {value:0.3f}) "
            if(label.text() != new_text):
                label.setText(new_text)
                label.setStyleSheet("font-style: italic; color: '#ffc107'")
        else:
            if(label.text() != label_text):
                label.setText(label_text)
                label.setStyleSheet("color: '#ffffff'")

    def update_limits(self, response):
        if response != None:
            air_gap = response.air_gap
            max_z1 = response.max_z1
            ice_depth = response.ice_depth
            if self.first_widget_fill:
                self.air_gap_edit.setText(f'{response.air_gap:.3f}')
                self.max_z1_edit.setText(f'{response.max_z1:.3f}')
                self.ice_depth_edit.setText(f'{response.ice_depth:.3f}')
                self.first_widget_fill = False
            else:
                self._setDisplayLine(
                    self.air_gap_label, self.air_gap_edit, 
                    "Air Gap to Regolith [m]: ", air_gap)
                self._setDisplayLine(
                    self.max_z1_label, self.max_z1_edit, 
                    "Max Z1 (Drill Travel) [m]: ", max_z1)
                self._setDisplayLine(
                    self.ice_depth_label, self.ice_depth_edit, 
                    "Ice Start Depth [m]: ", ice_depth)
            