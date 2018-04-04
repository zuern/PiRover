#!/bin/python

import time
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
        # see https://www.raspberrypi.org/documentation/usage/gpio/images/a-and-b-gpio-numbers.png for pinout information
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
        currentAction = None
        try:
            while True:
                    # Pick an action to do
                    nextAction = randint(0,3)
                    # Pick how long to do it in milliseconds
                    duration = randint(1000, 2000)
                    timeElapsed = 0
                    while timeElapsed < duration and self.ambleAround is True:
                        timeElapsed += 10
                        # Wait 10 ms before checking in again
                        time.sleep(0.01)
                        #print("TE {} DU {}".format(timeElapsed, duration))
                        if (currentAction == nextAction):
                            continue
                        # Execute the chosen action
                        currentAction = nextAction
                        actions[nextAction]()
        finally:
            self.cleanup()
            

    def __updateDriving(self, speeds):
        for i in range(4):
            self.pwms[i].ChangeDutyCycle(speeds[i])
    
    def drive_forwards(self):
        #print("Driving forwards")
        self.__updateDriving([0, self.speed, 0, self.speed])
    
    def drive_backwards(self):
        #print("Back")
        self.__updateDriving([self.speed, 0, self.speed, 0])
    
    def drive_left(self):
        #print("Left")
        self.__updateDriving([0, self.speed, self.speed, 0])
    
    def drive_right(self):
        #print("Right")
        self.__updateDriving([self.speed, 0, 0, self.speed])
    
    def stop(self):
        self.__updateDriving([0,0,0,0])
    
    def cleanup(self):
        print("Cleaning up motors")
        for pwm in self.pwms:
            pwm.stop()
        gpio.cleanup()
