#!/bin/python
import io
import socket
import struct
from PIL import Image

CAMERAPORT  = 8005
CONTROLPORT = 8001
ROVER_IP    = "192.168.42.1"

# Start a socket listening for connections on all interfaces
# Listens to receive images from the rover
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', CAMERAPORT))
server_socket.listen(0)
print("Server listening on port {}".format(CAMERAPORT))

# Accept a single connection and make a file-like object out of it
image_connection = server_socket.accept()[0].makefile('rb')
print("Image connection established with rover")

# Now that a connection is established to receive images, create a connection to send tag data
control_socket = socket.socket()
control_socket.connect((ROVER_IP, CONTROLPORT))
control_connection = control_socket.makefile('wb')
print("Control connection established with rover")
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', image_connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the image_connection
        image_stream = io.BytesIO()
        image_stream.write(image_connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
        image.verify()
        image = Image.open(image_stream)
	print('Image is verified')
        
        print("Saving img to darkflow img folder")
	image.save('../darkflow/img/latest.jpg', format='jpeg')
        print("Waiting for darkflow to process image")
        thread.sleep(1)
        print("Sending json back to rover")

        jsonBytes = open("../darkflow/img/out/latest.json", 'rb')
        jsonData = jsonBytes.read()
        size = len(jsonData)
        jsonBytes.close()

        control_socket.send(jsonData)


        break

finally:
    image_connection.close()
    control_connection.close()
    control_socket.close()
    server_socket.close()
