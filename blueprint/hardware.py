"""
hardware.py
Hardware Interface and Mock Layers for Hydration project.
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

from abc import ABC, abstractmethod
import time

class HardwareFactory:
    
    is_mock = {
        "drill": True
    }

    mock_load_profile_simple = {
        "drill_ramp_delay_ms": 10,
        "drill_ramp_slope_rpm_per_ms": 10 
    }

    current_load_profile = mock_load_profile_simple

    @classmethod
    def getDrill(cls):
        if (cls.is_mock["drill"]):
            return MockDrill()
        else:
            return Drill()
    

class AbstractDrill(ABC):
    
    @abstractmethod
    def set_drill_level(self, level):
        pass

    @abstractmethod
    def get_drill_level(self, level):
        pass

    @abstractmethod
    def get_rotation_rpm(self):
        pass

    @abstractmethod
    def get_active_power_W(self):
        pass

    @abstractmethod
    def get_total_current_mA(self):
        pass


class MockDrill(AbstractDrill):
    
    def __init__(self):
        self._set_time = time.time()
        self._current_level = 0.0
        self._set_level = 0.0

    def set_drill_level(self, level):
        self._set_time = time.time()
        self._set_level = level
    
    def get_drill_level(self):
        ramp = 


class Drill(AbstractDrill):
    def __init__(self):
        pass
