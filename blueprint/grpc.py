from .generated import echo_pb2_grpc, echo_pb2
from .generated import mission_control_pb2_grpc, mission_control_pb2
from .hardware import HardwareFactory

import time

class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):
        return echo_pb2.EchoReply(message=f'[Rpi 00] You said: {request.message}')

class MissionController(mission_control_pb2_grpc.MissionControlServicer):

    mission_time_started = False
    mission_start_time = -1
    mode = mission_control_pb2.STARTUP_DIAGNOSTICS

    def __init__(self):
        self._stopMotors()

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        cpu_temp = HardwareFactory.getMissionControlRPi() \
            .get_cpu_temperature()

        return mission_control_pb2.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            cpu_temperature_degC = cpu_temp,
            mission_time = timestamp - self.mission_start_time,
            mode = self.mode)

    def RigMove(self, request, context):
        return # no implementation currently

    def _stopMotors(self):
        # todo stop motors
        pass

    def _putInStartupDiagnosticsMode(self):
        self._stopMotors()
        self.mode =  mission_control_pb2.STARTUP_DIAGNOSTICS

    def SetMode (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode == request.mode): # do nothing
            return mission_control_pb2.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mission_control_pb2.EXECUTED)

        if (request.mode == mission_control_pb2.STARTUP_DIAGNOSTICS):
            self._putInStartupDiagnosticsMode()
            return mission_control_pb2.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mission_control_pb2.EXECUTED)

    def StartMissionClock (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mission_control_pb2.STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mission_control_pb2.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mission_control_pb2.INVALID_STATE)

        self.mission_start_time = timestamp
        self.mission_time_started = True
        
        return mission_control_pb2.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mission_control_pb2.EXECUTED)


class DrillController(mission_control_pb2_grpc.MissionControlServicer):
    drill_mode = False
    drill_calibrated = False
    drill_hw = HardwareFactory.getDrill()

    def start_drill_mode(self):
        drill_hw.start_sensor_readings()

    def stop_drill_mode(self):
        drill_hw.stop_sensor_readings()

    def DrillMode(self, request, context):
        timestamp = int(time.time()*1000)

        if (self.drill_mode == False) and (request.drill_mode == True):
            self.start_drill_mode()
        elif (self.drill_mode == True) and (request.drill_mode == False):
            self.stop_drill_mode()

        return mission_control_pb2.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mission_control_pb2.EXECUTED)

    def DrillDescendingDrilling(self):
        pass
