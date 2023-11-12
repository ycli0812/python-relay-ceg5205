import multiprocessing
import os
import time

import TestClient
import RelayServer
import socket

# import keyboard
from receiver import receive
from sender import send
import random
from utils import proc_print


# relay = None


# def handle_keyboard(ev):
#     print(ev.scan_code, ev.name)
#     relay.send('j')


if __name__ == '__main__':
    # random change
    proc_print('This is main process')
    queue = multiprocessing.Queue()
    server_port = 7777
    sender_port = 8888
    p_test_receiver = multiprocessing.Process(target=receive, args=(queue, server_port))
    p_test_sender = multiprocessing.Process(target=send, args=(queue, ))

    p_test_receiver.start()
    p_test_sender.start()

    time.sleep(1)
    test_sender = RelayServer.RelayServer(host='127.0.0.1', port=6666)
    try:
        test_sender.connect(host='127.0.0.1', port=server_port)
    except Exception as e:
        proc_print('Connect failed')
        p_test_receiver.kill()
        exit(1)

    while True:
        # generate 9 float numbers
        random_list = []
        for i in range(9):
            random_number = random.random() - 0.5
            random_list.append(random_number)
        test_sender.send(str(random_list))
        # time.sleep(1)


    # keyboard.on_press(handle_keyboard)
    # keyboard.wait()
