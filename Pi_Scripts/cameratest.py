import picamera
import time

camera = picamera.PiCamera()

camera.start_recording('video.h264')
time.sleep(5)
camera.stop_recording()
# This will display video out the HDMI port of the Pi
