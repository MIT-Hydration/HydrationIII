"""
WaterProductionStateMachine.py
Implements the state machine for the Water Production System.
"""

import threading
import configparser
from enum import Enum
from .generated import mission_control_pb2 as mcpb

config = configparser.ConfigParser()
config.read('config.ini')

class WPStateThread(threading.Thread):

    def __init__(self, state_machine):
        threading.Thread.__init__(self)
        self.state_machine = state_machine    

    def run(self):


class WaterProductionStateMachine:
    
    # 0 -> turn off
    # 100 -> full power
    def set_heater_level_percent(self, p):
        pass # add code to change heater level here

    def set_pump_level_percent(self, p):
        pass # add code to change pump level here

    def get_all_cleaning_sequences(self):
        pass # returns name and id of all cleaning sequences

    def run_cleaning_sequence(self, sequence_id):
        pass   

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

