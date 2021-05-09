import HydrationServo
import time

if __name__ == "__main__":
    print ("Init Done!")
    N = HydrationServo.get_num_motors()
    print(f'Number of Motors Detected = {N}')
    for i in range(N):
        print(f'Motor Name: {HydrationServo.get_motor_id(i)}')
        print (f'Motor Position: {HydrationServo.get_position(i)} m')
        HydrationServo.set_speed_rpm(i, 0)
        for i in range(100):
            print (f'Motor Position: {HydrationServo.get_position(i)} m')
            time.sleep(0.1)
        HydrationServo.set_speed_rpm(-10)
        HydrationServo.set_speed_rpm(0)
        for i in range(100):
            print (f'Motor Position: {HydrationServo.get_position(i)} m')
            time.sleep(0.1)
        

