"""
z1Control.py
Handles z1 drill assembly control system for Hydration project.
"""

__author__      = "Tao Sevigny, Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Tao Sevigny"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Tao Sevigny"
__email__ = "sevignyt@gmail.com"
__status__ = "Production"

#imports
import numpy as np
import time
import hardware
#import interpreter as inter
#import servos reading code as servo


#functions

#create a reference path
def make_ref_path(z_desired, z_current, mode, time_start):
    ref_path = []
    #mode determine rate 0=aggresive, 1=normal, 2=slow, 3=snail
    if mode == 0:
        rate = -3
    elif mode == 1:
        rate = -2
    elif mode == 2:
        rate = -1
    elif mode == 3:
        rate = -.5
    #return error if mode invalid
    else:
        return ("error")
    #determine number of steps with equation: steps = (z_end-z_start)/rate*10 steps per second
    steps = (z_current-z_desired)/rate*10 + 10
    #for each step, determine z position for that time
    for i in range(steps):
        t = i*.1 #seconds
        z = rate*t
        #add z and time to reference path list
        #if z if less than the z desired, than just add z_desired
        if z < z_desired:
            ref_path.append([z_desired,t+time_start])
        else:
            ref_path.append([z,t+time_start])
    return ref_path


def PID(Kp, Ki, Kd, t_0, Value_bar=0):
    e_prev = 0
    t_prev = t_0
    I = 0
    while True:
        t, Current_Value, Set_Value = yield Value

        #PID calculations
        #error in speed = error in position/expected time elapsed (.1s)
        e = (Set_Value - Current_Value)/.1

        P = Kp*e
        I = I + Ki*e*(t - t_prev)
        D = Kd*(e - e_prev)/(t-t_prev)

        Value = Value_bar + P + I + D

        e_prev = e
        t_prev = t


#unchanged variables
'''
for assigning unchanged variables use tuples
ex: g = (9.81, m/s^2)
g[0] is value, g[1] is units
'''
weight_on_bit_limit = 145 #[N]

#lead on lead screw
Lead = .002 #[m/rev].002m/rev or 2mm/rev

#pre-defined base speeds (Proportional control constant)
agg_base = 14 #[rev/s] rotational velocity of the motor
base = 10 #[rev/s] rotational velocity of the motor
slow_base = 5 #[rev/s] rotational velocity of the motor
snail_base = 2 #[rev/s] rotational velocity of the motor
up = -10 #[rev/s] rotational velocity of the motor
stop = 0
Kp = [14, 10, 5, 2]


#Integral and Deriviative control constants
Ki = 1
Kd = 1

#body

class DrillController:
    def __init__(self):
        #drill = hardware.Drill()
        #zServo = inter.ZServo()
    def Drill_Standby():

    def Drill_Calibrating():
        #calibrate sequence NOTE need to decide whether this controller or
        #the transition program btwn pthn and c will give sequence to servo
    def Drill_Calibration_Error():
        # return Error

    def Drill_Ascending_On(end_pos):
        #Drill turns on
        drill.run()
                
        #Drill assembly raises until at desired postion
        while end_pos > actual_pos
            
            #send conmand to servo for speed to go up
            zServo.speed = up
            
            #obtain sensors inputs
            #actual pos from servo output
            #limit_switch from limit switch (0=no,1=yes)
            #off from BIG RED BUTTON from central control (0=no,1=yes)
            if off == 1:
                servo_speed = stop
                break
            elif limit_switch == 1:
                servo_speed = stop
                actual_pos = 0 #if limit switch is hit, then the rig is at the 
                                #top
                break
        #Turn drill off
        servo_speed = stop
        drill.stop()

    def Drill_Ascending_off(end_pos):
        while end_pos > actual_pos
            
            #send conmand to servo for speed to go up
            servo_speed = up
            
            #obtain sensors inputs
            servo_data = hardware.servo_read

            #actual pos from servo output
            #limit_switch from limit switch (0=no,1=yes)
            #off from BIG RED BUTTON from central control


            if BigRedButton == on:
                servo_speed = stop
                break
            elif limit_switch == 1:
                servo_speed = stop
                actual_pos = 0 #if limit switch is hit, then the rig is at the 
                                #top
                break
        servo_speed = stop
        #return to standby

    def Drill_Descending_Drilling(end_pos):
        #Drill turns on
        drill.run()
        #sends command to central control to turn the drill on
        
        #read input from mission command/user to obtain desired_pos
        
        # start timer
        t_0 = time.time()
        
        #creates intial reference path using servo speed and length of travel
        ref_path = create_ref_path(desired_pos, actual_pos, 0, t_0)
        
        WOB_mode = 0
        step = 0
        controller = PID(agg_base, Ki, Kd, t_0)
        controller.send(None)

        #Drill assembly descends until at desired postion
        while (end_pos + .001) < actual_pos
            
            #obtain sensors inputs
            #actual pos from servo output
            #off from BIG RED BUTTON from central control (0=no,1=yes)
            #weight_on_bit from load cell
            if BigRedButton == off or weight_on_bit >= weight_on_bit_limit:
                servo.stop()
                break
            #set time
            t = time.time()
            
            
            #Adjusts behavior if neccessary based on WOB

            #if more than 140, stop z-axis movement and run troubleshoot automatically
            if WOB >= 140: [N]
                #stop servo
                servo_speed = stop
                #continue running drill for 5 seconds
                time.sleep(5)
                #attempt to move w/o exceeding WOB 3 times
                attempt=0
                while attempt < 3:
                    #pull servo out a little bit
                    servo_speed = up
                    time.sleep(.5)
                    servo_speed = stop
                    #refresh WOB
                    '''call WOB from loadcell'''
                    t_s=time.time()
                    servo_speed = 1 #rev/sec
                    passed = True
                    while (t-t_s) < 5:
                        '''call WOB from loadcell'''
                        if WOB>140:
                            servo_speed = stop
                            passed = False
                            break
                            
                    if passed == True:
                        break
                    else:
                        attempt += 1
                
                                
                #if failed, request continue or stop from user/mission control
                #if pass, remake reference path using snail rate and continue
                if passed == True:
                    WOB_mode = 3
                    t=time.time()
                    ref_path = create_ref_path(desired_pos, actual_pos, WOB_mode, round(t, 1)
                    step = 0
                else:
                    #send error to mision control
                    #return weight on bit limit exceeded Error
                    break

            # use WOB input to determine if speed mode needs to be changed, if the mode was changed, a new reference path is created        
            else:
                # normal rate of decent
                if WOB >= 100 and < 120
                    WOB_mode_new = 1
                # slow rat eof decent
                elif WOB >= 120 and < 130
                    WOB_mode_new = 2
                # snail rate of decent
                elif WOB >= 130 and < 140
                    WOB_mode_new = 3
                # aggressive rate of decent
                else:
                    WOB_mode_new = 0
                if WOB_mode != WOB_mode_new
                    WOB_mode = WOB_mode_new
                    #create new reference path
                    ref_path = create_ref_path(desired_pos, actual_pos, WOB_mode, round(t, 1)
                    step = 0
                    controller = PID(Kp[WOB_mode], Ki, Kd, t)
                    controller.send(None)
                    
            #pull reference position from the reference path
            ref_pos = ref_path[step]
            
            #send command to servo for speed to go down, pace determined by 
            #difference between actual position and reference position
            

            '''actual_pos = call from servo'''

            servo_speed = controller.send([t, actual_pos, ref_pos])
            '''drill.speed = servo_speed need to update with final hardware code'''

            step =+ 1
            #check if .1s has passed, if not, wait for .1 sec to finish to maintain max 10Hz freq
            t_elapsed = time.time() - t
            if t_elapsed < .1
                time.sleep(.1-t_elapsed)
            
        #drill assembly has reached desired height or while loop was broken  
          
        #Turn drill off
        servo_speed = stop
        drill.stop()
        #return to standby
        


    def Drill_Descending_Off(end_pos):
        #Drill assembly raises until at desired postion
        while end_pos < actual_pos
            
            #send conmand to servo for speed to go down
            servo_speed = base
            
            #obtain sensors inputs
            #actual pos from servo output
            #off from BIG RED BUTTON from central control (0=no,1=yes)
            if BigRedButton == on:
                servo_speed = stop
                break
            

        #return to standby
        servo_speed = stop



            





















'''
from abc import ABC, abstractmethod
import time
import threading

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder

from gpiozero import PWMLED
from gpiozero import CPUTemperature

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
    def start_sensor_readings(cls):
        pass

    @abstractmethod
    def start_sensor_readings(cls):
        pass
    
    @abstractmethod
    def set_drill_level(self, level):
        pass

    @abstractmethod
    def get_drill_level(self, level):
        pass

    @abstractmethod
    def get_speed_rpm(self):
        pass

    @abstractmethod
    def get_active_power_W(self):
        pass

    @abstractmethod
    def get_current_mA(self):
        pass


class MockDrill(AbstractDrill):
    
    def __init__(self):
        self._set_time = time.time()
        self._current_level = 0.0
        self._set_level = 0.0

    def set_drill_level(self, level):
        self._set_time = time.time()
        self._set_level = level
    
class Drill(AbstractDrill):

    class DrillThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = True
            self.sensor_readings = {
                    "active_power_W": 0.0,
                    "current_mA": 0.0,
                    "speed_rpm": 0.0,
                    "accel_x_g": 0.0,
                    "accel_y_g": 0.0,
                    "accel_z_g": 0.0,
                }
            self.client = ModbusSerialClient(port='/dev/ttyUSB0', method='rtu', baudrate=9600)

        def run(self):
            self.stopped = False
            while not self.stopped:
                loop_start = time.time()
                result  = self.client.read_holding_registers(address, count,  unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, 
                    wordorder = '>', byteorder = '>')
                current_mA = decoder.decode_32bit_float()
                power_W = decoder.decode_32bit_float()
                self.sensor_readings["active_power_W"] = power_W
                self.sensor_readings["current_mA"] =  current_mA
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.01):
                    time.sleep(0.01 - delta_time)
                
        def stop(self):
            self.stopped = True

    class FileWriterThread(threading.Thread):

        def __init__(self, drill_thread):
            threading.Thread.__init__(self)
            self.drill_thread = drill_thread
            self.stopped = True
            
        def run(self):
            self.stopped = False
            fp = open(f"{time_start_s}.csv", "w")
            fp.write("time_s,")
            keys = drill_thread.sensor_readings.keys
            for k in keys:
                fp.write(f"{k},")
            fp.write("\n")
            while not self.stopped:
                loop_start = time.time()
                fp.write(f"{loop_start},")
                for k in keys:
                    fp.write(f"{drill_thread.sensor_readings[k]},")
                fp.write("\n")
                loop_end = time.time()
                delta_time = loop_end - loop_start
                if (delta_time < 0.02):
                    time.sleep(0.02 - delta_time)

            fp.close()
                
        def stop(self):
            self.stopped = True
            
    modbus_reg_address = 75
    modbus_reg_count   = 4
    motor = PWMLED(12)
    drill_thread = DrillThread()
    writer_thread = FileWriterThread(drill_thread)
    
    @classmethod
    def start_sensor_readings(cls):
        cls.drill_thred.start()
        cls.writer_thread.start()

    @classmethod
    def stop_sensor_readings(cls):
        cls.drill_thread.stop()
        cls.writer_thread.stop()

    @classmethod
    def set_drill_level(cls, level):
        cls.motor.value = level

    @classmethod
    def get_drill_level(cls, level):
        return cls.motor.value

    @classmethod
    def get_speed_rpm(cls):
        return cls.drill_thread.sensor_readings["speed_rpm"]
        pass

    @classmethod
    def get_active_power_W(cls):
        return cls.drill_thread.sensor_readings["active_power_W"]
    
    @classmethod
    def get_current_mA(cls):
        return cls.drill_thread.sensor_reading["current_mA"]
'''