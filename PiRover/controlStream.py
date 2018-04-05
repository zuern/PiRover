#!/bin/python

import networkSend
import navigationSystem
import json
import time
import math

'''
This class is responsible for listening to and parsing responses from the server
'''
class ControlStream:
    def fileRecievedCallback(self, fileStream, ignored):
        try:
            print("Recieved JSON from server\n")
            time.sleep(1)
            data = json.load(fileStream)

            if (len(data) == 0): # nothing detected
                print("-->Nothing detected. Ambling around")
                self.nav.amble()
            else:
                print("-->object detected!")
                angleToObject = self.computeAngle(data[0], self.cameraStream.w ,self.cameraStream.h)
                if math.degrees(abs(angleToObject)) < 20:
                    print("-->Angle to obj: {}".format(math.degrees(angleToObject)))
                    self.nav.drive_forwards(0.5)
                else:
                    print("-->Turning to face object")
                    self.nav.turn(angleToObject)

            # Send the next image
            self.cameraStream.sendImage()
        except KeyboardInterrupt:
            print("KB intterupt!")
            nav.cleanup()
            quit()
        except Exception as e:
            print(e)
            return False
    
    def cleanupCallback(self):
        return # do nothing

    def initialize(self, port, cameraStream, navigationSystem):
        self.cameraStream = cameraStream
        self.nav = navigationSystem
        self.listener = networkSend.FileReciever(port, self.fileRecievedCallback, self.cleanupCallback)
        self.listener.start()
        print("Rover listening for server instructions on port {}".format(port))
        
        # Send the first image
        self.cameraStream.sendImage()
    # end initialize

    # Find the angle the centroid of obj is from the bottom center of the image
    # w = image with
    # h = image height
    # obj = bounding box from CNN
    def computeAngle(self, obj, w, h):
        # Centroid coordinates of the box
        bx = w + (obj['bottomright']['x'] - obj['topleft']['x']) / 2
        by = h - (obj['bottomright']['y'] - obj['topleft']['y']) / 2
        
        # angle off center bottom of image in radians
        theta = math.atan( ((0.5 * w) - bx) / (h - by) )
        return theta
