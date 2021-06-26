#!/usr/bin/env python
#Author velociraptor Genjix <aphidia@hotmail.com>

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtCore, QtWidgets, QtGui, QtStateMachine

class LightWidget(QtWidgets.QWidget):
    def __init__(self, colour):
        super(LightWidget, self).__init__()
        self.colour = colour
        self.onVal = False
    def isOn(self):
        return self.onVal
    def setOn(self, on):
        if self.onVal == on:
            return
        self.onVal = on
        self.update()
    @Slot()
    def turnOff(self):
        self.setOn(False)
    @Slot()
    def turnOn(self):
        self.setOn(True)
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.colour)

        if self.onVal:
            painter.setBrush(self.colour)
        else:
            painter.setBrush(Qt.blue)

        painter.drawEllipse(0, 0, self.width(), self.width())

        font = painter.font()
        font.setPixelSize(48)
        painter.setFont(font)
        rectangle = QRect(0, 0, 100, 50)
        boundingRect = QRect()
        painter.drawText(rectangle, str("Hello"))
        pen = painter.pen()
        pen.setColor(Qt.white)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.drawRect(boundingRect.adjusted(0, 0, -pen.width(), -pen.width()))
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawRect(rectangle.adjusted(0, 0, -pen.width(), -pen.width()))

        painter.setBrush(Qt.white)
        painter.drawText(50, 50, "hello")

    on = Property(bool, isOn, setOn)

class TrafficLightWidget(QtWidgets.QWidget):
    def __init__(self):
        super(TrafficLightWidget, self).__init__()
        vbox = QtWidgets.QVBoxLayout(self)
        self.redLight = LightWidget(Qt.red)
        vbox.addWidget(self.redLight)
        self.yellowLight = LightWidget(Qt.yellow)
        vbox.addWidget(self.yellowLight)
        self.greenLight = LightWidget(Qt.green)
        vbox.addWidget(self.greenLight)
        pal = QPalette()
        pal.setColor(QPalette.Base, Qt.black)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

def createLightState(light, duration, parent=None):
    lightState = QtStateMachine.QState(parent)
    timer = QTimer(lightState)
    timer.setInterval(duration)
    timer.setSingleShot(True)
    timing = QtStateMachine.QState(lightState)
    timing.entered.connect(light.turnOn)
    timing.entered.connect(timer.start)
    timing.exited.connect(light.turnOff)
    done = QtStateMachine.QFinalState(lightState)
    timing.addTransition(timer, SIGNAL('timeout()'), done)
    lightState.setInitialState(timing)
    return lightState

class TrafficLight(QtWidgets.QWidget):
    def __init__(self):
        super(TrafficLight, self).__init__()
        vbox = QtWidgets.QVBoxLayout(self)
        widget = TrafficLightWidget()
        vbox.addWidget(widget)
        vbox.setContentsMargins(0, 0, 0, 0)

        machine = QtStateMachine.QStateMachine(self)
        redGoingYellow = createLightState(widget.redLight, 1000)
        redGoingYellow.setObjectName('redGoingYellow')
        yellowGoingGreen = createLightState(widget.redLight, 1000)
        yellowGoingGreen.setObjectName('redGoingYellow')
        redGoingYellow.addTransition(redGoingYellow, SIGNAL('finished()'), yellowGoingGreen)
        greenGoingYellow = createLightState(widget.yellowLight, 3000)
        greenGoingYellow.setObjectName('redGoingYellow')
        yellowGoingGreen.addTransition(yellowGoingGreen, SIGNAL('finished()'), greenGoingYellow)
        yellowGoingRed = createLightState(widget.greenLight, 1000)
        yellowGoingRed.setObjectName('redGoingYellow')
        greenGoingYellow.addTransition(greenGoingYellow, SIGNAL('finished()'), yellowGoingRed)
        yellowGoingRed.addTransition(yellowGoingRed, SIGNAL('finished()'), redGoingYellow)

        machine.addState(redGoingYellow)
        machine.addState(yellowGoingGreen)
        machine.addState(greenGoingYellow)
        machine.addState(yellowGoingRed)
        machine.setInitialState(redGoingYellow)
        machine.start()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = TrafficLight()
    widget.resize(110, 300)
    widget.show()
    sys.exit(app.exec_())
