import picamera
import time

'''
Display video recording from PiCamera to the HDMI out on the raspberry pi
'''

camera = picamera.PiCamera()

camera.start_recording('video.h264')
time.sleep(5)
camera.stop_recording()
# This will display video out the HDMI port of the Pi
