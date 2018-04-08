# CISC 452/COGS 400 PiRover Project
# Kevin Zuern (10134425)
#
# When run this script will enable keyboard control of the Pi Robot via WASD keys
# This script is primarily to test the motors, however logic from this script
# will be borrowed when writing the navigation system of the robot.

import getch
import sys
import math
import time
sys.path.append('..') # include parent folder scripts in path
import navigationSystem
nav = navigationSystem.NavigationSystem()

def keyboardControl():
    # Control the motors from the keyboard via WASD keys
    try:
        while True:
            key = ord(getch.getch())
            if key == 27: #ESC
                break
            elif key == 119: # w
                nav.drive_forwards()
            elif key == 97: # a
                nav.drive_left()
            elif key == 115: # s
                nav.drive_backwards()
            else:
                nav.drive_right()

    except KeyboardInterrupt:
        nav.cleanup()
# end keyboardControls

if __name__ == "__main__":
    nav.drive_forwards()
    time.sleep(0.5)
    print("stopping")
    nav.stop()
    time.sleep(2)
    nav.cleanup()
#    keyboardControl()
