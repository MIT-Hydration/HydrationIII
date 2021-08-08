"""
core_sensors_server.py
"__"

"""

__author__      = "Prakash Manandhar, and Sophie Yang"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar, and Sophie Yang"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Sophie Yang"
__email__ = "scyang@mit.edu"
__status__ = "Production"

from concurrent import futures
import grpc

from .generated import mission_control_pb2_grpc
from .generated import mission_control_pb2 as mcpb
from .hardware import HardwareFactory

import time
import configparser
import blueprint

config = configparser.ConfigParser()
config.read('config.ini')

class CoreSensorsController(mission_control_pb2_grpc.CoreSensorsServicer):

    def __init__(self):

        self.last_weight_on_bit_drill_timestamp = 0
        self.weight_on_bit_drill_N = 0

        self.last_power_meter_timestamp = 0
        self.power_W = 0
        self.total_current_mA = 0

        self.wob_hardware = HardwareFactory.getWOBSensor()
        self.power_meter_hardware = HardwareFactory.getPowerMeter()

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        cpu_temp = HardwareFactory.getMissionControlRPi() \
            .get_cpu_temperature()

        try:
            
            wob_reading = self.wob_hardware.get_force_N()
            self.last_weight_on_bit_drill_timestamp = wob_reading[0]
            self.last_weight_on_bit_drill_N = wob_reading[1]
            
            
            power_meter_power_reading = self.power_meter_hardware.get_active_power_W()
            self.last_power_meter_timestamp = power_meter_power_reading[0]
            self.power_W = power_meter_power_reading[1]
            
            power_meter_current_reading = self.power_meter_hardware.get_current_mA()
            self.total_current_mA = power_meter_current_reading[0]
            
        except Exception as e: #return last known
            info = f"[Error] {str(e)}"
            print(info)

        return mcpb.CoreSensorsHeartBeatResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            cpu_temperature_degC = cpu_temp,
            last_weight_on_bit_drill_timestamp = self.last_weight_on_bit_drill_timestamp,
            weight_on_bit_drill_N = self.weight_on_bit_drill_N,
            last_power_meter_timestamp = self.last_power_meter_timestamp,
            power_W = self.power_W, 
            total_current_mA = self.total_current_mA
            )

IP_ADDRESS_PORT = f"0.0.0.0:{config.get('Network', 'GRPCActualPort')}"

class CoreSensorsServer:

    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        mission_control_pb2_grpc.add_CoreSensorsServicer_to_server(CoreSensorsController(), server)
        server.add_insecure_port(IP_ADDRESS_PORT)
        server.start()
        print("Core Sensors Server Started [OK], Use Ctrl-C to close")
        server.wait_for_termination()

if __name__ == '__main__':
    CoreSensorsServer.run()
