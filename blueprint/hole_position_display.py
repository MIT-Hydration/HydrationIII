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
from . import client_common
from .generated import mission_control_pb2
from datetime import datetime

config = configparser.ConfigParser(
    converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config.read('config.ini')
X_LENGTH = 0.1 #config.getfloat('Rig', 'XLength')
Y_LENGTH = config.getfloat('Rig', 'YLength')
Z_LENGTH = config.getfloat('Rig', 'ZLength')
RIG_UNITS = config.get('Rig', 'Units')
HeaterDeltaXY = config.getlist("Rig", "HeaterDeltaXY")
HeaterDeltaXY = [float(HeaterDeltaXY[0]), float(HeaterDeltaXY[1])]

Z1Cal = config.getfloat('Rig', 'Z1Cal')
Z2Cal = config.getfloat('Rig', 'Z2Cal')
YCal = config.getfloat('Rig', 'YCal')

class HolePositionDisplay(QtWidgets.QWidget):
    def __init__(self, main_window, layout):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.main_window = main_window
        self.threads = []
        self.layout = layout
        self.HOLE_DISPLAY_WIDTH = 1
        self.TARGET_DISPLAY_WIDTH = 10
        self.Z_DISPLAY_WIDTH = 1
        self.DISPLAY_HEIGHT = 10
        self._init_hole_display()
        self._init_target()
        self._init_z1_display()
        self._on_speed_change()
        
    def _init_hole_display(self):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.plot = pg.PlotWidget()
        self.plot.showGrid(x = True, y = True, alpha = 1.0)
        self.plot.setXRange(-X_LENGTH/2, X_LENGTH/2, padding=0)
        self.plot.setYRange(-0.05, Y_LENGTH + 0.05, padding=0)
        self.plot.getAxis('bottom').setLabel(f'X {RIG_UNITS}')
        self.plot.getAxis('left').setLabel(f'Y {RIG_UNITS}')
        self.holes_scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=3, color='#ffc107'), symbol='o', size=20)
        self.heater_scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=3, color='#dc3545'), symbol='x', size=10)
        self.scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=3, color='#cfebfd'), symbol='+', size=10)
        
        self.plot.addItem(self.holes_scatter)
        self.plot.addItem(self.scatter)
        self.plot.addItem(self.heater_scatter)
        self.plot.setMaximumWidth(120)
        
        self.layout.addWidget(self.plot, 0, 0, 
            self.DISPLAY_HEIGHT, self.HOLE_DISPLAY_WIDTH)

    def _init_target(self):
        start_h = self.HOLE_DISPLAY_WIDTH + 1
        self.layout.addWidget(QtWidgets.QLabel("Relative Motion (During Startup Idle)"), 0, start_h, 1, 2)
        
        self.layout.addWidget(QtWidgets.QLabel("Speed (RPM)"), 0, start_h + 2, 1, 1)
        self.target_speed = QtWidgets.QLineEdit("30")
        self.target_speed.setValidator(QtGui.QDoubleValidator())
        self.layout.addWidget(self.target_speed, 0, start_h + 3, 1, 1)
        
        self.speed_units = QtWidgets.QLabel("Speed Conversions:\nZ1 = \nZ2 = \nY = ")
        self.layout.addWidget(self.speed_units, 0, start_h + 4, 1, 1)
        self.target_speed.textChanged.connect(self._on_speed_change)

        self.layout.addWidget(QtWidgets.QLabel("Y [m]: "), 3, start_h, 1, 1)

        self.target_y = QtWidgets.QLineEdit("0.0")
        self.target_y.setValidator(QtGui.QDoubleValidator())
        
        self.layout.addWidget(self.target_y, 3, start_h + 1, 1, 1)

        self.goto_target_y = QtWidgets.QPushButton("Move Y")
        self.goto_target_y.clicked.connect(self._goto_y)
        self.layout.addWidget(self.goto_target_y, 3, start_h + 2, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel("Z1 [m]: "), 1, start_h, 1, 1)
        
        self.target_z1 = QtWidgets.QLineEdit("0.0")
        self.target_z1.setValidator(QtGui.QDoubleValidator())
        self.layout.addWidget(self.target_z1, 1, start_h + 1, 1, 1)
        
        
        self.layout.addWidget(QtWidgets.QLabel("Z2 [m]: "), 1, start_h + 2, 1, 1)
        
        self.target_z2 = QtWidgets.QLineEdit("0.0")
        self.target_z1.setValidator(QtGui.QDoubleValidator())
        self.layout.addWidget(self.target_z2, 1, start_h + 3, 1, 1)

        self.goto_z1 = QtWidgets.QPushButton("Move Z1")
        self.goto_z1.clicked.connect(self._goto_z1)

        self.layout.addWidget(self.goto_z1, 2, start_h, 1, 2)
        
        self.goto_z2 = QtWidgets.QPushButton("Move Z2")
        self.goto_z2.clicked.connect(self._goto_z2)

        self.layout.addWidget(self.goto_z2, 2, start_h+2, 1, 2)

        self.cur_pos_label = QtWidgets.QLabel("Current Position (Z1, Z2, Y) = (00.000 00.000 00.000) [m]")
        self.cur_pos_label.setStyleSheet("font-weight: bold; color: '#ffc107'; font-size: 25pt;")
        self.layout.addWidget(self.cur_pos_label, 5, start_h, 1, 5)

        self.set_home = QtWidgets.QPushButton("Set Current as Origin (Z1, Z2, Y)")
        self.set_home.clicked.connect(self._set_home)
        self.layout.addWidget(self.set_home, 6, start_h, 1, 4)

        self.align_button = QtWidgets.QPushButton(
            f"Align Heater (Preset Speed 300 RPM, Preset Y = {HeaterDeltaXY[1]} meters)")
        self.layout.addWidget(self.align_button, 7, start_h, 1, 4)
        self.align_button.clicked.connect(self._on_align)

    def _goto_y(self):
        target_vel = float(self.target_speed.text())
        client_thread = client_common.GotoYThread(float(self.target_y.text()), target_vel)
        self.threads.append(client_thread)
        client_thread.start()
        
    def _goto_z1(self):
        target_vel = float(self.target_speed.text())
        client_thread = client_common.GotoZ1Thread(
            float(self.target_z1.text()), target_vel)
        self.threads.append(client_thread)
        client_thread.start() 
    
    def _goto_z2(self):
        target_vel = float(self.target_speed.text())
        client_thread = client_common.GotoZ2Thread(
            float(self.target_z2.text()), target_vel)
        self.threads.append(client_thread)
        client_thread.start() 

    def _set_home(self):
        self.main_window.log("Setting Home...")
        client_thread = client_common.SetHomeThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def _init_z_display(self, zplot, start_h, label):
        global X_LENGTH, Z_LENGTH, RIG_UNITS
        zplot.showGrid(x = False, y = True, alpha = 1.0)
        zplot.setXRange(-0.0, 0.0, padding=0)
        zplot.setYRange(-Z_LENGTH - 0.05, 0.15, padding=0)
        zplot.getAxis('left').setLabel(f'{label} {RIG_UNITS}')
        zplot.setMaximumWidth(120)
        self.layout.addWidget(zplot, 0, start_h, 
            self.DISPLAY_HEIGHT, self.Z_DISPLAY_WIDTH)

    def _init_z1_display(self):
        global Z_LENGTH
        self.z1plot = pg.PlotWidget()

        self.z1_max_rect = pg.QtGui.QGraphicsRectItem(-0.05, -Z_LENGTH, 0.1, Z_LENGTH)
        self.z1_max_rect.setPen(pg.mkPen(None))
        self.z1_max_rect.setBrush(pg.mkBrush('#ffffff'))
        self.z1plot.addItem(self.z1_max_rect)
        
        self.z1_air_pos_rect = pg.QtGui.QGraphicsRectItem(-0.05, -0.1, 0.1, 0.1 + 0.15)
        self.z1_air_pos_rect.setPen(pg.mkPen(None))
        self.z1_air_pos_rect.setBrush(pg.mkBrush('#cfebfd'))
        self.z1plot.addItem(self.z1_air_pos_rect)

        self.z1_rego_rect = pg.QtGui.QGraphicsRectItem(-0.05, -0.1-0.3, 0.1, 0.3)
        self.z1_rego_rect.setPen(pg.mkPen(None))
        self.z1_rego_rect.setBrush(pg.mkBrush('#CA8D42'))
        self.z1plot.addItem(self.z1_rego_rect)

        self.z1_ice_rect = pg.QtGui.QGraphicsRectItem(-0.05, -0.1-0.3-0.3, 0.1, 0.3)
        self.z1_ice_rect.setPen(pg.mkPen(None))
        self.z1_ice_rect.setBrush(pg.mkBrush('#4169E1'))
        self.z1plot.addItem(self.z1_ice_rect)

        self.z1_drill_pos_rect = pg.QtGui.QGraphicsRectItem(-0.030, -0.1, 0.025, 0.1)
        self.z1_drill_pos_rect.setPen(pg.mkPen(None))
        self.z1_drill_pos_rect.setBrush(pg.mkBrush('#808080'))
        self.z1plot.addItem(self.z1_drill_pos_rect)

        self.z2_drill_pos_rect = pg.QtGui.QGraphicsRectItem( 0.010, -0.1, 0.025, 0.1)
        self.z2_drill_pos_rect.setPen(pg.mkPen(None))
        self.z2_drill_pos_rect.setBrush(pg.mkBrush('#ff4041'))
        self.z1plot.addItem(self.z2_drill_pos_rect)
        
        self._init_z_display(self.z1plot,  
            self.HOLE_DISPLAY_WIDTH + self.TARGET_DISPLAY_WIDTH + 1,
            'Z1 and Z2')
        
    def update_status(self, response):
        if (response != None):  
            z1 = response.rig_zdrill
            z2 = response.rig_zheater
            y = response.rig_y
            x = 0.0

            holes = response.holes
            holes_x = [h.x_m for h in holes]
            holes_y = [h.y_m for h in holes]
            self.holes_scatter.setData(holes_x, holes_y)
            
            self.scatter.setData([x], [y])
            self.heater_scatter.setData([x + HeaterDeltaXY[0]], [y + HeaterDeltaXY[1]])
            self.z1_drill_pos_rect.setRect(-0.030, z1, 0.025, -z1+0.15)
            self.z2_drill_pos_rect.setRect( 0.010, z2, 0.025, -z2+0.15)
        
            self.cur_pos_label.setText(
                f"Current Position (Z1, Z2, Y) = ({z1:0.3f}, {z2:0.3f}, {y:0.3f}) [m]")

            if (response.state != mission_control_pb2.STARTUP_IDLE):
                self.set_home.setEnabled(False)
                self.goto_target_y.setEnabled(False)
                self.goto_z1.setEnabled(False)
                self.goto_z2.setEnabled(False)
                
            else:
                self.set_home.setEnabled(True)
                self.goto_target_y.setEnabled(True)
                self.goto_z1.setEnabled(True)
                self.goto_z2.setEnabled(True)
                
        
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
    def _on_speed_change(self):
        #print("Changing speed")
        target_vel = float(self.target_speed.text())
        vel_z1 = (target_vel/30.0)*Z1Cal
        vel_z2 = (target_vel/30.0)*Z2Cal
        vel_y = (target_vel/30.0)*YCal
        self.speed_units.setText(
            f"Speed Conversions:\nZ1 = {vel_z1:0.1f} [mm/s]\nZ2 = {vel_z2:0.1f} [mm/s]\nY = {vel_y:0.1f} [mm/s]")
        
    def update_limits(self, response):
        global Z_LENGTH
        if response != None:
            air_gap = response.air_gap
            max_z1 = response.max_z1
            ice_depth = response.ice_depth
            self.z1_air_pos_rect.setRect(-0.05, -air_gap, 0.1, air_gap+0.15)
            self.z1_rego_rect.setRect(-0.05, -ice_depth, 0.1, ice_depth-air_gap)
            self.z1_ice_rect.setRect(-0.05, -max_z1, 0.1, max_z1-ice_depth)
        


