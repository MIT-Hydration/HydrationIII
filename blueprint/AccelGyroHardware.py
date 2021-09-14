"""
AccelGyroHardware.py
Interface to MPU6050 IMU. 
Adapted from: https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
"""

__author__      = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Hydration Team"
__credits__ = ["Prakash Manandhar"]
__license__ = "Internal"
__version__ = "1.0.0"
__maintainer__ = "Prakash Manandhar"
__email__ = "engineer.manandhar@gmail.com"
__status__ = "Production"

import time
import numpy
import smbus			#import SMBus module of I2C

import threading
import configparser

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

config = configparser.ConfigParser()
config.read('config.ini')

class AccelGyroThread(threading.Thread):
    
    def _MPU_Init(self):
        self.bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
        Device_Address = 0x68   # MPU6050 device address

        #write to sample rate register
        self.bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
        
        #Write to power management register
        self.bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
        
        #Write to Configuration register
        self.bus.write_byte_data(Device_Address, CONFIG, 0)
        
        #Write to Gyro configuration register
        self.bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        
        #Write to interrupt enable register
        self.bus.write_byte_data(Device_Address, INT_ENABLE, 1)
    
    def __init__(self):  
        self.sampling_time = config.getfloat('AccelGyro', 'SamplingTime')
        self._MPU_Init()
        self.sensor_readings = {
            "time_s": 0.0,
            "Gx_deg_p_sec": 0.0, 
            "Gy_deg_p_sec": 0.0, 
            "Gz_deg_p_sec": 0.0, 
            "Ax_g": 0.0, 
            "Ay_g": 0.0, 
            "Az_g": 0.0,  
        }

        threading.Thread.__init__(self)
        self.stopped = True

    def _read_raw_data(self, addr):
	    #Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(Device_Address, addr)
        low = self.bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

    def run(self):
        self.stopped = False
        
        while not self.stopped:
            loop_start = time.time()
            
            #Read Accelerometer raw value
            acc_x = self._read_raw_data(ACCEL_XOUT_H)
            acc_y = self._read_raw_data(ACCEL_YOUT_H)
            acc_z = self._read_raw_data(ACCEL_ZOUT_H)
            
            #Read Gyroscope raw value
            gyro_x = self._read_raw_data(GYRO_XOUT_H)
            gyro_y = self._read_raw_data(GYRO_YOUT_H)
            gyro_z = self._read_raw_data(GYRO_ZOUT_H)
            
            #Full scale range +/- 250 degree/C as per sensitivity scale factor
            Ax = acc_x/16384.0
            Ay = acc_y/16384.0
            Az = acc_z/16384.0
            
            Gx = gyro_x/131.0
            Gy = gyro_y/131.0
            Gz = gyro_z/131.0
            
            self.sensor_readings["Gx_deg_p_sec"] = Gx 
            self.sensor_readings["Gy_deg_p_sec"] = Gy
            self.sensor_readings["Gz_deg_p_sec"] = Gz
            self.sensor_readings["Ax_g"] = Ax 
            self.sensor_readings["Ay_g"] = Ay
            self.sensor_readings["Az_g"] = Az
            
            loop_end = time.time()
            self.sensor_readings["time_s"] = loop_start
            delta_time = loop_end - loop_start
            if (delta_time < self.sampling_time):
                time.sleep(self.sampling_time - delta_time)

    def stop(self):
        self.stopped = True

        
class FileWriterThread(threading.Thread): 
    def __init__(self, sensor_thread):
        threading.Thread.__init__(self)
        self.sensor_thread = sensor_thread
        self.stopped = True
        
    def run(self):
        self.stopped = False
        time_start_s = time.time()
        fp = open(f"AccelGyro_{time_start_s}.csv", "w")
        keys = self.sensor_thread.sensor_readings.keys()
        for k in keys:
            fp.write(f"{k},")
        fp.write("\n")
        sampling_time = config.getfloat("AccelGyro", "SamplingTime")
        
        while not self.stopped:
            loop_start = time.time()
            for k in keys:
                fp.write(f"{self.sensor_thread.sensor_readings[k]},")
            fp.write("\n")
            loop_end = time.time()
            delta_time = loop_end - loop_start
            if (delta_time < sampling_time):
                time.sleep(sampling_time - delta_time)
        
        fp.close()
        
    def stop(self):
        self.stopped = True


class AccelGyro:   
    def __init__(self):
        self.sensor_thread = AccelGyroThread()
        self.file_writer_thread = FileWriterThread(self.sensor_thread)
        self.sensor_thread.start()
        self.file_writer_thread.start()

    def get_sensor_readings(self):
        return self.sensor_thread.sensor_readings
