import multiprocessing
import os
import time

import TestClient
import RelayServer
import socket
import keyboard
from receiver import receive
import random
from utils import proc_print


relay = None


def handle_keyboard(ev):
    print(ev.scan_code, ev.name)
    relay.send('j')


if __name__ == '__main__':
    proc_print('This is main process')
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=receive, args=(queue, ))
    p.start()
    time.sleep(1)
    test_sender = RelayServer.RelayServer(host='127.0.0.1', port=6000)
    try:
        test_sender.connect(host='127.0.0.1', port=5000)
    except Exception as e:
        proc_print('Connect failed')
        p.kill()
        exit(1)

    while True:
        # generate 9 float numbers
        random_list = []
        for i in range(9):
            random_number = random.random() - 0.5
            random_list.append(random_number)
        test_sender.send(str(random_list))
        time.sleep(1)
    p.join()



    # keyboard.on_press(handle_keyboard)
    # keyboard.wait()
