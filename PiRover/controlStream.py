#!/bin/python

import networkSend
import json

'''
This class is responsible for listening to and parsing responses from the server
'''
class ControlStream:
    def computeDrivingDirection(boundingBox):
        print(boundingBox)
        # Get the dimensions of the image
        dim = self.imgDimensions.split("x")
        w = dim[0]
        h = dim[1]

        # Get the centroid of the bounding box
        centroid = (box['width'] / 2 + box['x'], box['height'] / 2 + box['y'])



    def fileRecievedCallback(self, fileStream, ignored):
#       print("Recieved JSON from server")
       data = json.load(fileStream)
       for box in data:
           if (box['class'] == "car"):
               print("Car detected! Sending navigation instructions to navigation system")
               driveDirection = self.computeDrivingDirection(box)

       print(data)
    
    def cleanupCallback(self):
        return # do nothing

    def initialize(self, port, imgDimensions):
        self.imgDimensions = imgDimensions
        self.listener = networkSend.FileReciever(port, self.fileRecievedCallback, self.cleanupCallback)
        print("Rover listening for server instructions on port {}".format(port))

    def startListening(self):
        self.listener.start()
