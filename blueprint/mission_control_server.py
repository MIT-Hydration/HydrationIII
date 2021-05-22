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
        self.air_gap = config.getfloat('Rig', 'AirGap')
        self.max_z1_travel = config.getfloat('Rig', 'MaxZ1Travel')
        self.current_limit_lower = config.getfloat('Rig', 'CurrentLimitLower')
        self.current_limit_upper = config.getfloat('Rig', 'CurrentLimitUpper')
        self.WOB_limit_lower = config.getfloat('Rig', 'WOBLimitLower')
        self.WOB_limit_upper = config.getfloat('Rig', 'WOBLimitUpper')
        self.RPM_limit_lower = config.getfloat('Rig', 'RPMLimitLower')
        self.RPM_limit_upper = config.getfloat('Rig', 'RPMLimitUpper')
        self.Z1_servo_torque = config.getfloat('Rig', 'Z1ServoTorque')
        self.Z2_servo_torque = config.getfloat('Rig', 'Z2ServoTorque')
        self.X_servo_torque = config.getfloat('Rig', 'XServoTorque')
        self.Y_servo_torque = config.getfloat('Rig', 'YServoTorque')

    def GetMajorModes(self, request, context):
        timestamp = int(time.time()*1000)
        modes = [
                mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS,
                mcpb.MAJOR_MODE_HOME_Z1_Z2,
                mcpb.MAJOR_MODE_MOVE_X_Y,
                mcpb.MAJOR_MODE_DRILL_BOREHOLE,
                mcpb.MAJOR_MODE_CASE_BOREHOLE,
                mcpb.MAJOR_MODE_INSERT_HEATER,
                mcpb.MAJOR_MODE_MINE_WATER,
                mcpb.MAJOR_MODE_DATA_DOWNLOAD,
                mcpb.MAJOR_MODE_TROUBLESHOOT,
            ]
        mode_labels = [
            "01 Startup/calibrate",
            "02 Home Z1, Z2",
            "03 Move X, Y",
            "04 Drill borehole",
            "05 Case borehole",
            "06 Insert heater",
            "07 Mine water",
            "08 Data download",
            "09 Troubleshoot"       
            ]
        return mcpb.MajorModesList(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            modes = modes,
            mode_labels = mode_labels)

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
            x_servo_moving = rig_hardware.isXMoving(),
            y_servo_moving = rig_hardware.isYMoving(),
            rig_x = rig_hardware.getPosition()[0],
            rig_y = rig_hardware.getPosition()[1],
            mode = self.mode)

    def RigMove(self, request, context):
        return # no implementation currently

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

    def StartHomeX (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.homeX()
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetAirGap (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.air_gap = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetAirGap(self, request, context):
        timestamp = int(time.time()*1000)

        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.air_gap)

    def SetMaxZ1Travel (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.max_z1_travel = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetMaxZ1Travel(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.max_z1_travel)

    def SetLowerCurrentLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.current_limit_lower = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetLowerCurrentLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.current_limit_lower)

    def SetUpperCurrentLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.current_limit_upper = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetUpperCurrentLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.current_limit_upper)

    def SetLowerWOBLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.WOB_limit_lower = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetLowerWOBLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.WOB_limit_lower)

    def SetUpperWOBLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.WOB_limit_upper = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetUpperWOBLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.WOB_limit_upper)

    def SetLowerRPMLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.RPM_limit_lower = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetLowerRPMLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.RPM_limit_lower)

    def SetUpperRPMLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.RPM_limit_upper = request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetUpperRPMLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.RPM_limit_upper)

    def SetZ1ServoTorqueLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.Z1_servo_torque= request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetZ1ServoTorqueLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.Z1_servo_torque)

    def SetZ2ServoTorqueLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.Z2_servo_torque= request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetZ2ServoTorqueLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.Z2_servo_torque)

    def SetXServoTorqueLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.X_servo_torque= request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetXServoTorqueLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.X_servo_torque)

    def SetYServoTorqueLimit (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.Y_servo_torque= request.value
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def GetYServoTorqueLimit(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.LimitResponse(
            request_timestamp = request.request_timestamp,
            value = self.Y_servo_torque)          

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

    def StartHomeY (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.mode != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS) or \
           (self.mission_time_started): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.homeY()
        
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

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def DrillDescendingDrilling(self):
        pass
