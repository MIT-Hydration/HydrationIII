import HydrationServo
import time
import numpy

def move_to_target_position(target):
    PID_P = 10000
    TOLERANCE = 0.001/2.0 # m
    MAX_SPEED = 250 # rpm
    HydrationServo.set_speed_rpm(3, 0)
    current_position = HydrationServo.get_position(3)*4.0
    while (abs(current_position - target) > TOLERANCE):
        speed = PID_P * (target - current_position)
        if (abs(speed) > MAX_SPEED):
            speed = numpy.sign(speed)*MAX_SPEED
        HydrationServo.set_speed_rpm(3, speed)
        time.sleep(0.1)
        current_position = HydrationServo.get_position(3)*4.0
        print (f'Drill Position: {current_position} m')
    HydrationServo.set_speed_rpm(3, 0)

if __name__ == "__main__":
    print ("Init Done!")
    target = 0.355 # cm
    try:
        for i in range(5):
            move_to_target_position(0) # move down
            time.sleep(5)
            move_to_target_position(target)
            time.sleep(5)
            move_to_target_position(0) # home
            time.sleep(5)
            move_to_target_position(target/2.0)
            time.sleep(5)
            move_to_target_position(0) # home
            time.sleep(5)
    except Exception as e:
        print("Exception!")
        print(e)
        HydrationServo.set_speed_rpm(3, 0)
    HydrationServo.set_speed_rpm(3, 0)

