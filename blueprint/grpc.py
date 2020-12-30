from .generated import echo_pb2_grpc, echo_pb2

class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):
<<<<<<< HEAD
        return echo_pb2.EchoReply(message=f'[macbook pro] You said: {request.message}')
=======
        return echo_pb2.EchoReply(message=f'[Rpi 00] You said: {request.message}')
>>>>>>> 6c88b5c105b30d2fa0e848f071be43e61c49447d
