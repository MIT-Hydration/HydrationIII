# Performs high velocity control test per discussion on week of 2021-Aug-09
# Prakash Manandhar, Eric Bui, and Roland de Filippi

from ..hardware import HardwareFactory
import time
import numpy as np

# control parameters
Ts = 0.1 # control loop runs every 0.1 second
Pv = 0.01/500
Iv = Pv/20
Pz = 0.1

class ControlSystem:
    def __init__(self, Z1target, WOBtarget, WOBmax):
        self.Pv = Pv
        self.Iv = Iv
        self.Pz = Pz
        self.Z1target = Z1target
        self.WOBtarget = WOBtarget
        self.WOBmax = WOBmax
        self.S = 0.0
        self.Ptol = 0.015 # m
        self.PStopTol = 0.002 # m
        
    def control(self, Z1, WOB):
        if np.abs(WOB) >= WOBmax:
            self.S = self.S/2.0
            return 0.0 # try to stop if we hit WOBmax
        
        WOBerr = self.WOBtarget - WOB
        self.S = self.S + self.Iv*WOBerr
        Perr = self.Z1target - Z1

        if np.abs(Perr) < self.PStopTol:
            return 0.0 # stop if we are within target position tolerance

        if np.abs(Perr) < self.Ptol:
            print("Near destination, stopping")
            V3 = self.Pz*Perr
        else:
            V3 = self.Pv*WOBerr + self.S
            
        return V3 

Z1_THREAD_PITCH = (2.0/1000.0) # == 2 mm 
iZ1 = 0
NUM_RETRIES = 10 # number of times error is cleared in there is a torque limit error
current_retries = 0

def checkAndClearMotorStatus(rig_h):
    motor_status = rig_h.motorStatus()
    if (motor_status[0].find("RMSOverloadShutdown") == -1): # no overload
        current_retries = 0
        return True
    else:
        current_retries = current_retries + 1
        if (current_retries > NUM_RETRIES):
            return False
        rig_h.clearAlert()
        time.sleep(1.0)
        return True

if __name__ == "__main__":
    rig_h = HardwareFactory.getRig()
    wob_h = HardwareFactory.getWOBSensor()
    WOB = wob_h.get_force_N()[1]
    
    # control targets down
    Z1target = 0.001 # m
    #Vmax controlled in CPP code to be VEL_LIM_RPM, 
    # e.g. 600 // (600.0/60.0)*(2.0/1000.0) == 0.02 == 2 cm/sec
    WOBtarget = 100
    WOBmax = 150 # always positive
    Ptol = 0.001 # m

    current_pos = rig_h.getPosition()
    z1 = current_pos[iZ1]
    z1err = Z1target - z1
   
    control_system = ControlSystem(Z1target, WOBtarget, WOBmax)
    time_start = time.time()
    fp = open(f"Vcommand_{time_start}.csv", "w")
    fp.write('UD,time_s,Vcommand_mps,Vcommand_RPM\n')
    
    print(f"WOB = {WOB} N")
    while np.abs(z1err) > Ptol:
        loop_start = time.time()
        WOB = wob_h.get_force_N()[1]
        current_pos = rig_h.getPosition()
        z1 = current_pos[0]
        Vcommand = control_system.control(z1, WOB)
        Vcommand_rpm = (Vcommand*60)/Z1_THREAD_PITCH
        zTorque = rig_h.getTorque(iZ1)
        fp.write(f'D,{loop_start},{Vcommand},{Vcommand_rpm}\n')
        print(f"D {loop_start - time_start:0.3f}s: z={z1:0.3f}m, WB={WOB:0.3f}N,"\
              f" T={zTorque:0.1f}p,"\
              f" Vc={Vcommand:0.5f}m/s, {Vcommand_rpm:0.1f}RPM")
        
        if (not checkAndClearMotorStatus(rig_h)): # try to clear alerts a number of times
            rig_h.set_speed_rpm(iZ1, 0)
            fp.close()
            exit(-1)

        rig_h.set_speed_rpm(iZ1, Vcommand_rpm)

        loop_end = time.time()
        delta_time = loop_end - loop_start
        if (delta_time < Ts):
            time.sleep(Ts - delta_time)
        z1err = Z1target - z1

    rig_h.set_speed_rpm(iZ1, 0)

    print("Reached target, moving up")
    time.sleep(1.0)
    exit(-1)

    # control targets down
    Z1target = 0.01 # m
    #Vmax controlled in CPP code to be VEL_LIM_RPM, 
    # e.g. 600 // (600.0/60.0)*(2.0/1000.0) == 0.02 == 2 cm/sec
    WOBtarget = 100
    WOBmax = 150 # always positive

    current_pos = rig_h.getPosition()
    z1 = current_pos[iZ1]
    z1err = Z1target - z1
   
    control_system = ControlSystem(Z1target, WOBtarget, WOBmax)
    time_start = time.time()
    while np.abs(z1err) > Ptol:
        loop_start = time.time()
        WOB = wob_h.get_force_N()[1]
        current_pos = rig_h.getPosition()
        z1 = current_pos[0]
        Vcommand = control_system.control(z1, WOB)
        Vcommand_rpm = (Vcommand*60)/Z1_THREAD_PITCH
        zTorque = rig_h.getTorque(iZ1)
        fp.write(f'U,{loop_start},{Vcommand},{Vcommand_rpm}\n')
        print(f"U {loop_start - time_start:0.3f}s: z={z1:0.3f}m, WB={WOB:0.3f}N,"\
              f" T={zTorque:0.1f}p,"\
              f" Vc={Vcommand:0.5f}m/s, {Vcommand_rpm:0.1f}RPM")
        
        if (not checkAndClearMotorStatus(rig_h)): # try to clear alerts a number of times
            rig_h.set_speed_rpm(iZ1, 0)
            fp.close()
            exit(-1)

        rig_h.set_speed_rpm(iZ1, Vcommand_rpm)

        loop_end = time.time()
        delta_time = loop_end - loop_start
        if (delta_time < Ts):
            time.sleep(Ts - delta_time)
        z1err = Z1target - z1
    
    rig_h.set_speed_rpm(iZ1, 0)
    fp.close()
