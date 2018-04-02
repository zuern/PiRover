#!/bin/python

import thread
# Handles sending images to server
import cameraStream
# Handles fetching control signals from server
import controlStream
# Handles navigation of the Rover
import navigationSystem

def main():
    try:
        cameraStr  = cameraStream.CameraStream()
        controlStr = controlStream.ControlStream()
        #nav = navigationSystem.NavigationSystem()
        
        cameraStr.initialize()
        controlStr.initialize(8001)
        #nav.initialize()

        # Start the navigation system up
        #thread.start_new_thread(nav.start, ())
        # Start sending images to the server for processing
        thread.start_new_thread(cameraStr.startSending, ())
        thread.start_new_thread(controlStr.startListening, ())
        return
        while (True):
            # Wait for the server to respond
            serverResponse = controlStr.getServerResponse()
            # Send the response to the navigation system to handle
            thread.start_new_thread(nav.handleResponse, (serverResponse))

    except KeyboardInterrupt:
        cameraStr.cleanup()
        controlStr.cleanup()
        #nav.cleanup()

if (__name__ == "__main__"):
    main()
