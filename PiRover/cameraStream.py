#!/bin/python
import io
import socket
import struct
import time
import picamera
import networkSend

FPS = 1/2

'''
This module creates a network stream over which captured images will be sent.
'''
class CameraStream:
    def __init__(self, host, port):
        try:
            self.imgSender = networkSend.FileSender(host, port)
            print("Connection to server established")
        except:
            print("CameraStream: Couldn't establish connection to the server. Exiting now.")
            quit()

    def start_sending(self):#, delayPerImageInMilliseconds):
        try:
            camera = picamera.PiCamera()
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            print("Camera warming up...")
            time.sleep(2)
            print("Camera ready")
            
            for image in camera.capture_continuous('latest.jpg', 'jpeg'):
                print("Sending image")
                self.imageSender.sendFile('latest.jpg')
                time.sleep(1 / FPS)#delayPerImageInMilliseconds / 1000)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Terminating connection to server")
            self.imgSender.cleanup()
# end CameraStream

if __name__ == "__main__":
    cStr = CameraStream("192.168.42.11", 8000)
    cStr.start_sending()
