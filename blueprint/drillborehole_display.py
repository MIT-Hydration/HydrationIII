"""
drillborehole_display.py
Settings and state for drilling borehole
"""

__author__      = "Prakash Manandhar and Eric Bui"
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
            [mcpb.DRILLING_HOLE_HOMING_Z1, QtWidgets.QLabel("6. Homing Z1")],
            [mcpb.HEATER_HOLE_MOVING_TO_Z2, QtWidgets.QLabel("7. Aligning Hole to Z2")],
            [mcpb.HEATER_IDLE, QtWidgets.QLabel("8. Ready to Heat / Lower Heater")],
            [mcpb.HEATER_LOWERING_DOWN, QtWidgets.QLabel("9. Lowering/Withdrawing Heater")],
            [mcpb.HEATER_MELTING, QtWidgets.QLabel("10. Melting")],
            [mcpb.HEATER_HOMING_Z2, QtWidgets.QLabel("11. Homing Z2 (Heater)")],
        ]

        self.layout = QtWidgets.QVBoxLayout()
        self.group_box.setLayout(self.layout)
        self._initWidgets()

    def _initWidgets(self):
        
        for i in range(len(self.state_labels)):
            if i%4 == 0:
                line = QtWidgets.QHBoxLayout()
                self.layout.addLayout(line)
            line.addWidget (self.state_labels[i][1])
        
        line = QtWidgets.QHBoxLayout()
        self.layout.addLayout(line)

        self.hole_label = QtWidgets.QLabel("Next Hole: ")
        self.new_hole_button = QtWidgets.QPushButton("New Hole")
        self.new_hole_button.clicked.connect(self._on_new_hole)
        self.move_y_label = QtWidgets.QLabel("Relative Move [m]: ")
        self.target_y = QtWidgets.QLineEdit("0.0")
        #self.target_y.setValidator(QtGui.QDoubleValidator())
        
        line = QtWidgets.QHBoxLayout()
        self.layout.addLayout(line)

        line.addWidget (self.move_y_label)
        line.addWidget (self.target_y)
        self.move_y_button = QtWidgets.QPushButton("Move Y")
        line.addWidget (self.move_y_button)
        self.move_y_button.clicked.connect(self._on_move_y)

        line.addWidget (self.hole_label)
        line.addWidget (self.new_hole_button)
        
        line = QtWidgets.QHBoxLayout()
        self.layout.addLayout(line)

        self.target_z1_label = QtWidgets.QLabel("Relative Target Drill Depth (-ve: down, +ve up) [m]: ")
        self.target_z1 = QtWidgets.QLineEdit("0.0")
        #self.target_z1.setValidator(QtGui.QDoubleValidator())
        line.addWidget (self.target_z1_label)
        line.addWidget (self.target_z1)
        
        line = QtWidgets.QHBoxLayout()
        self.layout.addLayout(line)

        self.velocity_label = QtWidgets.QLabel("Velocity in For (Both Y and Z) [RPM]")
        self.velocitys = QtWidgets.QLineEdit("90")
        line.addWidget (self.velocity_label)
        line.addWidget (self.velocitys )

        line = QtWidgets.QHBoxLayout()
        self.layout.addLayout(line)
        
        self.move_z1_button = QtWidgets.QPushButton("Drill Down/Ream Up")
        self.move_z1_button.clicked.connect(self._on_move_z1)
        line.addWidget (self.move_z1_button)
        
        self.finish_hole_button = QtWidgets.QPushButton("Home Z1, Goto Heating")
        line.addWidget (self.finish_hole_button)
        self.finish_hole_button.clicked.connect(self._on_finish_hole)

        self.align_button = QtWidgets.QPushButton("Align Heater")
        line.addWidget (self.align_button)
        self.align_button.clicked.connect(self._on_align)

        self.move_z2_button = QtWidgets.QPushButton("Move Z2 (Heater)")
        self.move_z2_button.clicked.connect(self._on_move_z2)
        line.addWidget (self.move_z2_button)

        line = QtWidgets.QHBoxLayout()
        self.layout.addLayout(line)
    
        self.melt_button = QtWidgets.QPushButton("Start Melting and Pumping")
        self.melt_button.clicked.connect(self._on_melt)
        line.addWidget (self.melt_button)
    
        self.end_melt_button = QtWidgets.QPushButton("End Melt, Home Z2, Finish Hole")
        self.end_melt_button.clicked.connect(self._on_end_melt)
        line.addWidget (self.end_melt_button)
    

    @QtCore.Slot(object)
    def _on_move_z1(self):
        timestamp = datetime.now()
        target_z1 = float(self.target_z1.text())
        target_vel = float(self.velocitys.text())
        self.main_window.log(
            f"[{timestamp}] Attempting to move Z1 by relative"\
            f" {target_z1:0.4f} [m]"\
            f" {target_vel:0.4f} [RPM]"
            )
        client_thread = client_common.GotoZ1Thread(target_z1, target_vel )
        client_thread.log.connect(self.main_window.on_log)
        self.threads.append(client_thread)
        client_thread.start()

    @QtCore.Slot(object)
    def _on_move_z2(self):
        timestamp = datetime.now()
        target_z = float(self.target_z1.text())
        target_vel = float(self.velocitys.text())
        self.main_window.log(
            f"[{timestamp}] Attempting to move Z2 by relative"\
            f" {target_z:0.4f} [m]"\
            f" {target_vel:0.4f} [RPM]"
            )
        client_thread = client_common.GotoZ2Thread(target_z, target_vel )
        client_thread.log.connect(self.main_window.on_log)
        self.threads.append(client_thread)
        client_thread.start()

    @QtCore.Slot(object)
    def _on_align(self):
        timestamp = datetime.now()
        self.main_window.log(
            f"[{timestamp}] Attempting to Align Heater"
            )
        client_thread = client_common.AlignHeaterThread()
        client_thread.log.connect(self.main_window.on_log)
        self.threads.append(client_thread)
        client_thread.start()
    
    @QtCore.Slot(object)
    def _on_move_y(self):
        try:
            timestamp = datetime.now() 
            target_y = float(self.target_y.text())
            target_vel = float(self.velocitys.text())

            self.main_window.log(
                f"[{timestamp}] Attempting to move Y by relative"\
                f" {target_y:0.4f} [m]"\
                f" {target_vel:0.4f} [RPM]")
            client_thread = client_common.GotoYThread(target_y, target_vel)
            client_thread.log.connect(self.main_window.on_log)
            self.threads.append(client_thread)
            client_thread.start()
        except Exception as e:
            print(e)

    @QtCore.Slot(object)
    def _on_hole_done(self, response):
        if (response != None):
            timestamp = datetime.now()
            self.main_window.log(f"[{timestamp}] Hole Start/Finish result {response}")

    @QtCore.Slot(object)
    def _on_new_hole(self):
        timestamp = datetime.now() 
        self.main_window.log(f"[{timestamp}] New Hole Command")
        client_thread = client_common.NewHoleThread()
        client_thread.log.connect(self.main_window.on_log)
        client_thread.done.connect(self._on_hole_done)
        self.threads.append(client_thread)
        client_thread.start()

    @QtCore.Slot(object)
    def _on_finish_hole(self):
        timestamp = datetime.now() 
        self.main_window.log(f"[{timestamp}] End Hole Command")
        client_thread = client_common.EndHoleThread()
        client_thread.log.connect(self.main_window.on_log)
        client_thread.done.connect(self._on_hole_done)
        self.threads.append(client_thread)
        client_thread.start()

    @QtCore.Slot(object)
    def _on_melt(self):
        timestamp = datetime.now() 
        self.main_window.log(f"[{timestamp}] Start Melt")
        client_thread = client_common.StartMeltThread()
        client_thread.log.connect(self.main_window.on_log)
        #client_thread.done.connect(self._on_hole_done)
        self.threads.append(client_thread)
        client_thread.start()

    @QtCore.Slot(object)
    def _on_end_melt(self):
        timestamp = datetime.now() 
        self.main_window.log(f"[{timestamp}] End Melt")
        client_thread = client_common.EndMeltThread()
        client_thread.log.connect(self.main_window.on_log)
        #client_thread.done.connect(self._on_hole_done)
        self.threads.append(client_thread)
        client_thread.start()
    
    def update_status(self, response):
        if (response != None):
            holes = response.holes
            if (response.state == mcpb.DRILL_IDLE):
                self.hole_label.setText(f"Next Hole: {len(holes) + 1}")
                self.move_y_button.setEnabled(True)
                self.new_hole_button.setEnabled(True)
                self.target_y.setEnabled(True)
                self.align_button.setEnabled(True)
            else:
                self.hole_label.setText(f"Current Hole: {len(holes)}")
                self.move_y_button.setEnabled(False)
                self.new_hole_button.setEnabled(False)
                self.target_y.setEnabled(False)
                self.align_button.setEnabled(False)

            if (response.state == mcpb.DRILLING_HOLE_IDLE):
                self.move_z1_button.setEnabled(True)
                self.finish_hole_button.setEnabled(True)
            else:
                self.move_z1_button.setEnabled(False)
                self.finish_hole_button.setEnabled(False)

            if (response.state == mcpb.HEATER_IDLE) \
                    or (response.state == mcpb.DRILLING_HOLE_IDLE):
                self.target_z1.setEnabled(True)
            else:
                self.target_z1.setEnabled(False)

            if (response.state == mcpb.HEATER_IDLE):
                self.move_z2_button.setEnabled(True)
                self.melt_button.setEnabled(True)
            else:
                self.move_z2_button.setEnabled(False)
                self.melt_button.setEnabled(False)

            if (response.state == mcpb.HEATER_MELTING):
                self.end_melt_button.setEnabled(True)
            else:
                self.end_melt_button.setEnabled(False)
            
            for l in self.state_labels:
                if l[0] == response.state:
                    l[1].setStyleSheet("font-style: italic; color: '#ffc107'")
                else:
                    l[1].setStyleSheet("font-style: normal; color: '#ffffff'")