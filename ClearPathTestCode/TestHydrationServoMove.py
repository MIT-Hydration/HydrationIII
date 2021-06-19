import HydrationServo
import time
import numpy

def move_to_target_position(target):
    PID_P = 10000
    TOLERANCE = 0.00001/2.0 # m
    MAX_SPEED = 50 # rpm
    HydrationServo.set_speed_rpm(0, 0)
    current_position = HydrationServo.get_position(0)*4.0
    while (abs(current_position - target) > TOLERANCE):
        speed = PID_P * (target - current_position)
        if (abs(speed) > MAX_SPEED):
            speed = numpy.sign(speed)*MAX_SPEED
        HydrationServo.set_speed_rpm(0, speed)
        time.sleep(0.1)
        current_position = HydrationServo.get_position(0)*4.0
        print (f'Drill Position: {current_position} m')
    HydrationServo.set_speed_rpm(0, 0)

if __name__ == "__main__":
    print ("Init Done!")
    current_position = HydrationServo.get_position(0)*4.0
    print (f"Current Position: {current_position}") 
    target = current_position + 0.03
    try:
        move_to_target_position(target) # move down
    except Exception as e:
        print("Exception!")
        print(e)
        HydrationServo.set_speed_rpm(0, 0)
    HydrationServo.set_speed_rpm(0, 0)

