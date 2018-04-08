#!/bin/python

import thread
# Handles sending images to server
import cameraStream
# Handles fetching control signals from server
import controlStream
# Handles navigation of the Rover
import navigationSystem

SERVER_IP   = "192.168.42.11"#"192.168.0.13"
CAMERAPORT  = 8000
CONTROLPORT = 8001

def main():
    try:
        cameraStr  = cameraStream.CameraStream(SERVER_IP, CAMERAPORT)
        controlStr = controlStream.ControlStream()
        nav = navigationSystem.NavigationSystem()
        
        controlStr.initialize(CONTROLPORT, cameraStr, nav)

    except KeyboardInterrupt:
        print("main: keyboard interrupt")
        controlStr.cleanup()
        cameraStr.cleanup()
        nav.cleanup()
    except Exception as e:
        print(e)
        cameraStr.cleanup()

if (__name__ == "__main__"):
    main()
