import socket
import struct
import io
import threading

'''
Listen for incoming files from FileSender.
'''
class FileReciever(threading.Thread):
    def __init__(self, port, fileCallbackFn):
        self.port = port
        self.fileCallbackFn = fileCallbackFn
        threading.Thread.__init__(self)
    def run(self):
        try:
            self.gateway = socket.socket()
            self.gateway.bind(('0.0.0.0', self.port))
            self.gateway.listen(0)
            print("Listening on port {}".format(self.port))
            self.keepListening = True
            self.connection = self.gateway.accept()[0].makefile('rb')
            while self.keepListening:
                file_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]

                if not file_len:
                    break

                file_stream = io.BytesIO()
                file_stream.write(self.connection.read(file_len))
                file_stream.seek(0)

                print("Received file from server")
                self.fileCallbackFn(file_stream)
        finally:
            self.kill()
    def kill(self):
        self.keepListening = False
        self.gateway.close()

'''
Send a file over the network.
'''
class FileSender:
    '''
    Host: The String IP address to send to
    Port: The int port to send to
    '''
    def __init__(self, host, port):
        self.gateway = socket.socket()
        self.gateway.connect((host, port))
        self.connection = self.gateway.makefile('wb')
        print("Connection to recipient established")
    
    '''
    Send a file
    filePath: String location of the file on disk
    '''
    def sendFile(self, filePath):
        fileBytes = open(filePath, 'rb')
        data = fileBytes.read()
        length = fileBytes.tell()

        self.connection.write(struct.pack('<L', length))
        self.connection.flush()
        self.connection.write(data)
        print("Sent file {} to client".format(filePath))
    
    '''
    Clean up after you're done sending files
    '''
    def cleanup(self):
        self.connection.write(struct.pack('<L', 0))
        self.connection.flush()
        self.connection.close()
        self.gateway.close()
