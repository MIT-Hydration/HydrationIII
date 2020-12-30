from __future__ import print_function
import logging

import grpc

from .generated import echo_pb2
from .generated import echo_pb2_grpc


def run():
<<<<<<< HEAD
    print('On Macbook Client')
    with grpc.insecure_channel('96.237.232.240:50051') as channel:
=======
    with grpc.insecure_channel('192.168.1.182:50051') as channel:
>>>>>>> 6c88b5c105b30d2fa0e848f071be43e61c49447d
        stub = echo_pb2_grpc.EchoStub(channel)
        response = stub.Reply(echo_pb2.EchoRequest(message='Hello World!'))
    print("Echo client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
