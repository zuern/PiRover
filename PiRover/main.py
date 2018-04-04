#!/bin/python

import thread
# Handles sending images to server
import cameraStream
# Handles fetching control signals from server
import controlStream
# Handles navigation of the Rover
import navigationSystem

SERVER_IP   = "192.168.42.11"
CAMERAPORT  = 8000
CONTROLPORT = 8001

def main():
    try:
        cameraStr  = cameraStream.CameraStream()
        controlStr = controlStream.ControlStream()
        #nav = navigationSystem.NavigationSystem()
        
        controlStr.initialize(CONTROLPORT)
        cameraStr.initialize(SERVER_IP, CAMERAPORT)
        #nav.initialize()

        # Start the navigation system up
        #thread.start_new_thread(nav.start, ())
        # Start sending images to the server for processing
        thread.start_new_thread(cameraStr.start_sending, ())
        #cameraStr.start_sending(1000)
        while (True):
            # Wait for the server to respond
            serverResponse = controlStr.get_server_response()
            # Send the response to the navigation system to handle
            #thread.start_new_thread(nav.handleResponse, (serverResponse))

    except KeyboardInterrupt:
        cameraStr.cleanup()
        controlStr.cleanup()
        #nav.cleanup()

if (__name__ == "__main__"):
    main()
