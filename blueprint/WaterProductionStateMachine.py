"""
WaterProductionStateMachine.py
Implements the state machine for the Water Production System.
"""

import threading, time
import configparser
from enum import Enum
from .generated import mission_control_pb2 as mcpb
from .hardware import HardwareFactory

config = configparser.ConfigParser(
    converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config.read('config.ini')

class CleaningStates(Enum):
    STEP_1 = 0
    STEP_2 = 1
    STEP_3 = 2

class WPStateThread(threading.Thread):

    def __init__(self, state_machine):
        threading.Thread.__init__(self)
        self.state_machine = state_machine    

    def _cleaningStep(self):
        current_time = time.time()
        delta_time = self.state_machine.cleaning_step_start_time \
            - current_time
        # get step speed and time and set it in hardware
        speed = self.cleaning_speeds[self.state_machine.cleaning_step]
        timer = self.cleaning_speeds[self.state_machine.cleaning_timers]
        pump = HardwareFactory.getWaterPump()
        pump.set_speed_pom(speed) # TODO respect direction
    
        if (delta_time > timer):
            # next step
            if (self.state_machine.cleaning_step == CleaningStates.STEP_1):
                self.state_machine.cleaning_step == CleaningStates.STEP_2
            if (self.state_machine.cleaning_step == CleaningStates.STEP_1):
                self.state_machine.cleaning_step == CleaningStates.STEP_2
            

    def run(self):
        self.stopped = False
        CONTROL_LOOP_TIME = configparser.getfloat(
            "WaterAssembly", "ControlLoopTime")
        while not self.stopped:
            loop_start = time.time()
            if (self.state_machine.state == mcpb.WPSTATE_MANUAL):
                pass
            elif (self.state_machine.state == mcpb.WPSTATE_CLEANING):
                self._cleaningStep()

            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < CONTROL_LOOP_TIME):
                time.sleep(CONTROL_LOOP_TIME - delta_time)

    def stop(self):
        self.stopped = True

class WaterProductionStateMachine:
    
    # 0 -> turn off
    # 100 -> full power
    def set_heater_level_percent(self, p):
        pass # add code to change heater level here

    def set_pump_level_percent(self, p):
        pass # add code to change pump level here

    def get_all_cleaning_sequences(self):
        pass # returns name and id of all cleaning sequences

    def _loadConfigValuesForCleaning(self, id):
        config_speed_name = f"Cleaning{id}_PumpSpeeds"
        config_timer_name = f"Cleaning{id}_Timers"
        speeds = config.getlist("WaterAssembly", config_speed_name)
        timers = config.getlist("WaterAssembly", config_timer_name)
        speeds = [float(x) for x in speeds]
        timers = [float(x) for x in timers]
        return [speeds, timers]

    def run_cleaning_sequence(self, sequence_id):
        if sequence_id == mcpb.CLEANING_SEQ_1:
            [self.cleaning_speeds, self.cleaning_timers] = \
                self._loadConfigValuesForCleaning(1)
            
        elif sequence_id == mcpb.CLEANING_SEQ_2:
            [self.cleaning_speeds, self.cleaning_timers] = \
                self._loadConfigValuesForCleaning(2)
            
        elif sequence_id == mcpb.CLEANING_SEQ_3:
            
            [self.cleaning_speeds, self.cleaning_timers] = \
                self._loadConfigValuesForCleaning(3)
        else:
            return
        self._state = mcpb.WPSTATE_CLEANING
        self.cleaning_step = CleaningStates.STEP_1
        self.cleaning_step_start_time = time.time()

    def get_state(self):
        return self._state

    def emergency_stop(self):
        self._state = mcpb.WPSTATE_MANUAL
        self.set_heater_level_percent(0)
        self.set_pump_level_percent(0)

    def __init__(self):
        super().__init__()
        self._state = mcpb.WPSTATE_MANUAL
        self.set_heater_level_percent(0)
        self.set_pump_level_percent(0)

