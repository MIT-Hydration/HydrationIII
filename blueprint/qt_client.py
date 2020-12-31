import sys
from urllib.request import urlopen

import logging

import grpc

from .generated import echo_pb2
from .generated import echo_pb2_grpc


from PyQt5 import QtCore, QtGui, QtWidgets
from QLed import QLed

RPI_IP_ADDRESS_PORT = '96.237.232.240:50051'

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
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_widget = QtWidgets.QListWidget()
        self.button = QtWidgets.QPushButton("Start")
        self.echo_button = QtWidgets.QPushButton("Echo Server")
        self.echo_textedit = QtWidgets.QTextEdit("Change the text and test!!!")
        self.button.clicked.connect(self.start_download)
        self.echo_button.clicked.connect(self.start_echo)

        self._led=QLed(self, onColour=QLed.Green, shape=QLed.Circle)
        self._led.value=False

        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self._led)
        status_layout.addWidget(QtWidgets.QLabel("Mission Control Status"))
        status_layout.addStretch(1)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(status_layout)
        layout.addWidget(self.button)
        layout.addWidget(self.echo_button)
        layout.addWidget(self.echo_textedit)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

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

    
    def on_data_ready(self, data):
        print(data)
        self.list_widget.addItem(data)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())