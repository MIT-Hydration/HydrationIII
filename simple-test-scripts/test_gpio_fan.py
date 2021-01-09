from gpiozero import PWMLED
from gpiozero import CPUTemperature
from time import sleep

led = PWMLED(12)
cpu = CPUTemperature()

while True:
    print("Turning off")
    led.value = 0  # off
    print('temperature: {}C'.format(cpu.temperature))
    sleep(1)
    print("Turning half")
    led.value = 0.5  # half brightness
    print('temperature: {}C'.format(cpu.temperature))
    sleep(1)
    print("Turning on")
    led.value = 1  # full brightness
    print('temperature: {}C'.format(cpu.temperature))
    sleep(1)
