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
        self.plot = pg.plot()
        self.plot.showGrid(x = True, y = True, alpha = 1.0)
        
        self._initAxis(
            self.plot.getAxis('bottom'),
            f'X {RIG_UNITS}', X_LENGTH + 5
            )
        
        self._initAxis(
            self.plot.getAxis('left'),
            f'Y {RIG_UNITS}', Y_LENGTH + 5
            )
        
        layout.addWidget(self.plot, 1, 0, 10, 1)

    def _initAxis(self, ax, label, length):
        ax.unlinkFromView()
        ax.setLabel(label)
        ax.setRange(0, length)