import time
import networkSend

'''
This file illustrates how the Pi's image sending / control recieving logic should work
'''

# Pi recieving commands from the server
def recieve(stream, ignored):
    print("Recieved JSON response from server")

def cleanup():
    # Do nothing
    return

sender = networkSend.FileSender("0.0.0.0", 8005)
reciever = networkSend.FileReciever(8001, recieve, cleanup)

reciever.start()

# Simulate the Pi sending 10 frames to the server
try:
    while True:
        print("Sending server new image file")
        sender.sendFile("/home/kevin/Pictures/archlinuxlogo.png")
        time.sleep(1)
except KeyboardInterrupt:
    print("detected interrupt. terminating program")
# Pi closing the connection to the server, terminating the program locally and on the server
sender.cleanup()
