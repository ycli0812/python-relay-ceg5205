import math
import socket
import keyboard
import time
import os
import multiprocessing
import random


if __name__ == '__main__':
    c = socket.socket()
    c.bind(('127.0.0.1', 5000))
    c.connect(('127.0.0.1', 6000))
    counter = 0
    while True:
        # generate 9 float numbers
        random_list = []
        for i in range(9):
            # Generate a random float number between 0 and 1
            random_number = random.random() - 0.5
            # Append the random number to the list
            random_list.append(random_number)
        c.send(str(random_list).encode('utf-8'))
        counter += 1
        time.sleep(1)
