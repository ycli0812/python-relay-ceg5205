import os
from multiprocessing import Lock


def proc_print(*args):
    lock = Lock()
    lock.acquire()
    print('[% 6d]' % os.getpid(), *args)
    lock.release()

