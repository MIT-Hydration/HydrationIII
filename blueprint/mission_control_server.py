from .generated import mission_control_pb2_grpc
from .generated import mission_control_pb2 as mcpb
from .hardware import HardwareFactory

import time
import configparser
import blueprint

config = configparser.ConfigParser()
config.read('config.ini')

class StateMachine:
    
    def __init__(self):
        self.major_mode = mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS
        self.state = mcpb.STARTUP_IDLE

        self.start_up_states = {
            mcpb.STARTUP_IDLE: mcpb.STARTUP_MISSION_CLOCK_STARTED,
            mcpb.STARTUP_MISSION_CLOCK_STARTED: mcpb.STARTUP_HOMING_Z1,
            mcpb.STARTUP_HOMING_Z1: mcpb.STARTUP_HOME_Z1_COMPLETED,
            mcpb.STARTUP_HOME_Z1_COMPLETED: mcpb.STARTUP_HOMING_Y,
            mcpb.STARTUP_HOMING_Y: mcpb.STARTUP_HOME_Y_COMPLETED
        }

        self.drill_states = {
            mcpb.DRILL_IDLE: [mcpb.DRILL_MOVING_Y, mcpb.DRILLING_HOLE_IDLE],
            mcpb.DRILL_MOVING_Y: [mcpb.DRILL_IDLE],
            mcpb.DRILLING_HOLE_IDLE: [mcpb.DRILL_IDLE],
            mcpb.DRILLING_HOLE_DRILLING_DOWN: [mcpb.DRILL_IDLE],
            mcpb.DRILLING_HOLE_REAMING_UP: [mcpb.DRILL_IDLE],
            mcpb.DRILLING_HOLE_HOMING_Z1: [mcpb.DRILL_IDLE],
        }


    def getMajorMode(self):
        return self.major_mode
    
    def getState(self):
        return self.state
    
    def getAllowedStateTransitions(self):
        next_mode = [mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS]
        next_state = [mcpb.STARTUP_IDLE]
        if self.major_mode == mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS:
            if self.state != mcpb.STARTUP_HOME_Y_COMPLETED:
                next_mode.append(mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS)
                next_state.append(self.start_up_states[self.state])
            else:
                next_mode.append(mcpb.MAJOR_MODE_DRILL_BOREHOLE)
                next_state.append(mcpb.DRILL_IDLE)
        if self.major_mode == mcpb.MAJOR_MODE_DRILL_BOREHOLE:
            next_mode.append(mcpb.MAJOR_MODE_DRILL_BOREHOLE)
            for k in self.drill_states[self.state]:
                next_state.append(k)

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
        self.holes = []
        self.last_y_move = 0

        self.iZ1 = 0
        self.iZ2 = 1
        self.iX = 2
        self.iY = 3

        
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

        current_state = self.state_machine.getState()
        if (current_state == mcpb.STARTUP_HOMING_Z1):
            if rig_hardware.isHomeZ1():
                self.state_machine.transitionState(
                    mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS, 
                    mcpb.STARTUP_HOME_Z1_COMPLETED
                )

        if (current_state == mcpb.STARTUP_HOMING_Y):
            if rig_hardware.isHomeY():
                self.state_machine.transitionState(
                    mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS, 
                    mcpb.STARTUP_HOME_Y_COMPLETED
                )

        if (current_state == mcpb.DRILL_MOVING_Y):
            move_time_buffer = config.getint("Rig", "MoveTimeBuffer")
            if ((timestamp - self.last_y_move) > move_time_buffer) and \
                (not rig_hardware.isYMoving()):
                self.state_machine.transitionState(
                    mcpb.MAJOR_MODE_DRILL_BOREHOLE, 
                    mcpb.DRILL_IDLE
                )

        position = rig_hardware.getPosition()
        return mcpb.HeartBeatReply(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            cpu_temperature_degC = cpu_temp,
            mission_time_ms = mission_time,
            zdrill_servo_moving = rig_hardware.isZ1Moving(),
            y_servo_moving = rig_hardware.isYMoving(),
            rig_zdrill = position[self.iZ1],
            rig_y = position[self.iY],
            major_mode = self.state_machine.getMajorMode(),
            state = self.state_machine.getState(),
            server_version = blueprint.HYDRATION_VERSION,
            holes = self.holes)

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

    def Z1Move(self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState() != mcpb.STARTUP_IDLE): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        move_success = rig_hardware.movePositionZ1(request.delta)

        if move_success:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTED)
        else:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTION_ERROR)
            
    def YMove(self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState() != mcpb.STARTUP_IDLE) and \
            (self.state_machine.getState() != mcpb.DRILL_IDLE): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)

        rig_hardware = HardwareFactory.getRig()
        move_success = rig_hardware.movePositionY(request.delta)

        if (self.state_machine.getState() == mcpb.DRILL_IDLE): 
            self.state_machine.transitionState(
                mcpb.MAJOR_MODE_DRILL_BOREHOLE, mcpb.DRILL_MOVING_Y)

        if move_success:
            self.last_y_move = timestamp
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTED)
        else:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTION_ERROR)

    def StartDrillHole(self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState() != mcpb.DRILL_IDLE): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)
        
        self.state_machine.transitionState(
                mcpb.MAJOR_MODE_DRILL_BOREHOLE, mcpb.DRILLING_HOLE_IDLE)

        if self.state_machine.getState() == mcpb.DRILLING_HOLE_IDLE:
            self._create_new_hole()
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTED)
        else:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTION_ERROR)

    def _create_new_hole(self):
        rig_hardware = HardwareFactory.getRig()
        position = rig_hardware.getPosition()
        hole = mcpb.Hole(
            order = len(self.holes) + 1,
            x_m = position[self.iX],
            y_m = position[self.iY],
            max_z_m = 0.0,
            water_ml = 0.0,
            diameter_m = 0.03
        )
        self.holes.append(hole)

    def StartupNext (self, request, context):
        timestamp = int(time.time()*1000)
        if (self.state_machine.getMajorMode() != mcpb.MAJOR_MODE_STARTUP_DIAGNOSTICS): # do nothing
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)
        state = self.state_machine.getState()
        if (state == mcpb.STARTUP_IDLE):
            return self._startMissionClock(request, context)
        elif (state == mcpb.STARTUP_MISSION_CLOCK_STARTED):
            return self._StartHomeZ1(request, context)
        elif (state == mcpb.STARTUP_HOME_Z1_COMPLETED):
            return self._StartHomeY(request, context)
        
        else:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)
        
        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def _startMissionClock (self, request, context):
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
            mcpb.STARTUP_MISSION_CLOCK_STARTED
        )

        return mcpb.CommandResponse(
            request_timestamp = request.request_timestamp,
            timestamp = timestamp,
            status = mcpb.EXECUTED)

    def SetHomeZ1 (self, request, context):
        print("Setting Home Z1 ...")
        timestamp = int(time.time()*1000)
        if (self.state_machine.getState() != mcpb.STARTUP_IDLE): # do nothing
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
        if (self.state_machine.getState() != mcpb.STARTUP_IDLE): # do nothing
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

    def _StartHomeZ1 (self, request, context):
        timestamp = int(time.time()*1000)
        if self.state_machine.getState() \
                != mcpb.STARTUP_MISSION_CLOCK_STARTED: # do nothing
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
        
    def _StartHomeY (self, request, context):
        print("Homing Y...")
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

    def GotoMajorMode(self, request, context):
        timestamp = int(time.time()*1000)
        if request.new_mode == mcpb.MAJOR_MODE_DRILL_BOREHOLE:
            self.state_machine.transitionState(
                mcpb.MAJOR_MODE_DRILL_BOREHOLE,
                mcpb.DRILL_IDLE
            )
        if self.state_machine.getMajorMode() == request.new_mode:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.EXECUTED)
        else:
            return mcpb.CommandResponse(
                request_timestamp = request.request_timestamp,
                timestamp = timestamp,
                status = mcpb.INVALID_STATE)