"""
hole_pos_display.py
Displays the positions of the holes, and displays X Y positions and controls
to set the X, Y positions
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
import pyqtgraph as pg
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
X_LENGTH = config.getfloat('Rig', 'XLength')
Y_LENGTH = config.getfloat('Rig', 'YLength')
RIG_UNITS = config.get('Rig', 'Units')

class HolePositionDisplay(QtWidgets.QWidget):
    def __init__(self, layout):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.layout = layout
        self.HOLE_DISPLAY_WIDTH = 4
        self.TARGET_DISPLAY_WIDTH = 4
        self.Z_DISPLAY_WIDTH = 1
        self.DISPLAY_HEIGHT = 10
        self._init_hole_display()
        self._init_target()
        self._init_z1_display()
        self._init_z2_display()

    def _init_hole_display(self):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.plot = pg.PlotWidget()
        self.plot.showGrid(x = True, y = True, alpha = 1.0)
        self.plot.setXRange(-0.05, X_LENGTH + 0.05, padding=0)
        self.plot.setYRange(-0.05, Y_LENGTH + 0.05, padding=0)
        self.plot.getAxis('bottom').setLabel(f'X {RIG_UNITS}')
        self.plot.getAxis('left').setLabel(f'Y {RIG_UNITS}')
        self.scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=7, color='r'), symbol='o', size=10)
        self.plot.addItem(self.scatter)
        self.layout.addWidget(self.plot, 0, 0, 
            self.DISPLAY_HEIGHT, self.HOLE_DISPLAY_WIDTH)

    def _init_target(self):
        start_h = self.HOLE_DISPLAY_WIDTH + 1
        self.layout.addWidget(QtWidgets.QLabel("Target [m]"), 0, start_h, 1, 2)
        self.layout.addWidget(QtWidgets.QLabel("X: "), 1, start_h, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel("Y: "), 1, start_h + 2, 1, 1)
        self.layout.addWidget(QtWidgets.QLineEdit(""), 1, start_h + 1, 1, 1)
        self.layout.addWidget(QtWidgets.QLineEdit(""), 1, start_h + 3, 1, 1)
        self.layout.addWidget(QtWidgets.QPushButton("GoTo Target (X, Y)"), 0, start_h + 2, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel("Z1: "), 2, start_h, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel("Z2: "), 2, start_h + 2, 1, 1)
        self.layout.addWidget(QtWidgets.QLineEdit(""), 2, start_h + 1, 1, 1)
        self.layout.addWidget(QtWidgets.QLineEdit(""), 2, start_h + 3, 1, 1)

        self.layout.addWidget(QtWidgets.QPushButton("GoTo Target (Z1)"), 3, start_h, 1, 2)
        self.layout.addWidget(QtWidgets.QPushButton("GoTo Target (Z2)"), 3, start_h + 2, 1, 2)
        
        self.layout.addWidget(QtWidgets.QLabel("Current Position (X, Y, Z1, Z2) [m]"), 
            5, start_h, 1, 2)

        self.layout.addWidget(QtWidgets.QPushButton("Set Current as Origin (X, Y, Z1, Z2)"), 
            6, start_h, 1, 4)
        
    def _init_z_display(self, zplot, zscatter, start_h, label):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        zplot.showGrid(x = False, y = True, alpha = 1.0)
        zplot.setXRange(-0.0, 0.0, padding=0)
        zplot.setYRange(-0.05, Y_LENGTH + 0.05, padding=0)
        zplot.getAxis('left').setLabel(f'{label} {RIG_UNITS}')
        zplot.addItem(zscatter)
        zplot.setMaximumWidth(120)
        self.layout.addWidget(zplot, 0, start_h, 
            self.DISPLAY_HEIGHT, self.Z_DISPLAY_WIDTH)

    def _init_z1_display(self):
        self.z1plot = pg.PlotWidget()
        self.z1scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=7, color='r'), symbol='o', size=10)
        self._init_z_display(self.z1plot, self.z1scatter, 
            self.HOLE_DISPLAY_WIDTH + self.TARGET_DISPLAY_WIDTH + 1,
            'Z1 (Drill)')

    def _init_z2_display(self):
        self.z2plot = pg.PlotWidget()
        self.z2scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=7, color='r'), symbol='o', size=10)
        self._init_z_display(self.z2plot, self.z2scatter, 
            self.HOLE_DISPLAY_WIDTH + self.TARGET_DISPLAY_WIDTH + self.Z_DISPLAY_WIDTH + 1,
            'Z2 (Heater)')

    def update_display(self, response):
        if (response != None):    
            print(response.rig_x)
            print(response.rig_y)  
            self.scatter.setData([response.rig_x], [response.rig_y])
