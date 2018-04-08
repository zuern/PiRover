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
            self.imageSender = networkSend.FileSender(host, port)
            print("Connection to server established")
        except:
            print("CameraStream: Couldn't establish connection to the server. Is the server process running already? Exiting now.")
            quit()

    def start_sending(self, FPS):#, delayPerImageInMilliseconds):
        try:
            camera = picamera.PiCamera()
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            print("Camera warming up...")
            time.sleep(2)
            print("Camera ready")
            while True: 
                # We're going to capture 5 frames rapidly, these are their names
                imageFileNames = ["image{}.jpg".format(x) for x in range(5)]
                camera.capture_sequence(imageFileNames, format='jpeg', use_video_port=True)
                for name in imageFileNames:
#                    print("Sending image")
                    self.imageSender.sendFile(name)
                time.sleep(1 / FPS)#delayPerImageInMilliseconds / 1000)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Terminating connection to server")
            self.imageSender.cleanup()
# end CameraStream
