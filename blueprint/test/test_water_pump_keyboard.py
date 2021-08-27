from ..hardware import HardwareFactory
import time
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    pump = HardwareFactory.getWaterPump()
    
    current_speed = 0
    pump.set_speed_rpm(current_speed)
    
    stdscr.nodelay(True)
    while(True):
        time.sleep(0.1)
        stdscr.addstr(0, 0, f'Press "f" for forward at 250 RPM, "r" for reverse at 250 RPM, "s" for stop, "e" for exit')
        stdscr.addstr(1, 0, f'Current Speed == {current_speed} RPM (positive forward, negative reverse)')
        
        ch = stdscr.getch()
        if ch == -1:
            ch = 'nothing'
        else:
            ch = chr(ch)
        stdscr.addstr(2, 0, f'You pressed {ch}         ')
        stdscr.refresh()
        if ch == 'nothing':
            continue

        if ch == 'f':
            current_speed = 250
        elif ch == 'r':
            current_speed = -250
        elif (ch == 's') or (ch == 'e'):
            current_speed = 0
        
        pump.set_speed_rpm(current_speed)
    
        if ch == 'e':
            break
        
wrapper(main)