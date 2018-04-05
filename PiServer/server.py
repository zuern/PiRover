#!/bin/python
import os
import time
import networkSend
from PIL import Image

CAMERAPORT  = 8000
CONTROLPORT = 8001
ROVER_IP    = "192.168.42.1" #"192.168.42.1"
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
        
        print("Saving img to darkflow img folder")
        image.save("../darkflow/img/latest.jpg", format='jpeg')
        
        print("Sending json back to rover")
        try:
            filePath = '../darkflow/img/out/latest.json'.format(imgNumber)
            while (os.path.isfile(filePath) is False):
                print("Waiting for darkflow to output json file to disk...")
                time.sleep(0.1)
            jsonSender.sendFile(filePath)
            print("Sent json\n")
        except Exception as e:
            print(e)
            print("Couldn't send the json file. Exiting")
    except IOError as e:
        print("The connection to the pi was broken. Exiting program")
        print(e)
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
    print("Setting up server and listening for images from PiRover on port {}".format(CAMERAPORT))
    # Set up our image reciever and run it on a new thread
    imageReciever = networkSend.FileReciever(CAMERAPORT, processImageCallbackFunction, cleanupCallbackFn)
    # Run the imageReciever synchronously (blocks the process from exiting)
    imageReciever.run()
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting.")
    if (jsonSender != None):
        jsonSender.cleanup()
except Exception as e:
    print("Error. Exiting")
    print(e)
    quit()

print("Server process exiting.")
