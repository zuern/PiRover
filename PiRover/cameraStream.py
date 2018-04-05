#!/bin/python
import io
import socket
import struct
import time
import picamera
import networkSend

'''
This module creates a network stream over which captured images will be sent.
'''
class CameraStream:
    def __init__(self, host, port):
        try:
            self.w = 640
            self.h = 480
            self.camera = picamera.PiCamera()
            self.camera.resolution = (self.w, self.h)
            # Start a preview and let the camera warm up for 2 seconds
            self.camera.start_preview()
            print("Camera warming up...")
            time.sleep(2)
            print("Camera ready")
            
            
            self.imageSender = networkSend.FileSender(host, port)
            print("Connection to server established")
        except Exception as e:
            print(e)
            print("CameraStream: Couldn't establish connection to the server. Is the server process running already? Exiting now.")
            quit()

    def sendImage(self):
        try:
            print("Capturing")
            self.camera.capture('img.jpg', format='jpeg')    
            print("Sending image")
            self.imageSender.sendFile('img.jpg')
            print("Image sent")
        except Exception as e:
            print("CameraStream sending failed")
            print(e)
            self.cleanup()
            quit()

    def cleanup(self):
        self.imageSender.cleanup()

# end CameraStream
