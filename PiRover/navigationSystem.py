#!/bin/python

import time
import math
from random import randint
try:
    import RPi.GPIO as gpio
except:
    print("NavigationSystem must be run as root (it needs GPIO access)")
    quit()

'''
This class contains all the navigation logic/commands for the PiRover
'''
class NavigationSystem:
    def __init__(self):
        self.ambleAround = True
        self.freq  = 50 # Hz
        self.speed = 70

        # These are the GPIO pins that the motor logic leads are connected to
        # see https://pinout.xyz/ for pinout information
        motor1A = 3
        motor1B = 5
        motor2A = 8
        motor2B = 10

        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)

        gpio.setup(motor1A, gpio.OUT)
        gpio.setup(motor1B, gpio.OUT)
        gpio.setup(motor2A, gpio.OUT)
        gpio.setup(motor2B, gpio.OUT)

        p1A = gpio.PWM(motor1A, self.freq)
        p1B = gpio.PWM(motor1B, self.freq)
        p2A = gpio.PWM(motor2A, self.freq)
        p2B = gpio.PWM(motor2B, self.freq)

        self.pwms = [p1A, p1B, p2A, p2B]

        for pwm in self.pwms:
            pwm.start(0)

        self.start()
    # end __init__

    '''
    Makes the rover move aimlessly around the terrain until self.ambleAround is set to False
    '''
    def start(self):
        # Possible actions that can be taken
        actions = [self.drive_forwards, self.drive_backwards, self.drive_left, self.drive_right]
        while True:
            # Pick an action to do
            nextAction = randint(0,4)
            # Pick how long to do it in milliseconds
            duration = randint(1, 2000)
            timeElapsed = 0
            while timeElapsed < duration and self.ambleAround is True:
                # Execute the chosen action
                actions[nextAction]()
                # Wait 10 ms before checking in again
                time.sleep(0.01)
                timeElapsed += 10
            

    def __updateDriving(self, speeds):
        for i in range(4):
            self.pwms[i].ChangeDutyCycle(speeds[i])
    
    # Turn the robot an angle of theta radians from it's front facing position.
    # Positive theta values will turn right, negative left
    # Theta should be < 90 degrees
    # This will only be approximate since we're using DC motors and not stepper motors to control the rover
    def turn(self, theta):
        self.stop()
        time.sleep(0.1) # Give motors a sec to wind down
        # We need to calculate how long the motor should run to make it travel the correct distance to turn the rover
        # The following values were measured, and are approximate
        c       = 6 *  math.pi  # Circumference of the wheels in cm
        track   = 10.4          # Tire-to-Tire width in cm
        RPS     = 2.208         # Tire revolutions per second (approximate)
        timeToSleep = (c * track * math.sin(theta) ) / RPS
        print("TTS: {}".format(timeToSleep))
        if theta > 0:
            # Turning right, so use the left motor only, going forwards
            self.__updateDriving([0, 0, 0, self.speed])
        else:
            self.__updateDriving([0, self.speed, 0, 0])
        time.sleep(timeToSleep)
        self.stop()

    def drive_forwards(self):
        self.__updateDriving([0, self.speed, 0, self.speed])
    
    def drive_backwards(self):
        self.__updateDriving([self.speed, 0, self.speed, 0])
    
    def drive_left(self):
        self.__updateDriving([0, self.speed, self.speed, 0])
    
    def drive_right(self):
        self.__updateDriving([self.speed, 0, 0, self.speed])
    
    def stop(self):
        self.__updateDriving([0,0,0,0])
    
    def cleanup(self):
        for pwm in self.pwms:
            pwm.stop()
        gpio.cleanup()
