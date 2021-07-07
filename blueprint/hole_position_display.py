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
from datetime import datetime, timedelta
import time

import grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc


config = configparser.ConfigParser(
    converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config.read('config.ini')
X_LENGTH = config.getfloat('Rig', 'XLength')
Y_LENGTH = config.getfloat('Rig', 'YLength')
Z_LENGTH = config.getfloat('Rig', 'ZLength')
RIG_UNITS = config.get('Rig', 'Units')
HeaterDeltaXY = config.getlist("Rig", "HeaterDeltaXY")
HeaterDeltaXY = [float(HeaterDeltaXY[0]), float(HeaterDeltaXY[1])]

MC_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class SetHomeThread(QtCore.QThread):    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        print("Trying to set Home")
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.SetHomeZ1 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
                response = stub.SetHomeY (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print(response)
                
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

class GotoThread(QtCore.QThread):    
    def __init__(self, delta):
        QtCore.QThread.__init__(self)
        self.delta = delta
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        #print(f"Moving to {self.z}")
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = self._request_response(stub, timestamp)
                
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

    def _request_response(self, stub):
        pass

class GotoZ1Thread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.Z1Move (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta),
                    timeout = GRPC_CALL_TIMEOUT )

class GotoYThread(GotoThread):    
    def _request_response(self, stub, timestamp):
        return stub.YMove (
                    mission_control_pb2.MoveRequest(
                        request_timestamp = timestamp,
                        delta = self.delta),
                    timeout = GRPC_CALL_TIMEOUT )

class HolePositionDisplay(QtWidgets.QWidget):
    def __init__(self, main_window, layout):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.main_window = main_window
        self.threads = []
        self.layout = layout
        self.HOLE_DISPLAY_WIDTH = 4
        self.TARGET_DISPLAY_WIDTH = 4
        self.Z_DISPLAY_WIDTH = 1
        self.DISPLAY_HEIGHT = 10
        self._init_hole_display()
        self._init_target()
        self._init_z1_display()
        
    def _init_hole_display(self):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.plot = pg.PlotWidget()
        self.plot.showGrid(x = True, y = True, alpha = 1.0)
        self.plot.setXRange(-0.05, X_LENGTH + 0.05, padding=0)
        self.plot.setYRange(-0.05, Y_LENGTH + 0.05, padding=0)
        self.plot.getAxis('bottom').setLabel(f'X {RIG_UNITS}')
        self.plot.getAxis('left').setLabel(f'Y {RIG_UNITS}')
        self.scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=3, color='#dc3545'), symbol='x', size=10)
        self.heater_scatter = pg.ScatterPlotItem(
            pen=pg.mkPen(width=3, color='#cfebfd'), symbol='o', size=10)
        
        self.plot.addItem(self.scatter)
        self.plot.addItem(self.heater_scatter)
        self.layout.addWidget(self.plot, 0, 0, 
            self.DISPLAY_HEIGHT, self.HOLE_DISPLAY_WIDTH)

    def _init_target(self):
        start_h = self.HOLE_DISPLAY_WIDTH + 1
        self.layout.addWidget(QtWidgets.QLabel("Relative Motion (During Startup Idle)"), 0, start_h, 1, 4)
        self.layout.addWidget(QtWidgets.QLabel("Y [m]: "), 1, start_h + 2, 1, 1)

        self.target_y = QtWidgets.QLineEdit("")
        self.target_y.setValidator(QtGui.QDoubleValidator())
        
        self.layout.addWidget(self.target_y, 1, start_h + 3, 1, 1)

        self.goto_target_y = QtWidgets.QPushButton("Move Y")
        self.goto_target_y.clicked.connect(self._goto_y)
        self.layout.addWidget(self.goto_target_y, 2, start_h + 2, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel("Z1 [m]: "), 1, start_h, 1, 1)
        
        self.target_z1 = QtWidgets.QLineEdit("")
        self.target_z1.setValidator(QtGui.QDoubleValidator())
        self.layout.addWidget(self.target_z1, 1, start_h + 1, 1, 1)
        
        self.goto_z1 = QtWidgets.QPushButton("Move Z1")
        self.goto_z1.clicked.connect(self._goto_z1)

        self.layout.addWidget(self.goto_z1, 2, start_h, 1, 2)
        
        self.cur_pos_label = QtWidgets.QLabel("Current Position (Z1, Y) [m]")
        self.cur_pos_label.setStyleSheet("color: '#ffc107'")
        self.layout.addWidget(self.cur_pos_label, 5, start_h, 1, 4)

        self.set_home = QtWidgets.QPushButton("Set Current as Origin (Z1, Y)")
        self.set_home.clicked.connect(self._set_home)
        self.layout.addWidget(self.set_home, 6, start_h, 1, 4)

        
    def _goto_y(self):
        client_thread = GotoYThread(float(self.target_y.text()))
        self.threads.append(client_thread)
        client_thread.start()
        
    def _goto_z1(self):
        client_thread = GotoZ1Thread(
            float(self.target_z1.text()))
        self.threads.append(client_thread)
        client_thread.start() 

    def _set_home(self):
        self.main_window.log("Setting Home...")
        client_thread = SetHomeThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def _init_z_display(self, zplot, start_h, label):
        global X_LENGTH, Z_LENGTH, RIG_UNITS
        zplot.showGrid(x = False, y = True, alpha = 1.0)
        zplot.setXRange(-0.0, 0.0, padding=0)
        zplot.setYRange(-Z_LENGTH + 0.05, 0.05, padding=0)
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
        
        self.z1_air_pos_rect = pg.QtGui.QGraphicsRectItem(-0.05, -0.1, 0.1, 0.1)
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

        self.z1_drill_pos_rect = pg.QtGui.QGraphicsRectItem(-0.025, -0.1, 0.05, 0.1)
        self.z1_drill_pos_rect.setPen(pg.mkPen(None))
        self.z1_drill_pos_rect.setBrush(pg.mkBrush('#808080'))
        self.z1plot.addItem(self.z1_drill_pos_rect)

        self._init_z_display(self.z1plot,  
            self.HOLE_DISPLAY_WIDTH + self.TARGET_DISPLAY_WIDTH + 1,
            'Z1 (Drill)')
        
    def update_status(self, response):
        if (response != None):  
            z1 = response.rig_zdrill
            y = response.rig_y
            x = 0.25
            
            self.scatter.setData([x], [y])
            self.heater_scatter.setData([x + HeaterDeltaXY[0]], [y + HeaterDeltaXY[1]])
            self.z1_drill_pos_rect.setRect(-0.025, z1, 0.05, -z1)
        
            self.cur_pos_label.setText(
                f"Current Position (Z1, Y) = ({z1:0.3f}, {y:0.3f}) [m]")

            if (response.state != mission_control_pb2.STARTUP_IDLE):
                self.set_home.setEnabled(False)
                self.goto_target_y.setEnabled(False)
                self.goto_z1.setEnabled(False)
            else:
                self.set_home.setEnabled(True)
                self.goto_target_y.setEnabled(True)
                self.goto_z1.setEnabled(True)
        
    def update_limits(self, response):
        global Z_LENGTH
        if response != None:
            air_gap = response.air_gap
            max_z1 = response.max_z1
            ice_depth = response.ice_depth
            self.z1_air_pos_rect.setRect(-0.05, -air_gap, 0.1, air_gap)
            self.z1_rego_rect.setRect(-0.05, -ice_depth, 0.1, ice_depth-air_gap)
            self.z1_ice_rect.setRect(-0.05, -max_z1, 0.1, max_z1-ice_depth)
        


