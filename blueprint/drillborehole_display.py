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
from . import client_common
from .generated import mission_control_pb2 as mcpb
from datetime import datetime

class DrillBoreholeDisplay(QtWidgets.QWidget):
    def __init__(self, main_window, group_box):
        # Tuple (buttons display text, pointer to functions)  
        self.threads = []
        self.group_box = group_box
        self.main_window = main_window
        self.state_labels = [
            [mcpb.DRILL_IDLE, QtWidgets.QLabel("1. Idle")],
            [mcpb.DRILL_MOVING_Y, QtWidgets.QLabel("2. Moving Y")],
            [mcpb.DRILLING_HOLE_IDLE, QtWidgets.QLabel("3. Waiting to Start Drill")],
            [mcpb.DRILLING_HOLE_DRILLING_DOWN, QtWidgets.QLabel("4. Drilling Down")],
            [mcpb.DRILLING_HOLE_REAMING_UP, QtWidgets.QLabel("5. Reaming Up")],
            [mcpb.DRILLING_HOLE_HOMING_Y, QtWidgets.QLabel("6. Homing Z1")]
        ]

        self.layout = QtWidgets.QVBoxLayout()
        self.group_box.setLayout(self.layout)
        self._initWidgets()

    def _initWidgets(self):
        line = QtWidgets.QHBoxLayout()
        self.hole_label = QtWidgets.QLabel("Next Hole: ")
        line.addWidget (self.hole_label)
        self.layout.addLayout(line)
        for i in range(len(self.state_labels)):
            if (i + 1)%4 == 0:
                line = QtWidgets.QHBoxLayout()
                self.layout.addLayout(line)
            line.addWidget (self.state_labels[i][1])
        self.move_y_label = QtWidgets.QLabel("Relative Move [m]: ")
        self.target_y = QtWidgets.QLineEdit("")
        self.target_y.setValidator(QtGui.QDoubleValidator())
        line = QtWidgets.QHBoxLayout()
        line.addWidget (self.move_y_label)
        line.addWidget (self.target_y)
        self.move_y_button = QtWidgets.QPushButton("Move Y")
        line.addWidget (self.move_y_button)
        self.move_y_button.clicked.connect(self.on_move_y)
        self.layout.addLayout(line)

    @QtCore.Slot(object)
    def on_move_y(self):
        timestamp = datetime.now() 
        self.main_window.log(
            f"[{timestamp}] Attempting to move Y by relative"\
            f" {float(self.target_y.text()):0.4f} [m]")
        client_thread = client_common.GotoYThread(float(self.target_y.text()))
        self.threads.append(client_thread)
        client_thread.start()
    
    def update_status(self, response):
        if (response != None):
            holes = response.holes
            if (response.state == mcpb.DRILL_IDLE):
                self.hole_label.setText(f"Next Hole: {len(holes) + 1}")
            else:
                self.hole_label.setText(f"Current Hole: {len(holes)}")
            
            for l in self.state_labels:
                if l[0] == response.state:
                    l[1].setStyleSheet("font-style: italic; color: '#ffc107'")
                else:
                    l[1].setStyleSheet("font-style: normal; color: '#ffffff'")