from .generated import echo_pb2_grpc, echo_pb2
from .generated import mission_control_pb2_grpc, mission_control_pb2

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

    def FanCommand(self, request, context):
        timestamp = int(time.time()*1000)
        
        if (request.fan_on):
            self.fan.value = 0.5
        else:
            self.fan.value = 0.0

        return mission_control_pb2.FanCommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            mode = mission_control_pb2.EXECUTED)
