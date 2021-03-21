import sys
from urllib.request import urlopen

import logging

import grpc

from .generated import echo_pb2
from .generated import echo_pb2_grpc
from .generated import mission_control_pb2, mission_control_pb2_grpc

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QDateTime

from QLed import QLed

from datetime import datetime
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

RPI_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

HEARTBEAT_TIMEOUT   = \
    config.getint('Network', 'HeartbeatTimeout')
GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.pyqtSignal(object)

    def __init__(self, url):
        QtCore.QThread.__init__(self)
        self.url = url

    def run(self):
        try:
            info = urlopen(self.url).info()   
        except:
            info = f"Error opening URL: {self.url}"
        self.data_downloaded.emit('%s\n%s' % (self.url, info))

class RPiHeartBeat(QtCore.QThread):
    heartbeat_done = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.HeartBeat (
                    mission_control_pb2.HeartBeatRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi HeartBeat received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.heartbeat_done.emit(response)


class RPiFanThread(QtCore.QThread):
    fan_done = QtCore.pyqtSignal(object)
    state = False

    def __init__(self, state):
        QtCore.QThread.__init__(self)
        self.state = state
        
    def run(self):
        global RPI_IP_ADDRESS_PORT, GRPC_CALL_TIMEOUT
        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.FanCommand (
                    mission_control_pb2.FanCommandRequest(
                        request_timestamp = timestamp, fan_on = self.state),
                    timeout = GRPC_CALL_TIMEOUT )
                print("Mission Control RPi FanCommandResponse received at: " + str(datetime.now()))
                print(response)
        
        except Exception as e:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            print(info)
            
        self.fan_done.emit(response)

class RPiServerThread(QtCore.QThread):
    echo_done = QtCore.pyqtSignal(object)

    def __init__(self, echo_text):
        QtCore.QThread.__init__(self)
        self.echo_text = echo_text

    def run(self):
        global RPI_IP_ADDRESS_PORT
        try:
            with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
                stub = echo_pb2_grpc.EchoStub(channel)
                response = stub.Reply(echo_pb2.EchoRequest(message=self.echo_text))
                info = "Echo client received: " + response.message   
        except:
            info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}"
        self.echo_done.emit(f'Response from {RPI_IP_ADDRESS_PORT}\n{info}')

class MainWindow(QtWidgets.QWidget):
    
    def _addStatus(self, led, description):
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(led)
        h_layout.addWidget(QtWidgets.QLabel(description))
        h_layout.addStretch(5)
        led.setMaximumHeight(20)
        led.setMaximumWidth(20)
        self.status_layout.addLayout(h_layout)

    def _initStatusWidgets(self):
        self.status_groupbox = QtWidgets.QGroupBox("STATUS")
        self.status_layout = QtWidgets.QVBoxLayout()
        self.status_groupbox.setLayout(self.status_layout)
        self.main_h_layout.addWidget(self.status_groupbox)

        self.mission_control_led=QLed(self, onColour=QLed.Green, shape=QLed.Circle)
        self.mission_control_led.value=False
        self._addStatus(self.mission_control_led, "Mission Control")

        self.drill_asm_led=QLed(self, onColour=QLed.Green, shape=QLed.Circle)
        self.drill_asm_led.value=False
        self._addStatus(self.drill_asm_led, "Drilling Assembly")

        self.water_prod_led = QLed(self, onColour=QLed.Green, shape=QLed.Circle)
        self.water_prod_led.value=False
        self._addStatus(self.water_prod_led, "Water Production")

        self.status_layout.addWidget(QtWidgets.QLabel('-------------------'))
        self.fan_on_led = QLed(self, onColour=QLed.Green, shape=QLed.Circle)
        self.fan_on_led.value = False
        self._addStatus(self.fan_on_led, "MiCon CPU Fan")
        
        h_layout_temp = QtWidgets.QHBoxLayout()
        h_layout_temp.addWidget(QtWidgets.QLabel("MC Temp.:"))
        self.mc_temp_label = QtWidgets.QLabel("N/A [degC]")
        self.mc_temp_label.setMinimumWidth(70)
        h_layout_temp.addWidget(self.mc_temp_label)
        self.status_layout.addLayout(h_layout_temp)

        self.status_layout.addStretch()
        
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel("Trip Time:"))
        self.rtt_label = QtWidgets.QLabel("N/A [ms]")
        self.rtt_label.setMinimumWidth(70)
        h_layout.addWidget(self.rtt_label)
        self.status_layout.addLayout(h_layout)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_h_layout = QtWidgets.QHBoxLayout()
        self._initStatusWidgets()
        
        self.list_widget = QtWidgets.QListWidget()
        self.test_client_button = QtWidgets.QPushButton("Test Client")
        
        self.echo_button = QtWidgets.QPushButton("Echo Server")
        self.echo_textedit = QtWidgets.QTextEdit("Change the text and test!!!")
        self.echo_textedit.setMaximumHeight(20)
        #self.echo_textedit.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        echo_layout = QtWidgets.QHBoxLayout()
        echo_layout.addWidget(self.echo_textedit)
        echo_layout.addWidget(self.echo_button)

        self.fan_on_button = QtWidgets.QPushButton("Turn ON Fan")
        self.fan_off_button = QtWidgets.QPushButton("Turn OFF Fan")
        fan_layout = QtWidgets.QHBoxLayout()
        fan_layout.addWidget(self.fan_on_button)
        fan_layout.addWidget(self.fan_off_button)

        self.fan_on_button.clicked.connect(self.turn_fan_on)
        self.fan_off_button.clicked.connect(self.turn_fan_off)
        
        self.test_client_button.clicked.connect(self.start_download)
        self.echo_button.clicked.connect(self.start_echo)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(echo_layout)
        layout.addLayout(fan_layout)
        
        layout.addWidget(self.test_client_button)
        layout.addStretch()
        layout.addWidget(self.list_widget)

        self.main_h_layout.addLayout(layout)
        self.setLayout(self.main_h_layout)

        self.heartbeat_timer=QTimer()
        self.heartbeat_timer.timeout.connect(self.onHeartBeat)
        self.startHeartBeatTimer()

    def start_download(self):
        urls = ['http://google.com', 'http://twitter.com', 'http://yandex.ru',
                'http://stackoverflow.com/', 'http://www.youtube.com/'
                ]
        self.threads = []
        for url in urls:
            downloader = DownloadThread(url)
            downloader.data_downloaded.connect(self.on_data_ready)
            self.threads.append(downloader)
            downloader.start()

    def start_echo(self):
        self.threads = []
        client_thread = RPiServerThread(self.echo_textedit.toPlainText())
        client_thread.echo_done.connect(self.on_data_ready)
        self.threads.append(client_thread)
        client_thread.start()

    def set_fan(self, state):
        self.threads = []
        client_thread = RPiFanThread(state)
        client_thread.fan_done.connect(self.on_fan_done)
        self.threads.append(client_thread)
        client_thread.start()

    def turn_fan_on(self):
        self.set_fan(True)
    
    def turn_fan_off(self):
        self.set_fan(False)

    def on_fan_done(self):
        return

    def onHeartBeat(self):
        self.threads = []
        client_thread = RPiHeartBeat()
        client_thread.heartbeat_done.connect(self.on_heartbeat_received)
        self.threads.append(client_thread)
        client_thread.start()

    def on_heartbeat_received(self, response):
        if (response != None):
            self.mission_control_led.value = True
            self.fan_on_led.value = response.fan_on
            self.mc_temp_label.setText(f"{response.cpu_temperature_degC:.2f} [degC]")
            rtt_time = response.timestamp - response.request_timestamp
            self.rtt_label.setText(f"{rtt_time} [ms]")
            
        else:
            self.mission_control_led.value = False

    def on_data_ready(self, data):
        print(data)
        self.list_widget.addItem(data)

    def startHeartBeatTimer(self):
        global HEARTBEAT_TIMEOUT
        self.heartbeat_timer.start(HEARTBEAT_TIMEOUT)
        
    def endHeartBeatTimer(self):
        self.heartbeat_timer.stop()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())