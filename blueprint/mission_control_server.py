from .generated import mission_control_pb2_grpc
from .generated import mission_control_pb2 as mcpb
from .hardware import HardwareFactory

import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class StateMachine:
    
    def __init__(self):
        self.major_mode = mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS
        self.state = mcpb.STARTUP_IDLE

        self.start_up_states = {
            mcpb.STARTUP_IDLE: mcpb.STARTUP_START_MISSION_CLOCK_COMPLETED,
            mcpb.STARTUP_START_MISSION_CLOCK_COMPLETED, mcpb.STARTUP_HOMING_Z1,
            mcpb.STARTUP_HOMING_Z1: mcpb.STARTUP_HOME_Z1_COMPLETED,
            mcpb.STARTUP_HOME_Z1_COMPLETED: mcpb.STARTUP_HOMING_Y,
            mcpb.STARTUP_HOMING_Y: mcpb.STARTUP_HOME_Y_COMPLETD
        }

    def getMajorMode(self):
        return self.major_mode
    
    def getState(self):
        return self.state
    
    def getAllowedStateTransitions(self):
        next_mode = mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS
        next_state = mcpb.STARTUP_IDLE
        if self.major_mode == mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS:
            if self.state != mcpb.STARTUP_HOME_Y_COMPLETD:
                next_mode.append(mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS)
                next_state.append = self.start_up_states[self.state]
            else:
                next_mode.append(mcpb.MAJOR_MODE_DRILL_BOREHOLE)
                next_state.append(mcpb.DRILL_IDLE)

        return [next_mode, next_state]

    def transitionState(self, new_mode, new_state):
        allowed = self.getAllowedStateTransitions()
        if (new_mode in allowed[0]) and (new_state in allowed[1]):
            self.major_mode = new_mode
            self.state = new_state
            return True
        return False

class MissionController(mission_control_pb2_grpc.MissionControlServicer):
    
    def __init__(self):
        self.air_gap = 0.05
        self.max_z1  = 0.85
        self.ice_depth = 0.3
        self.state_machine = StateMachine()
        self.mission_time_started = False
        self.mission_start_time = -1
        
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

    def HeartBeat(self, request, context):
        timestamp = int(time.time()*1000)
        cpu_temp = HardwareFactory.getMissionControlRPi() \
            .get_cpu_temperature()

        rig_hardware = HardwareFactory.getRig()

        if (self.mission_time_started):
            mission_time = timestamp - self.mission_time
        else:
            mission_time = 0

        if (self.state_machine.getState() == mcpb.STARTUP_HOMING_Z1):
            if rig_hardware.isHomeZ1():
                self.state_machine.transitionState(
                    mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS, 
                    mcpb.STARTUP_HOME_Z1_COMPLETED
                )

        if (self.state_machine.getState() == mcpb.STARTUP_HOMING_Y):
            if rig_hardware.isHomeY():
                self.state_machine.transitionState(
                    mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS, 
                    mcpb.STARTUP_HOME_Y_COMPLETED
                )

        return mcpb.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            cpu_temperature_degC = cpu_temp,
            mission_time_ms = mission_time,
            zdrill_servo_moving = rig_hardware.isZ1Moving(),
            y_servo_moving = rig_hardware.isYMoving(),
            rig_zdrill = rig_hardware.getPosition()[0],
            rig_y = rig_hardware.getPosition()[3],
            major_mode = self.state_machine.getMajorMode(),
            state = self.state_machine.getState())

    def GetLimits(self, request, context):
        timestamp = int(time.time()*1000)
        
        return mcpb.Limits(
            request_timestamp = request.request_timestamp,
            air_gap = self.air_gap,
            max_z1  = self.max_z1,
            ice_depth = self.ice_depth
            )

    def SetLimits(self, request, context):
        timestamp = int(time.time()*1000)

        # don't let change max_z1 unless we are in ide state
        if self.max_z1 != request.max_z1:
            if self.state_machine.getState() != mcpb.STARTUP_IDLE:
                return mcpb.CommandResponse(
                    request_timestamp = request.request_timestamp,
                    timestamp = timestamp,
                    status = mcpb.INVALID_STATE)

        self.air_gap = request.air_gap
        self.max_z1 = request.max_z1
        self.ice_depth = request.ice_depth    

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

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
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState() != mcpb.STARTUP_IDLE): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.movePositionZ1(request.delta)

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)
        
    def StartMissionClock (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState() != mcpb.STARTUP_IDLE): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        self.mission_time = timestamp
        self.mission_time_started = True
        self.state_machine.transitionState(
            mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS,
            mcpb.STARTUP_START_MISSION_CLOCK_COMPLETED
        )

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetHomeZ1 (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState != mcpb.STARTUP_IDLE): # do nothing
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

    def SetHomeY (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState != mcpb.STARTUP_IDLE): # do nothing
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

    def StartHomeZ1 (self, request, context):
        timestamp = int(time.time()*1000)
        if self.state_machine.getState() \
                != mcpb.STARTUP_START_MISSION_CLOCK_COMPLETED: # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)
        self.state_machine.transitionState(
            mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS, mcpb.STARTUP_HOMING_Z1)
        rig_hardware = HardwareFactory.getRig()
        rig_hardware.homeZ1()
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)
        
    def StartHomeY (self, request, context):
        timestamp = int(time.time()*1000)
        if self.state_machine.getState() \
                != mcpb.STARTUP_HOME_Z1_COMPLETED: # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)
        self.state_machine.transitionState(
            mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS, mcpb.STARTUP_HOMING_Y)
        rig_hardware = HardwareFactory.getRig()
        rig_hardware.homeY()
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def EmergencyStop(self, request, context):
        timestamp = int(time.time()*1000)

        rig_hardware = HardwareFactory.getRig()
        rig_hardware.emergencyStop()
        
        self.state_machine.transitionState(
            mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS,
            mcpb.STARTUP_IDLE
        )

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    