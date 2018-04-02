#!/bin/python

'''
PiRover Server-Side Image Capture

This script receives images from the PiRover's onboard camera in a continuous stream.

Script taken from picamera.readthedocs.io
'''

import io
import socket
import struct
from PIL import Image

# Start listening on all interfaces port 8000
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

print("Server listening on all interfaces on port 8000")

# Accept a connection and create a file-like object from it
connection = server_socket.accept()[0].makefile('rb')
print("Accepted connection, reading input...")
try:
    while True:
        imageLen = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if imageLen is 0:
            break
        imageStream = io.BytesIO()
        imageStream.write(connection.read(imageLen))
        # Rewind the stream, open as image with PIL and do stuff
        image = stream.seek(0)
        image = Image.open(imageStream)
        print("Image is %dx%d" % image.size)
        image.verify()
        print("Image is verified")
finally:
    connection.close()
    server_socket.close()
