import os


def proc_print(str, *args):
    print('[% 6d]' % os.getpid(), str, *args)

