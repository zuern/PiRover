import networkSend
import thread

'''
This file illustrates how the Pi's image sending / control recieving logic should work
'''

sender = networkSend.FileSender("0.0.0.0", 8005)
reciever = networkSend.FileReciever()

def recieve(stream):
    print(stream.read())
    reciever.cleanup()

reciever.run(8001, recieve)
for x in range(10):
    sender.sendFile("/home/kevin/Pictures/archlinuxlogo.png")
sender.cleanup()
