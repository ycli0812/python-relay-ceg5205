import multiprocessing
import socket
import random
import time

from receiver import receive
from utils import proc_print
import RelayServer


if __name__ == '__main__':
    server_port = 7777
    ip_addr = socket.gethostbyname(socket.gethostname())
    proc_print('This is main process')
    proc_print('IP address: %s, port: %d' % (ip_addr, server_port))
    queue = multiprocessing.Queue()

    p_test_receiver = multiprocessing.Process(target=receive, args=(queue, server_port))
    p_test_receiver.start()
    time.sleep(1)

    # --- comment this if there is a real device ---
    c = RelayServer.RelayServer('127.0.0.1', 9999)
    c.connect('127.0.0.1', server_port)
    for i in range(99):
        random_list = []
        for j in range(9):
            random_number = random.random() - 0.5
            random_list.append(random_number)
        c.send(str(random_list))
    # --- end ---

    p_test_receiver.join()
