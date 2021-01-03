from concurrent import futures
import grpc

from .generated import echo_pb2_grpc
from .generated import mission_control_pb2_grpc
from .grpc import DrillAsmController

class DrillAsmServer:

    @staticmethod
    def run():
        DrillAsmController.initBoard()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        mission_control_pb2_grpc.add_DrillAsmServicer_to_server(DrillAsmController(), server)
        server.add_insecure_port('0.0.0.0:50051')
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    DrillAsemServer.run()