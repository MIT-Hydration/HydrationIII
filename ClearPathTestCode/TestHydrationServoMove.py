import HydrationServo
import time
import numpy

def move_to_target_position(target):
    PID_P = 100000
    TOLERANCE = 0.001 # m
    MAX_SPEED = 250 # rpm
    HydrationServo.set_drill_speed(0)
    current_position = HydrationServo.get_drill_position()
    while (abs(current_position - target) > TOLERANCE):
        speed = PID_P * (target - current_position)
        if (abs(speed) > MAX_SPEED):
            speed = numpy.sign(speed)*MAX_SPEED
        HydrationServo.set_drill_speed(speed)
        time.sleep(0.1)
        current_position = HydrationServo.get_drill_position()
        print (f'Drill Position: {current_position} m')
    HydrationServo.set_drill_speed(0)

if __name__ == "__main__":
    print ("Init Done!")
    target = -4 * 25.4/1000 # -2 inches to m
    try:
        move_to_target_position(0) # home
        time.sleep(1)
        move_to_target_position(target)
    except Exception as e:
        print("Exception!")
        print(e)
        HydrationServo.set_drill_speed(0)
    HydrationServo.set_drill_speed(0)

