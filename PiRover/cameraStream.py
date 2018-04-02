#!/bin/python
import io
import socket
import struct
import time
import picamera

'''
This module creates a network stream over which captured images will be sent.
'''
class CameraStream:
    def __init__(self):
        self.initialized = False
        self.socket = socket.socket()
        self.connecton = None
        self.stopSending = None

    def initialize(self, host, port):
        self.socket.connect((host, port))
        self.connection = self.socket.makefile('wb')
        self.initialized = True

    def start_sending(self, delayPerImageInMilliseconds):
        if (self.initialized == False):
            print("Camera Stream was not initialized before startSending was called!")
            return
        try:
            camera = picamera.PiCamera()
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            print("Camera warming up...")
            time.sleep(2)
            print("Camera ready")

            # Construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            stream = io.BytesIO()
            for image in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                self.connection.write(struct.pack('<L', stream.tell()))
                self.connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)

                print("Sending image")
                self.connection.write(stream.read())
                
                if (self.stopSending):
                    break;

                time.sleep(delayPerImageInMilliseconds / 1000)

                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            # Write a length of zero to the stream to signal we're done
            print("Sending quit signal")
            self.connection.write(struct.pack('<L', 0))
        finally:
            print("Cleaning up")
            self.cleanup()
    def cleanup(self):
        self.stopSending = True
        self.connection.close()
        self.socket.close()
# end CameraStream

if __name__ == "__main__":
    cStr = CameraStream()
    cStr.initialize("192.168.0.13", 8000)
    cStr.start_sending(1000)
