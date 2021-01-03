from .generated import echo_pb2_grpc, echo_pb2
from .generated import mission_control_pb2_grpc, mission_control_pb2

import grpc

import time

import threading
import gpiozero

RPI_DRILL_ASM_IP_PORT = '192.168.1.197:50051'
GRPC_CALL_TIMEOUT = 1000

class Echoer(echo_pb2_grpc.EchoServicer):
    def Reply(self, request, context):
        return echo_pb2.EchoReply(message=f'[Rpi 00] You said: {request.message}')

class MissionController(mission_control_pb2_grpc.MissionControlServicer):
    def HeartBeat(self, request, context):
        global RPI_DRILL_ASM_IP_PORT
        global GRPC_CALL_TIMEOUT

        response = None
        try:
            timestamp = int(time.time()*1000)
            with grpc.insecure_channel(RPI_DRILL_ASM_IP_PORT) as channel:
                stub = mission_control_pb2_grpc.MissionControlStub(channel)
                response = stub.HeartBeat (
                    mission_control_pb2.HeartBeatRequest(request_timestamp = timestamp),
                    timeout = GRPC_CALL_TIMEOUT )
                #print("Drill Asm Control RPi HeartBeat received at: " + str(datetime.now()))
                #print(response)
        
        except Exception as e:
            response  = None
            #info = f"Error connecting to RPi Server at: {RPI_IP_ADDRESS_PORT}: + {str(e)}"
            #print(info)

        timestamp_res = int(time.time()*1000)
        return mission_control_pb2.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp_res,
            drill_subsystem_online = (response != None),
            mode = mission_control_pb2.READY)

    def DrillAsmStatus(self, request, context):
        timestamp = int(time.time()*1000)
        return mission_control_pb2.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            mode = mission_control_pb2.READY)

class DrillAsmController(mission_control_pb2_grpc.DrillAsmServicer):

    __drill_out = gpiozero.LED(17, initial_value = False)
    __tachometer = 0.0

    @staticmethod
    def initBoard():
        DrillAsmController.__drill_out.off()

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        return mission_control_pb2.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            mode = mission_control_pb2.READY)    

    def DrillAsmStatus(self, request, context):
        timestamp = int(time.time()*1000)
        return mission_control_pb2.DrillAsmStatusResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            drill_on = (DrillAsmController.__drill_out.value == 1),
            tachometer = DrillAsmController.__tachometer
            )
