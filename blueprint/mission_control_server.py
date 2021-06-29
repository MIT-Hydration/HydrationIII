from .generated import mission_control_pb2_grpc
from .generated import mission_control_pb2 as mcpb
from .hardware import HardwareFactory

import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class MissionController(mission_control_pb2_grpc.MissionControlServicer):

    mission_time_started = False
    mission_start_time = -1
    mode = mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS

    def __init__(self):
        self._stopMotors()
        
    def GetMajorModes(self, request, context):
        timestamp = int(time.time()*1000)
        modes = [
                mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS,
                #mcpb.MAJOR_MODE_HOME_Z1_Z2,
                #mcpb.MAJOR_MODE_MOVE_X_Y,
                mcpb.MAJOR_MODE_DRILL_BOREHOLE,
                # mcpb.MAJOR_MODE_CASE_BOREHOLE,
                # mcpb.MAJOR_MODE_INSERT_HEATER,
                # mcpb.MAJOR_MODE_MINE_WATER,
                # mcpb.MAJOR_MODE_DATA_DOWNLOAD,
                # mcpb.MAJOR_MODE_TROUBLESHOOT,
            ]
        mode_labels = [
            "01 Startup/calibrate",
            #"02 Home Z1, Z2",
            #"03 Move X, Y",
            "04 Drill borehole",
            # "05 Case borehole",
            # "06 Insert heater",
            # "07 Mine water",
            # "08 Data download",
            # "09 Troubleshoot"
            ]
        return mcpb.MajorModesList(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            modes = modes,
            mode_labels = mode_labels)

    def DrillAssemblyStatus(self, request, context):
        #(DrillAssemblyStatusRequest) returns (DrillAssemblyStatusResponse);
        timestamp = int(time.time()*1000)

        tachometer_hardware = HardwareFactory.getTachometer()

        return mcpb.DrillAssemblyStatusResponse(
            request_timestamp_ms = request.request_timestamp_ms,
            timestamp_ms = timestamp,
            tachometer_RPM = tachometer_hardware.get_rpm()
            )

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        cpu_temp = HardwareFactory.getMissionControlRPi() \
            .get_cpu_temperature()

        rig_hardware = HardwareFactory.getRig()

        if (self.mission_time_started):
            mission_time = timestamp - self.mission_time
        else:
            mission_time = 0

        return mcpb.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            cpu_temperature_degC = cpu_temp,
            mission_time_ms = mission_time,
            zdrill_servo_moving = rig_hardware.isZ1Moving(),
            zwater_servo_moving = rig_hardware.isZ2Moving(),
            x_servo_moving = rig_hardware.isXMoving(),
            y_servo_moving = rig_hardware.isYMoving(),
            rig_zdrill = rig_hardware.getPosition()[0],
            rig_zwater = rig_hardware.getPosition()[1],
            rig_x = rig_hardware.getPosition()[2],
            rig_y = rig_hardware.getPosition()[3],
            rig_torque_z1 = rig_hardware.getTorque(0),
            mode = self.mode)

    def RigMove(self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.gotoPosition(request.x, request.y)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def ZMove(self, request, context, f):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        f(request.z)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def Z1Move(self, request, context):
        rig_hardware = HardwareFactory.getRig()
        return self.ZMove(request, context, rig_hardware.gotoPositionZ1)

    def Z2Move(self, request, context):
        rig_hardware = HardwareFactory.getRig()
        return self.ZMove(request, context, rig_hardware.gotoPositionZ2)

    def _stopMotors(self):
        # todo stop motors
        pass

    def _putInStartupDiagnosticsMode(self):
        self._stopMotors()
        self.mode =  mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS

    def SetMode (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode == request.mode): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTED)

        if (request.mode == mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS):
            self._putInStartupDiagnosticsMode()
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTED)

    def StartMissionClock (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.mission_time = timestamp
        self.mission_time_started = True

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetHomeZ1 (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.setHomeZ1()

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetHomeZ2 (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.setHomeZ2()

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetHomeX (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.setHomeX()

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetHomeY (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.setHomeY()

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def StartHomeAxis (self, request, context, f):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        f()

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def StartHomeZ1 (self, request, context):
        rig_hardware = HardwareFactory.getRig()
        return self.StartHomeAxis(request, context, rig_hardware.homeZ1)

    def StartHomeZ2 (self, request, context):
        rig_hardware = HardwareFactory.getRig()
        return self.StartHomeAxis(request, context, rig_hardware.homeZ2)

    def StartHomeX (self, request, context):
        rig_hardware = HardwareFactory.getRig()
        return self.StartHomeAxis(request, context, rig_hardware.homeX)

    def StartHomeY (self, request, context):
        rig_hardware = HardwareFactory.getRig()
        return self.StartHomeAxis(request, context, rig_hardware.homeY)

    def StartSpinPump (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        pump = HardwareFactory.getPump()
        pump.set_direction(1)
        pump.set_speed_pom(66)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)



    def EmergencyStop(self, request, context):
        timestamp = int(time.time()*1000)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.emergencyStop()

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def StartSpinPump (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        pump = HardwareFactory.getPump()
        pump.set_direction(1)
        pump.set_speed_pom(66)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def StartSpinPump (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        pump = HardwareFactory.getPump()
        pump.set_direction(1)
        pump.set_speed_pom(66)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def StopSpinPump (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        pump = HardwareFactory.getPump()
        pump.set_direction(1)
        pump.set_speed_pom(0)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)
