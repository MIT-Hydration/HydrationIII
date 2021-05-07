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
        self.plot = pg.PlotWidget()
        self.plot.showGrid(x = True, y = True, alpha = 1.0)
        self.plot.setXRange(-5, X_LENGTH + 5, padding=0)
        self.plot.setYRange(-5, Y_LENGTH + 5, padding=0)
        self.plot.getAxis('bottom').setLabel(f'X {RIG_UNITS}')
        self.plot.getAxis('left').setLabel(f'Y {RIG_UNITS}')
        self.scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=7, color='r'), symbol='o', size=10)
        self.plot.addItem(self.scatter)
        layout.addWidget(self.plot, 1, 0, 10, 1)

    def update_display(self, response):
        if (response != None):    
            print(response.rig_x)
            print(response.rig_y)  
            self.scatter.setData([response.rig_x], [response.rig_y])
