import HydrationServo
import time

if __name__ == "__main__":
    print ("Init Done!")
    tolerance = 0.01 # m
    try:
        HydrationServo.set_drill_speed(0)
        current_position = HydrationServo.get_drill_position()
        while (abs(current_position) > tolerance):
            if (current_position > 0):
                direction = -1
            else:
                direction = 1    
            HydrationServo.set_drill_speed(10*direction)
            time.sleep(0.1)
            current_position = HydrationServo.get_drill_position()
            print (f'Drill Position: {current_position} m')
    except:
        print("Exception!")
        HydrationServo.set_drill_speed(0)
    HydrationServo.set_drill_speed(0)

