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

GRPC_TIMEOUT = config.getint('Network', 'GRPCTimeout')

def run():
    print(f'timeout = {GRPC_TIMEOUT}')
    print('On Macbook Client')
    with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
        print ('creating stub')
        stub = echo_pb2_grpc.EchoStub(channel)
        print ('trying to communicate ...')
        response = stub.Reply(
	                echo_pb2.EchoRequest(message='Hello World!'),
                        timeout = GRPC_TIMEOUT)
    print("Echo client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    run()
