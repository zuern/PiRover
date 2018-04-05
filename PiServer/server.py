#!/bin/python3
from sys import argv
import numpy as np
from PIL import Image
import json
from darkflow.cli import cliHandler
import networkSend

CAMERAPORT  = 8000
CONTROLPORT = 8001
ROVER_IP    = "192.168.0.32" #"192.168.42.1"
#ROVER_IP = "0.0.0.0"

'''
This script handles images sent from the PI and sends back JSON to the Pi
This script will run until the Pi terminates the image connection.

If you want to stop this program, kill the process on the Pi first.
'''

jsonSender = None
network = None


# This gets called every time we recieve a new image
def processImageCallbackFunction(recievedImage, imgNumber):
    global jsonSender
    global network
    if (jsonSender is None): 
        jsonSender = networkSend.StringSender(ROVER_IP, CONTROLPORT)
    try:
        # Import received image as numpy array
        image = np.array(Image.open(recievedImage))
        
        print("Generating prediction...")
        # Predict bounding box info (yields dict in standard format)
        prediction = network.return_predict(image)
	
        print("Sending JSON back to rover")
        jsonSender.sendString(json.dumps(prediction))
    except BrokenPipeError:
        print("The connection to the pi was broken. Exiting program")
        quit()
    except IOError:
        print("The connection to the pi was broken. Exiting program")
        quit()    
# end processImageCallbackFunction

# This gets called once the image reciever has finished recieving images
def cleanupCallbackFn():
    print("Hit server cleanup")
    global jsonSender
    if (jsonSender != None):
        jsonSender.cleanup()
# end cleanupCallbackFn



'''
MAIN CODE BELOW
'''
try:
    # Set up neural network with desired weights
    network = cliHandler(argv)

    print("Setting up server and listening for images from PiRover on port {}".format(CAMERAPORT))
    # Set up our image reciever and run it on a new thread
    imageReciever = networkSend.FileReciever(CAMERAPORT, processImageCallbackFunction, cleanupCallbackFn)
    # Run the imageReciever synchronously (blocks the process from exiting)
    imageReciever.run()

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting.")
    if (jsonSender != None):
        jsonSender.cleanup()
    imageReciever.cleanup()
except Exception as e:
    print("Error. Exiting")
    print(e)
    quit()

print("Server process exiting.")
