from .generated import echo_pb2_grpc, echo_pb2
from .generated import mission_control_pb2_grpc, mission_control_pb2
from .hardware import HardwareFactory

import time

from gpiozero import PWMLED
from gpiozero import CPUTemperature

class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):
        return echo_pb2.EchoReply(message=f'[Rpi 00] You said: {request.message}')

class MissionController(mission_control_pb2_grpc.MissionControlServicer):

    fan = PWMLED(12)
    cpu = CPUTemperature()

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        return mission_control_pb2.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            fan_on = (self.fan.value > 0.0),
            cpu_temperature_degC = self.cpu.temperature,
            mode = mission_control_pb2.READY)

    def RigMove(self, request, context):
        return # no implementation currently

class DrillController(mission_control_pb2_grpc.MissionControlServicer):
    drill_mode = False
    drill_calibrated = False
    drill_hw = HardwareFactory.getDrill()

    def start_drill_mode(self):
        drill_hw.start_sensor_readings()

    def stop_drill_mode(self):
        drill_hw.stop_sensor_readings()

    def DrillMode(self, request, context):
        timestamp = int(time.time()*1000)

        if (self.drill_mode == False) and (request.drill_mode == True):
            self.start_drill_mode()
        elif (self.drill_mode == True) and (request.drill_mode = False):
            self.stop_drill_mode()

        return mission_control_pb2.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mission_control_pb2.EXECUTED)

    def DrillDescendingDrilling:
