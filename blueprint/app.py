from concurrent import futures
import grpc

from .generated import echo_pb2_grpc, echo_pb2
from .generated import mission_control_pb2_grpc
from .mission_control_server import MissionController

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

MC_IP_ADDRESS_PORT = f"0.0.0.0:{config.get('Network', 'GRPCActualPort')}"


class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):
        return echo_pb2.EchoReply(message=f'[Rpi 00] You said: {request.message}')

class Server:

    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        echo_pb2_grpc.add_EchoServicer_to_server(Echoer(), server)
        mission_control_pb2_grpc.add_MissionControlServicer_to_server(MissionController(), server)
        server.add_insecure_port(MC_IP_ADDRESS_PORT)
        print("Before server.start()")
        server.start()
        print("Mission Control Server Started [OK], Use Ctrl-C to close")
        server.wait_for_termination()
