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
        self.max_z1_edit = QtWidgets.QLineEdit()
        self.ice_depth_edit = QtWidgets.QLineEdit()
        self.save_button = QtWidgets.QPushButton("Set Limits")
        
        self.layout.addRow(self.air_gap_label, self.air_gap_edit)
        self.layout.addRow(self.max_z1_label, self.max_z1_edit)
        self.layout.addRow(self.ice_depth_label, self.ice_depth_edit)
        self.layout.addRow(self.save_button)

    def _setDisplayLine(self, label, edit, label_text, value):
        if value != str(edit.text()):
            new_text = label_text + "(changed) "
            if(label.text() != new_text):
                label.setText(label_text + "(changed) ")
                label.setStyleSheet("color: '#dc3545'")
        else:
            if(label.text() != label_text):
                label.setText(label_text)
                label.setStyleSheet("color: '#ffffff'")


    def _updateLimitDisplay(self, response):
       
        air_gap = f'{response.air_gap:.4f}'
        max_z1 = f'{response.max_z1:.4f}'
        ice_depth = f'{response.ice_depth:.4f}'
        if self.first_widget_fill:
            self.air_gap_edit.setText(air_gap)
            self.max_z1_edit.setText(max_z1)
            self.ice_depth_edit.setText(ice_depth)
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
            