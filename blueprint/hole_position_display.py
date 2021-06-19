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


config = configparser.ConfigParser()
config.read('config.ini')
X_LENGTH = config.getfloat('Rig', 'XLength')
Y_LENGTH = config.getfloat('Rig', 'YLength')
RIG_UNITS = config.get('Rig', 'Units')

MC_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class GotoXYThread(QtCore.QThread):    
    def __init__(self, x, y):
        QtCore.QThread.__init__(self)
        self.x = x
        self.y = y
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.RigMove (
                    mission_control_pb2.RigMoveCommandRequest(
                        request_timestamp = timestamp,
                        x = self.x, y = self.y),
                    timeout = GRPC_CALL_TIMEOUT )
                
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

class SetHomeThread(QtCore.QThread):    
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global MC_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(MC_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.SetHomeZ1 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                
                response = stub.SetHomeZ2 (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                
                response = stub.SetHomeX (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )

                response = stub.SetHomeY (
                    mission_control_pb2.StartCommandRequest(
                        request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                
        except Exception as e:
            info = f"Error connecting to RPi Server at: {MC_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)

class GotoZThread(QtCore.QThread):    
    def __init__(self, z):
        QtCore.QThread.__init__(self)
        self.z = z
        
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

class GotoZ1Thread(GotoZThread):    
    def _request_response(self, stub, timestamp):
        return stub.Z1Move (
                    mission_control_pb2.ZMoveRequest(
                        request_timestamp = timestamp,
                        z = self.z),
                    timeout = GRPC_CALL_TIMEOUT )

class GotoZ2Thread(GotoZThread):    
    def _request_response(self, stub, timestamp):
        return stub.Z2Move (
                    mission_control_pb2.ZMoveRequest(
                        request_timestamp = timestamp,
                        z = self.z),
                    timeout = GRPC_CALL_TIMEOUT )


class HolePositionDisplay(QtWidgets.QWidget):
    def __init__(self, layout):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        self.threads = []
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

        self.target_x = QtWidgets.QLineEdit("")
        self.target_x.setValidator(QtGui.QDoubleValidator())
            
        self.target_y = QtWidgets.QLineEdit("")
        self.target_y.setValidator(QtGui.QDoubleValidator())
        
        self.layout.addWidget(self.target_x, 1, start_h + 1, 1, 1)
        self.layout.addWidget(self.target_y, 1, start_h + 3, 1, 1)

        self.goto_target_xy = QtWidgets.QPushButton("GoTo Target (X, Y)")
        self.goto_target_xy.clicked.connect(self._goto_xy)
        self.layout.addWidget(self.goto_target_xy, 0, start_h + 2, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel("Z1: "), 2, start_h, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel("Z2: "), 2, start_h + 2, 1, 1)
        
        self.target_z1 = QtWidgets.QLineEdit("")
        self.target_z1.setValidator(QtGui.QDoubleValidator())
        
        self.target_z2 = QtWidgets.QLineEdit("")
        self.target_z2.setValidator(QtGui.QDoubleValidator())

        self.layout.addWidget(self.target_z1, 2, start_h + 1, 1, 1)
        self.layout.addWidget(self.target_z2, 2, start_h + 3, 1, 1)

        self.goto_z1 = QtWidgets.QPushButton("GoTo Target (Z1)")
        self.goto_z1.clicked.connect(self._goto_z1)

        self.goto_z2 = QtWidgets.QPushButton("GoTo Target (Z2)")
        self.goto_z2.clicked.connect(self._goto_z2)
        
        self.layout.addWidget(self.goto_z1, 3, start_h, 1, 2)
        self.layout.addWidget(self.goto_z2, 3, start_h + 2, 1, 2)
        
        self.cur_pos_label = QtWidgets.QLabel("Current Position (Z1, Z2, X, Y) [m]")
        self.layout.addWidget(self.cur_pos_label, 5, start_h, 1, 2)

        self.set_home = QtWidgets.QPushButton("Set Current as Origin (Z1, Z2, X, Y)")
        self.set_home.clicked.connect(self._set_home)
        self.layout.addWidget(self.set_home, 6, start_h, 1, 4)

        
    def _goto_xy(self):
        client_thread = GotoXYThread(
            float(self.target_x.text()), 
            float(self.target_y.text()))
        self.threads.append(client_thread)
        client_thread.start() 
        
    def _goto_z1(self):
        client_thread = GotoZ1Thread(
            float(self.target_z1.text()))
        self.threads.append(client_thread)
        client_thread.start() 

    def _goto_z2(self):
        client_thread = GotoZ2Thread(
            float(self.target_z2.text()))
        self.threads.append(client_thread)
        client_thread.start() 

    def _set_home(self):
        client_thread = SetHomeThread()
        self.threads.append(client_thread)
        client_thread.start() 

    def _init_z_display(self, zplot, zscatter, start_h, label):
        global X_LENGTH, Y_LENGTH, RIG_UNITS
        zplot.showGrid(x = False, y = True, alpha = 1.0)
        zplot.setXRange(-0.0, 0.0, padding=0)
        zplot.setYRange(-Y_LENGTH + 0.05, 0.05, padding=0)
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
            z1 = response.rig_zdrill
            z2 = response.rig_zwater
            x = response.rig_x
            y = response.rig_y
            
            self.scatter.setData([x], [y])
            self.z1scatter.setData([0.0], [z1])
            self.z2scatter.setData([0.0], [z2])
            self.cur_pos_label.setText(
                f"(Z1, Z2, X, Y) = ({z1:0.3f}, {z2:0.3f}{x:0.3f}{y:0.3f}) [m]")
        



