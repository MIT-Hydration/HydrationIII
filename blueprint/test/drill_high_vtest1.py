# Performs high velocity control test per discussion on week of 2021-Aug-09
# Prakash Manandhar, Eric Bui, and Roland de Filippi

from ..hardware import HardwareFactory
import time
import numpy as np

# control parameters
Ts = 0.1 # control loop runs every 0.1 second
Pv = 0.03/500
Iv = Pv/10
Pz = 0.03

class ControlSystem:
    def __init__(self, Z1target, Vtarget, WOBtarget, WOBmax):
        self.Pv = Pv
        self.Iv = Iv
        self.Pz = Pz
        self.Z1target = Z1target
        self.Vtarget = Vtarget
        self.WOBtarget = WOBtarget
        self.WOBmax = WOBmax
        self.S = 0.0
        self.Ptol = 0.010 # m
        
    def control(self, Z1, WOB):
        if np.abs(WOB) >= WOBmax:
            return 0.0 # try to stop if we hit WOBmax
        
        WOBerr = self.WOBtarget - WOB
        self.S = self.S + self.Iv*WOBerr
        Perr = self.Z1target - Z1
        
        if np.abs(Perr) < self.Ptol:
            V3 = self.Pz*Perr
        else:
            V3 = self.Pv*WOBerr + self.S
            
        return V3   

# control targets
Z1target = -0.7 # m
Vtarget = -0.01 # m/s
#Vmax controlled in CPP code to be VEL_LIM_RPM, 
# e.g. 600 // (600.0/60.0)*(2.0/1000.0) == 0.02 == 2 cm/sec
WOBtarget = -100
WOBmax = 150 # always positive

Ptol = 0.002 # m, position tolerance for stop

Z1_THREAD_PITCH = (2.0/1000.0) # == 2 mm 
iZ1 = 0
NUM_RETRIES = 10 # number of times error is cleared in there is a torque limit error
current_retries = 0

def checkAndClearMotorStatus(rig_h):
    motor_status = rig_h.motorStatus()
    if (motor_status[0].find("RMSOverloadShutdown")): # no overload
        current_retries = 0
        return True
    else:
        current_retries = current_retries + 1
        if (current_retries > NUM_RETRIES):
            return False
        rig_h.clearAlert()
        return True

if __name__ == "__main__":
    rig_h = HardwareFactory.getRig()
    wob_h = HardwareFactory.getWOBSensor()
    
    current_pos = rig.getPosition()
    z1 = current_pos[0]
    z1err = Z1target - z1
   
    control_system = ControlSystem(Z1target, Vtarget, WOBtarget, WOBmax)
    fp = open(f"Vcommand_{time.time()}.csv", "w")
    fp.write('time_s,Vcommand_mps,Vcommand_RPM\n')
    while np.abs(z1err) < Ptol:
        loop_start = time.time()
        WOB = wob_h.get_force_N()
        current_pos = rig_h.getPosition()
        z1 = current_pos[0]
        Vcommand = control_system.control(z1, WOB)
        Vcommand_rpm = (Vcommand*60)/Z1_THREAD_PITCH
        fp.write(f'{loop_start},{Vcommand},{Vcommand_rpm}\n')
        
        if (not checkAndClearMotorStatus(rig_h)): # try to clear alerts a number of times
            break
        rig_h.set_speed_rpm(iZ1, Vcommand_rpm)

        loop_end = time.time()
        delta_time = loop_end - loop_start
        if (delta_time < Ts):
            time.sleep(Ts - delta_time)

    rig_h.set_speed_rpm(iZ1, 0)