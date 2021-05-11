import HydrationServo
import time

if __name__ == "__main__":
    print ("Init Done!")
    N = HydrationServo.get_num_motors()
    print(f'Number of Motors Detected = {N}')
    for n in range(N):
        print(f'Motor Name: {HydrationServo.get_motor_id(n)}')
        print (f'Motor Position: {HydrationServo.get_position(n)} m')
        HydrationServo.set_speed_rpm(n, 0)
        for i in range(100):
            print (f'Motor Position: {HydrationServo.get_position(n)} m')
            time.sleep(0.1)
        HydrationServo.set_speed_rpm(n, -10)
        for i in range(100):
            print (f'Motor Position: {HydrationServo.get_position(n)} m')
            time.sleep(0.1)
        HydrationServo.set_speed_rpm(n, 0)
        

