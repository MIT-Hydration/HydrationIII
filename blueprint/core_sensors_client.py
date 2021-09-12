from __future__ import print_function

import grpc

from .generated import mission_control_pb2
from .generated import mission_control_pb2_grpc

from datetime import datetime, timedelta
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

RPI_IP_ADDRESS_PORT = \
    f"{config.get('Network', 'CoreSensorsRPiAddress')}:" \
    f"{config.get('Network', 'CoreSensorsGRPCPort')}"

HEARTBEAT_TIMEOUT   = \
    config.getint('Network', 'HeartbeatTimeout')
GRPC_CALL_TIMEOUT   = \
    config.getint('Network', 'GRPCTimeout')

def run():
    
    timestamp = int(time.time()*1000)
    with grpc.insecure_channel(RPI_IP_ADDRESS_PORT) as channel:
        stub = mission_control_pb2_grpc.CoreSensorsStub(channel)
        response = stub.HeartBeat (
            mission_control_pb2.HeartBeatRequest(request_timestamp = timestamp),
            timeout = GRPC_CALL_TIMEOUT )
        print("Core Sensors HeartBeat received at: " + str(datetime.now()))
        print(response) #whats the response? the things in the HeartBeat in mission control returns?
        
if __name__ == '__main__':
    run()
