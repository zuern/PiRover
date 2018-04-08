#!/bin/python

import networkSend
import json

'''
This class is responsible for listening to and parsing responses from the server
'''
class ControlStream:
    def fileRecievedCallback(self, fileStream, ignored):
#       print("Recieved JSON from server")
       data = json.load(fileStream)
       print(data)
    
    def cleanupCallback(self):
        return # do nothing

    def initialize(self, port):
        self.listener = networkSend.FileReciever(port, self.fileRecievedCallback, self.cleanupCallback)
        print("Rover listening for server instructions on port {}".format(port))

    def startListening(self):
        self.listener.start()
