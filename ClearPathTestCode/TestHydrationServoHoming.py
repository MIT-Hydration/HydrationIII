import HydrationServo
import time

if __name__ == "__main__":
    print ("Init Done!")
    tolerance = 0.001 # m
    try:
        HydrationServo.set_speed_rpm(3, 0)
        current_position = HydrationServo.get_position(3)
        while (abs(current_position) > tolerance):
            if (current_position > 0):
                direction = -1
            else:
                direction = 1    
            HydrationServo.set_speed_rpm(3, 10*direction)
            time.sleep(0.1)
            current_position = HydrationServo.get_position(3)
            print (f'Drill Position: {current_position} m')
    except:
        print("Exception!")
        HydrationServo.set_speed_rpm(3, 0)
    HydrationServo.set_speed_rpm(3, 0)

