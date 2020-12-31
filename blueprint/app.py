from concurrent import futures
import grpc

from .generated import echo_pb2_grpc
from .generated import mission_control_pb2_grpc
from .grpc import Echoer
from .grpc import MissionController

class Server:

    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        echo_pb2_grpc.add_EchoServicer_to_server(Echoer(), server)
        mission_control_pb2_grpc.add_MissionControlServicer_to_server(MissionController(), server)
        server.add_insecure_port('0.0.0.0:50051')
        server.start()
        server.wait_for_termination()
