import multiprocessing
import socket

from receiver import receive
from utils import proc_print


if __name__ == '__main__':
    server_port = 7777
    ip_addr = socket.gethostbyname(socket.gethostname())
    proc_print('This is main process')
    proc_print('IP address: %s, port: %d' % (ip_addr, server_port))
    queue = multiprocessing.Queue()

    p_test_receiver = multiprocessing.Process(target=receive, args=(queue, server_port))

    p_test_receiver.start()

    p_test_receiver.join()

