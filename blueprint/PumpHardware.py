# library for the arrays
import numpy as np
from numpy import amax

# for the FFT
from scipy.fft import fft, ifft, fftshift

from time import sleep  # this lets us have a time delay
import time
from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html

if config.getboolean('Operating System', 'RunningInRPi'):
    from gpiozero import PWMLED
    import RPi.GPIO as GPIO

PUL = 13  # Stepper Drive Pulses to GPIO 13 (PWM-1)
# Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
DIR = 27
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
#SIG = 26  # Pin receiving the Hall Effect signal

#GPIO.setmode(GPIO.BCM)

#GPIO.setup(PUL, GPIO.OUT)
#GPIO.setup(DIR, GPIO.OUT)
#GPIO.setup(ENA, GPIO.OUT)
#GPIO.setup(SIG, GPIO.IN)

class PumpMode:
    MANUAL = 0  # manually set speed, direction, cleaning sequence, stop
    AUTOMATIC = 1  # run continuously, clean if required, stop

    # when starting manual mode from automatic, always start from 0 speed (stop)
    # emergency stop is always possible, and returns to manual mode


class AbstractPump(ABC):

    # @abstractmethod
    # def emergency_stop(self):
    #     pass

    # @abstractmethod
    # def get_flow_mlps(self):
    #     pass

    # DIRECTIONS:
    @abstractmethod
    def set_direction(self, direction):
        pass

    @abstractmethod
    def get_direction(self):
        pass

    # SPEED (Milli-liter per seconds):
    @abstractmethod
    def set_speed_mlps(self, speedmlps_value):
        pass

    @abstractmethod
    def get_speed_mlps(self):
        pass

    # @abstractmethod
    # def get_mode(self):
    #     pass
    #
    # @abstractmethod
    # def set_mode(self, mode):
    #     pass

    # FILTER CLEANING SEQUENCE:
    @abstractmethod
    def cleaning_sequence(self):
        pass

    # MAXSPEED (Percentage of the Max):
    @abstractmethod
    def get_max_speed(self):
        pass

    @abstractmethod
    def set_speed_pom(self, speedpom_value):
        pass

    @abstractmethod
    def get_speed_pom(self):
        pass


class MockPump(AbstractPump):
    duration = 400
    delay = 0.0000001

    def __init__(self):
        self.speedmlps = 0
        self.speedpom = 0
        self.direction = 0

    @staticmethod
    def run_pump():
        pass

    def set_direction(self, direction):
        pass

    # def set_direction_forward(self):
    #     self.direction = 1
    #     pass
    #
    # def set_direction_reverse(self):
    #     self.direction = 0
    #     pass

    def get_direction(self):
        return self.direction

    def set_speed_mlps(self, speedmlps_value):
        self.speedmlps = speedmlps_value
        pass

    def get_speed_mlps(self):
        return self.speedmlps

    # FILTER CLEANING SEQUENCE:

    def cleaning_sequence(self):
        pass

    # MAXSPEED (Percentage of the Max):

    def get_max_speed(self):
        pass

    def set_speed_pom(self, speedpom_value):
        self.speedpom = speedpom_value
        print(f"Setting Mock Speed to {speedpom_value} % of Max")
        pass

    def get_speed_pom(self):
        return self.speedpom

    def set_sensor(self):
        pass

    def add_flow(self):
        pass

    # def get_mode(self):
    #     pass
    #
    # def set_mode(self, mode):
    #     pass


class Pump(AbstractPump):
    duration = 400
    delay = 0.0000001
    pump_pwm = PWMLED(PUL)

    class PumpThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.set_speed_mlps(0)
            self.set_speed_pom(33)
            self.direction = 0
            self.flow = [10, 10, 10]
            self.voltage = []  # the array that will contain the direct voltage values from the sensor (MCP3008)
            self.N = 0
            self.N_flow = 0
            self.delta_t = 1
            #self.mode = PumpMode()
            self.stopped = True

        def run(self):
            #should this be before or after the while not self.stopped?
            self.set_sensor()
            print("Setting sensor succeeded")
            starttime = time.time()
            limit_time = 900  # limit time = 15 min for now mais à définir avec MIT
            lowerbound_flow = 0.5
            flow_time = 5
            self.stopped = False
            while not self.stopped:
                #while True:
                pumping_time = time.time() - starttime
                print(str(len(self.flow) - 1) + str(len(self.flow) - 2))
                actual_flow = (self.flow[len(self.flow) - 1] + self.flow[len(self.flow) - 2]) / 2
                #if limit_time > pumping_time > flow_time and actual_flow < lowerbound_flow: ?
                if pumping_time < limit_time and actual_flow < lowerbound_flow and pumping_time > flow_time:
                    self.cleaning_sequence()
                if pumping_time > limit_time and actual_flow < lowerbound_flow:  # means no more ice, stop the pump
                    break
                else:  # if flow is sufficient
                    print("Pumping")
                    self.run_pump()
                    
        # def run(self):
        #     self.stopped = False
        #     while not self.stopped:
        #         self.set_sensor()
        #         #print("Setting sensor succeeded")
        #         starttime = time.time()
        #         limit_time = 900  # limit time = 15 min for now mais à définir avec MIT
        #         lowerbound_flow = 0.5
        #         flow_time = 5
        #         while not self.stopped:
        #             pumping_time = time.time() - starttime
        #             print(str(len(self.flow) - 1) + str(len(self.flow) - 2))
        #             actual_flow = (self.flow[len(self.flow) - 1] + self.flow[len(self.flow) - 2]) / 2
        #             #if limit_time > pumping_time > flow_time and actual_flow < lowerbound_flow:
        #             if pumping_time < limit_time and actual_flow < lowerbound_flow and pumping_time > flow_time:
        #                 self.cleaning_sequence()
        #             if pumping_time > limit_time and actual_flow < lowerbound_flow:  # means no more ice, stop the pump
        #                 break
        #             else:  # if flow is sufficient
        #                 print("Pumping")
        #                 self.run_pump()
        
        def stop(self):
            self.stopped = True

    pump_thread = PumpThread()

    def run_pump(self):
        cycles = 1
        cyclecount = 0
        while cyclecount < cycles:
            GPIO.setup(ENA, GPIO.OUT)
            GPIO.output(ENA, GPIO.LOW)
            self.set_direction_reverse()
            # duration needs to be set like the settings of the stepper driver
            for x in range(Pump.duration):
                GPIO.output(PUL, GPIO.HIGH)
                sleep(Pump.delay)
                GPIO.output(PUL, GPIO.LOW)
                sleep(Pump.delay)
                self.add_flow()
            cyclecount = (cyclecount + 1)


    def set_direction(self, direction):
        if direction == 1:
            GPIO.output(DIR, GPIO.LOW)
            self.direction = 1
        if direction == 0:
            GPIO.output(DIR, GPIO.HIGH)
            self.direction = 0
        pass


    # def set_direction_forward(self):
    #     GPIO.output(DIR, GPIO.LOW)
    #     self.direction = 1
    #
    # def set_direction_reverse(self):
    #     GPIO.output(DIR, GPIO.HIGH)
    #     self.direction = 0

    def get_direction(self):
        return self.direction

        # SPEED (Liter per Minute):

    def set_speed_mlps(self, speedmlps_value):
        self.speedlpm = speedlpm_value
        pass

    def get_speed_mlps(self):
        return self.speedmlps

    # Stop pump 5 sec, reverse pump 5 sec, stop pump 10 sec to let debris settle /
    # be diluted, normal pump 10 sec, reverse pump 5 sec, stop pump 5 sec, back to normal    pumping
    # FILTER CLEANING SEQUENCE:

    def cleaning_sequence(self):
        time.sleep(5)
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.set_direction(0)
            self.run_pump()
            if elapsed_time > seconds:
                print("Finished iterating in:" + str(int(elapsed_time)))
                break
        time.sleep(10)
        start_time = time.time()
        seconds = 10
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.set_direction(1)
            self.run_pump()
            if elapsed_time > seconds:
                print("Finished iterating in:" + str(int(elapsed_time)))
                break
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.set_direction(0)
            self.run_pump()
            if elapsed_time > seconds:
                print("Finished iterating in:" + str(int(elapsed_time)))
                break
        time.sleep(5)

    # MAXSPEED (Percentage of the Max):

    def get_max_speed(self):
        # return 300 rpm in mlps once we have the mapping
        pass

    def set_speed_pom(self, speedpom):
        self.speedpom = speedpom
        if speedpom < 1.0:
            self.pump_pwm.value = 0.0
        else:
            PULSE_PER_REV = 400.0
            MAX_SPEED_RPM = 300.0
            speed_rpm = (speedpom * MAX_SPEED_RPM)/100.0
            speed_rps = speed_rpm/60.0
            pulse_per_second = speed_rps*PULSE_PER_REV
            self.pump_pwm.frequency = pulse_per_second
            self.pump_pwm.value = 0.2

    def get_speed_pom(self):
        return self.speedpom

    def set_sensor(self):
        print("Setting up sensor...")
        self.N = 1000  # variable determining the number of values we want to keep in VOLTAGE array to compute flow #must be even
        self.N_flow = 1000  # variable determining the number of values we want to keep in FLOW array to compute flow
        # filling up the first 1000 cases of the array
        t0 = time.time()
        while len(self.voltage) < self.N:
            if GPIO.input(26):
                self.voltage.append(1)
            else:
                self.voltage.append(0)
            sleep(0.003)
        t1 = time.time()
        # variable defining the time between each aquisition (seconds)
        self.delta_t = (t1 - t0) / self.N
        print(self.delta_t)
        pass

    def add_flow(self):
        print("Computing flow...")
        self.voltage.pop(1)  # delete first one
        if GPIO.input(26):
            self.voltage.append(1)
        else:
            self.voltage.append(0)
            # add one to the back
        t3 = time.time()
        # the array for the k-space of the FFT
        k = np.linspace(-0.5 / self.delta_t, 0.5 / self.delta_t - 1 / (self.N * self.delta_t), num=self.N)
        # print(channel.voltage)  $
        trans = abs(fftshift(fft(self.voltage)))  # take the fourier transform
        # print(trans)
        frequency = k[np.argmax(trans[501:1000]) + 500]  # take the max close to zero (bc that's the peak that matters)
        # print(str(np.argmax(trans[501:1000])+500))
        # file.write(str(np.max(trans[501:1000]))+"\n")
        if np.amax(trans[501:1000]) < 20:
            frequency = 0.0
        # print(frequency)
        flow_value = frequency / 10500  # turning pulse/second into L/second
        print(str(flow_value * 1000) + " \n")
        self.flow.append(
            flow_value * 1000)  # adding the value of the flow to the array (maybe will be in a file) and putting it in ml/s
        if len(self.flow) > self.N_flow:
            self.flow.pop(1)
        t4 = time.time()
        print("Flow added")
        pass

    # def get_mode(self):
    #     return self.mode
    #
    # def set_mode(self, mode):
    #     self.mode= mode