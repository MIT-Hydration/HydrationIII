from .generated import echo_pb2_grpc, echo_pb2
from .generated import mission_control_pb2_grpc, mission_control_pb2

import time

class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):
        return echo_pb2.EchoReply(message=f'[Rpi 00] You said: {request.message}')

class MissionController(mission_control_pb2_grpc.MissionControlServicer):

    def HeartBeat(self, request, context):
        request_timestamp = request.request_timestamp
        timestamp = int(time.time())
        return mission_control_pb2.HeartBeatReply(
            request_timestamp = request_timestamp,
            timestamp = timestamp,
            mode = mission_control_pb2.READY)