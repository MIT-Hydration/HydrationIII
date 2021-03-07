import HydrationServo
import time

if __name__ == "__main__":
    print ("Init Done!")
    print (f'Drill Position: {HydrationServo.get_drill_position()} m')
    HydrationServo.set_drill_speed(0)
    HydrationServo.set_drill_speed(-10)
    for i in range(100):
        print (f'Drill Position: {HydrationServo.get_drill_position()} m')
        time.sleep(0.1)
    HydrationServo.set_drill_speed(0)

