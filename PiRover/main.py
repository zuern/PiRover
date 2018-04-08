#!/bin/python

import thread
# Handles sending images to server
import cameraStream
# Handles fetching control signals from server
import controlStream
# Handles navigation of the Rover
import navigationSystem

SERVER_IP   = "192.168.0.13"#"192.168.42.11"
CAMERAPORT  = 8000
CONTROLPORT = 8001

def main():
    try:
        cameraStr  = cameraStream.CameraStream(SERVER_IP, CAMERAPORT)
        controlStr = controlStream.ControlStream()
        #nav = navigationSystem.NavigationSystem()
        
        controlStr.initialize(CONTROLPORT)
        #nav.initialize()

        # Start the navigation system up
        #thread.start_new_thread(nav.start, ())
        
        serverResponse = controlStr.startListening()
        # Start sending images to the server for processing
        cameraStr.start_sending(50) # FPS
        
        # Send the response to the navigation system to handle
            #thread.start_new_thread(nav.handleResponse, (serverResponse))

    except KeyboardInterrupt:
        controlStr.cleanup()
        #nav.cleanup()

if (__name__ == "__main__"):
    main()
