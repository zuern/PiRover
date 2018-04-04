# CISC 452/COGS 400 PiRover Project
# Kevin Zuern (10134425)
#
# When run this script will enable keyboard control of the Pi Robot via WASD keys
# This script is primarily to test the motors, however logic from this script
# will be borrowed when writing the navigation system of the robot.

import time
import getch
try:
    import RPi.GPIO as gpio
except:
    print("Must run as root to enable GPIO access")
    quit()

freq  = 50 # Hz
speed = 70

# These are the GPIO pins that the motor logic leads are connected to
# see https://pinout.xyz/ for pinout information
motor1A = 3
motor1B = 2
motor2A = 4
motor2B = 17

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(motor1A, gpio.OUT)
gpio.setup(motor1B, gpio.OUT)
gpio.setup(motor2A, gpio.OUT)
gpio.setup(motor2B, gpio.OUT)

p1A = gpio.PWM(motor1A, freq)
p1B = gpio.PWM(motor1B, freq)
p2A = gpio.PWM(motor2A, freq)
p2B = gpio.PWM(motor2B, freq)

pwms = [p1A, p1B, p2A, p2B]

for pwm in pwms:
    pwm.start(0)

def updateDriving(speeds):
    for i in range(4):
        pwms[i].ChangeDutyCycle(speeds[i])
def driveForwards():
    updateDriving([0, speed, 0, speed])
def driveBackwards():
    updateDriving([speed, 0, speed, 0])
def driveLeft():
    updateDriving([0, speed, speed, 0])
def driveRight():
    updateDriving([speed, 0, 0, speed])


print("Controls:")
print("ESC\tExit")
print("WASD: Forward Left Right Back")

# Control the motors from the keyboard via WASD keys
try:
    while True:
        key = ord(getch.getch())
        if key == 27: #ESC
            break
        elif key == 119: # w
            driveForwards()
        elif key == 97: # a
            driveLeft()
        elif key == 115: # s
            driveBackwards()
        else:
            driveRight()

except KeyboardInterrupt:
    p1A.stop()
    p1B.stop()
    gpio.cleanup()

