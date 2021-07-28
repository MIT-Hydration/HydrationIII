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

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        cpu_temp = HardwareFactory.getMissionControlRPi() \
            .get_cpu_temperature()

        try:
            wob_hardware = HardwareFactory.getWOBSensor()
            wob_reading = wob_hardware.get_force_N()
            self.last_weight_on_bit_drill_timestamp = wob_reading[0]
            self.last_weight_on_bit_drill_N = wob_reading[1]
            #GET WOB READING and power reading and retrun it in the return below and cuz its outside it will return both times
            #even w exception will still go there bc outside exception
        except Exception as e: #return last known
            info = f"[Error] {str(e)}"
            print(info)

        return mcpb.CoreSensorsHeartBeatResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            cpu_temperature_degC = cpu_temp,
            )