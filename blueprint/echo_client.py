from __future__ import print_function
import logging

import grpc

from .generated import echo_pb2
from .generated import echo_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = echo_pb2_grpc.EchoStub(channel)
        response = stub.Reply(echo_pb2.EchoRequest(message='Hello World!'))
    print("Echo client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()