from __future__ import print_function
import logging

import grpc

from .generated import echo_pb2
from .generated import echo_pb2_grpc

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

RPI_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'MissionControlRPiIPAddress')}:" \
    f"{config.get('Network', 'GRPCPort')}"

def run():
    print('On Macbook Client')
    with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
        stub = echo_pb2_grpc.EchoStub(channel)
        response = stub.Reply(echo_pb2.EchoRequest(message='Hello World!'))
    print("Echo client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    run()
