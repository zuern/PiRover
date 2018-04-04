#!/bin/python
import io
import socket
import struct
import networkSend
from PIL import Image

CAMERAPORT  = 8005
CONTROLPORT = 8001
#ROVER_IP    = "192.168.42.1"
ROVER_IP = "0.0.0.0"

jsonSender = None 
def processImageCallbackFunction(recievedImage):
    print("1")
    global jsonSender
    if (jsonSender is None): 
        jsonSender = networkSend.FileSender(ROVER_IP, CONTROLPORT)
    
    image = Image.open(recievedImage)
    
    print("Saving img to darkflow img folder")
    image.save('../darkflow/img/latest.jpg', format='jpeg')
    
    print("Sending json back to rover")
    jsonSender.sendFile('../darkflow/img/out/latest.json')
# end processImageCallbackFunction

imageReciever = networkSend.FileReciever(CAMERAPORT)
imageReciever.listenForFiles(processImageCallbackFunction)
print(2)
jsonSender.cleanup()
imageReciever.cleanup()
