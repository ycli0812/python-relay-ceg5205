import ctypes
import math
import socket
import time
import os
import multiprocessing
from utils import proc_print


class RelayServer:
    def __init__(self, host='127.0.0.1', port=15001):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.connected = False

    def connect(self, host, port):
        if not self.connected:
            self.socket.connect((host, port))
            self.connected = True
            proc_print('Connected to %s:%d' % (host, port))
        else:
            proc_print('Already connected, can not connect again.')

    def accept(self):
        if not self.connected:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            proc_print('Start listening on %d' % self.port)
            c, addr = self.socket.accept()
            self.socket = c
            self.connected = True
            proc_print('Client connected:', addr)
        else:
            proc_print('Already connected, can not accept connections.')

    def send(self, text):
        if self.socket is not None:
            return self.socket.send(text.encode('utf-8'))
        else:
            proc_print('Not connected, can not send.')
            return -1

    def recv(self, length=100):
        if self.connected:
            return self.socket.recv(length)
        else:
            proc_print('Not connected, can not receive.')
            return -1
