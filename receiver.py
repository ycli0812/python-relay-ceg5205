import multiprocessing
import os
import time

import TestClient
import RelayServer
import socket
import keyboard
from utils import proc_print


def receive(q):
    if q is None:
        proc_print('This function must be run in a sub-process and require a Queue.')
        return

    # create server and wait for connection
    relay = RelayServer.RelayServer(host='127.0.0.1', port=5000)
    relay.accept()

    # ready to receive
    buffer = ''
    left_bracket_detected = False
    right_bracket_detected = False
    while True:
        res = relay.recv(1).decode('utf-8')
        if res != '':
            buffer += res
            if res == '[':
                left_bracket_detected = True
            if res == ']':
                right_bracket_detected = True
            if left_bracket_detected and right_bracket_detected:
                frame = None
                # try to parse data
                try:
                    frame = eval(buffer)
                except Exception as e:
                    proc_print('Invalid data.', e)
                proc_print(frame)
                q.put(frame)
                # clear
                left_bracket_detected = False
                right_bracket_detected = False
                buffer = ''
