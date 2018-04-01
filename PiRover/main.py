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
        cameraStream.initialize()
        controlStream.initialize()
        navigationSystem.initialize()

        # Start the navigation system up
        thread.start_new_thread(navigationSystem.start, ())
        # Start sending images to the server for processing
        thread.start_new_thread(cameraStream.startSending, ())
        while (True):
            # Wait for the server to respond
            serverResponse = controlStream.getServerResponse()
            # Send the response to the navigation system to handle
            thread.start_new_thread(navigationSystem.handleResponse, (serverResponse))

    except KeyboardInterrupt:
        cameraStream.cleanup()
        controlStream.cleanup()
        cameraCapture.cleanup()
        navigationSystem.cleanup()

if (__name__ == "__main__"):
    main()
