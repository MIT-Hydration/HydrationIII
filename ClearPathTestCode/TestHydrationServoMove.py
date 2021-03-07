import HydrationServo
import time

if __name__ == "__main__":
    print ("Init Done!")
    tolerance = 0.001 # m
    target = -2 * 25.4/1000 # -2 inches to m
    PID_P = 10
    try:
        HydrationServo.set_drill_speed(0)
        current_position = HydrationServo.get_drill_position()
        while (abs(current_position - target) > tolerance):
            speed = PID_P * (target - current_position) 
            HydrationServo.set_drill_speed(speed)
            time.sleep(0.1)
            current_position = HydrationServo.get_drill_position()
            print (f'Drill Position: {current_position} m')
    except:
        print("Exception!")
        HydrationServo.set_drill_speed(0)
    HydrationServo.set_drill_speed(0)

