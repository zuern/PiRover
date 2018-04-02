#!/bin/python

import io
import socket
import struct

'''
This class is responsible for listening to and parsing responses from the server
'''
class ControlStream:
    def initialize(self, port):
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0',port))
        self.socket.listen(0)
        print("Controller listening for server responses on port {}".format(port))
    def get_server_response(self):
        # Accept a single connection and make a file-like object out of it
        connection = self.socket.accept()[0].makefile('rb')
        try:
            while True:
                print("Connected to server stream")
        finally:
            connection.close()
            self.socket.close()
