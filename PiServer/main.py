#!/bin/python
import io
import socket
import struct
from PIL import Image

LISTENPORT  = 8000
CONTROLPORT = 8001
ROVER_IP    = "192.168.0.2"

# Start a socket listening for connections on all interfaces
# Listens to receive images from the rover
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', LISTENPORT))
server_socket.listen(0)
print("Server listening on port {}".format(LISTENPORT))

# Accept a single connection and make a file-like object out of it
image_connection = server_socket.accept()[0].makefile('rb')
print("Image connection established with rover")

# Now that a connection is established to receive images, create a connection to send tag data
control_socket = socket.socket()
print("Connecting control connection to rover")
control_socket.connect((ROVER_IP, CONTROLPORT))
control_connection = control_socket.makefile('wb')
print("Control connection established")

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
        '''
        TODO: Hook in the CNN here, feeding in image.
        '''
        print('Image is verified')
        # Display the image in a default program on your pc
        #image.show()
        sampleJSON = '[{"label":"person", "confidence": 0.56, "topleft": {"x": 184, "y": 101}, "bottomright": {"x": 274, "y": 382}},{"label": "dog", "confidence": 0.32, "topleft": {"x": 71, "y": 263}, "bottomright": {"x": 193, "y": 353}},{"label": "horse", "confidence": 0.76, "topleft": {"x": 412, "y": 109}, "bottomright": {"x": 592,"y": 337}}]'


finally:
    image_connection.close()
    server_socket.close()