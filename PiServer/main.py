#!/bin/python
import io
import socket
import struct
import networkSend
from PIL import Image

CAMERAPORT  = 8000
CONTROLPORT = 8001
ROVER_IP    = "192.168.42.1"
#ROVER_IP = "0.0.0.0"

'''
This script handles images sent from the PI and sends back JSON to the Pi
This script will run until the Pi terminates the image connection.

If you want to stop this program, kill the process on the Pi first.
'''

jsonSender = None

# This gets called every time we recieve a new image
def processImageCallbackFunction(recievedImage, imgNumber):
    global jsonSender
    if (jsonSender is None): 
        jsonSender = networkSend.FileSender(ROVER_IP, CONTROLPORT)
    try:
        image = Image.open(recievedImage)
        
        #print("Saving img to darkflow img folder")
        # TESTING: image.save("../darkflow/img/latest.png")

        # Save the image sent from the Pi to the darkflow input folder, with an added image number
        image.save("../darkflow/img/img{}.jpg".format(imgNumber), format='jpeg')
        
        #print("Sending json back to rover")
        jsonSender.sendFile('../darkflow/img/out/latest.json')
    except BrokenPipeError:
        print("The connection to the pi was broken. Exiting program")
        quit()
    except IOError:
        print("The connection to the pi was broken. Exiting program")
        quit()    
# end processImageCallbackFunction

# This gets called once the image reciever has finished recieving images
def cleanupCallbackFn():
    global jsonSender
    if (jsonSender != None):
        jsonSender.cleanup()
# end cleanupCallbackFn

try:
    print("Setting up server and listening for images from PiRover on port {}".format(CAMERAPORT))
    # Set up our image reciever and run it on a new thread
    imageReciever = networkSend.FileReciever(CAMERAPORT, processImageCallbackFunction, cleanupCallbackFn)
    # Run the imageReciever synchronously (blocks the process from exiting)
    imageReciever.run()
    print("Server process exiting.")
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting.")
    if (jsonSender != None):
        jsonSender.cleanup()
    imageReciever.cleanup()
