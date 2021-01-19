import time

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder

from gpiozero import PWMLED
from gpiozero import CPUTemperature

print("Reading registers")
client = ModbusSerialClient(port='/dev/ttyUSB0', method='rtu', baudrate=9600)
#response = client.read_holding_registers(75,2,unit=1)
#print(response.registers[0])
#print(response.registers[1])

address = 75
count   = 4

motor = PWMLED(12)
cpu = CPUTemperature()

time_start_s = time.time()
fp = open(f"{time_start_s}.csv", "w")
fp.write("Time [s], CPU Temperature [degC], PWM command, Current [mA], Active Power [W]\n")
while True:
    time_s = time.time()
    time_s_10sint = int((time_s - time_start_s)/10)
    pwm_val = (time_s_10sint%5)*0.25
    if pwm_val > 1.0:
        pwm_val = 1.0
    motor.value = (time_s_10sint%5)*0.25
    result  = client.read_holding_registers(address, count,  unit=1)
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, 
        wordorder = '>', byteorder = '>')
    current_mA = decoder.decode_32bit_float()
    power_W = decoder.decode_32bit_float()
    cpu_temp = cpu.temperature
    print (f"{time_s}, {cpu_temp} [degC], {motor.value}, {current_mA} [mA], {power_W} [W]")
    fp.write (f"{time_s}, {cpu_temp}, {motor.value}, {current_mA}, {power_W}\n")
    time.sleep(0.02)

client.close()
fp.close()



