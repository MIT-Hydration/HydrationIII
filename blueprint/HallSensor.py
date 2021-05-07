#library for the arrays
import numpy as np
from numpy import amax

#libraries for the voltage measure
from time import sleep,time
import RPi.GPIO as GPIO

#for the FFT
from scipy.fft import fft, ifft, fftshift

#the array that will contain the direct voltage values from the sensor (MCP3008)
voltage=[]

#the array that will contain the measures of the flow
flow=[]

#variable determining the number of values we want to keep in VOLTAGE array to compute flow
#must be even
N=1000

#variable determining the number of values we want to keep in FLOW array to compute flow
N_flow=1000

#create an input GPIO coming from the Hall Effect Sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

#while True:
#    print((GPIO.input(26)))

#filling up the first 1000 cases of the array
t0=time()
while len(voltage)<N:
    if GPIO.input(26):
        voltage.append(1)
    else: 
        voltage.append(0)
    sleep(0.002)
t1=time() 
#variable defining the time between each aquisition (seconds)
delta_t=(t1-t0)/N

file=open("voltage.txt", "w+")

#the array for the k-space of the FFT
k=np.linspace(-0.5/delta_t,0.5/delta_t-1/(N*delta_t),num=N)

#infite loop of: 1) putting values in array 2) measuring the flow 3)putting it in flow array 4) deleting all the useless parts of the array

while True:
    voltage.pop(1)      #delete first one
    if GPIO.input(26):
        voltage.append(1)
    else: 
        voltage.append(0)
        #add one to the back
    t3=time()
    #print(channel.voltage)  $
    trans=abs(fftshift(fft(voltage))) #take the fourier transform
    #print(trans)
    frequency=k[np.argmax(trans[501:1000])+500] #take the max close to zero (bc that's the peak that matters)
    print(str(np.argmax(trans[501:1000])+500))
    file.write(str(np.max(trans[501:1000]))+"\n")
    if np.amax(trans[501:1000])<50:
        frequency=0.0
    print(frequency)
    flow_value= frequency/10500 #turning pulse/second into L/second
    print(str(flow_value*1000) + " \n")
    flow.append(flow_value*1000) #adding the value of the flow to the array (maybe will be in a file) and putting it in ml/s
    if len(flow)>N_flow:
        flow.pop(1)
    t4=time()
    if (t4-t3)<delta_t:
        sleep(delta_t-(t4-t3))
        #print(t4-t3)
    else:
        print(t4-t3)
   # break
# print(delta_t)
# for i in range(len(trans)):
 #   file.write( str(voltage[i])+ "                                    "+ str(trans[i])+"\n" )
