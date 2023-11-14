import math
import time

import numpy as np
import torch
import os
from model.model import GRUModel
import RelayServer

from utils import proc_print


class AcceDetector:
    def __init__(self, threshold=20, cooling_time=500):
        self.counter = 0
        self.detected = False
        self.threshold = threshold
        self.cooling_time = cooling_time
        self.last_acquire_time = 0

    def push(self, detected):
        if self.detected:
            if detected:
                self.counter += 1
            else:
                self.detected = False
                self.counter = 0
        else:
            if detected:
                self.detected = True
                self.counter += 1
            else:
                self.counter += 1

    def get_counter(self):
        return self.counter

    def is_ready(self):
        cur = int(time.time() * 1000)
        if self.detected and self.counter > self.threshold and cur - self.last_acquire_time > self.cooling_time:
            self.last_acquire_time = cur
            return True
        else:
            return False


def load_model(path='model/model_demo_95.pt'):
    assert os.path.exists(path), ('%s not exist, train the model first.' % path)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load model
    input_size = 9
    hidden_size = 64
    num_layers = 2
    num_classes = 2
    model = GRUModel(input_size, hidden_size, num_layers, num_classes)
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.to(device)
    model.eval()
    return model, device


def send(lock, q, bind_port=7777):
    if q is None:
        proc_print('This function must be run in a sub-process and require a Queue.')
        return

    # load model
    model, device = load_model(path='model/model_demo_95.pt')
    proc_print('Model loaded.')

    # create server and wait for connection
    relay = RelayServer.RelayServer(host='127.0.0.1', port=bind_port)
    relay.accept()

    lock.release()

    buffer = []

    detector = AcceDetector(threshold=10, cooling_time=1700)

    # ready to receive
    while True:
        while not q.empty():
            data = q.get()
            buffer.append(data)
            if len(buffer) >= 150:
                # extract last 150 timestamps
                frame = buffer[:150]
                # feed into the model
                feed = torch.from_numpy(np.array(frame)).unsqueeze(0).to(device)
                output = model(feed.float())
                _, predicted = torch.max(output.data, 1)
                # throw away some oldest timestamps
                buffer = buffer[10:]
                # send signal
                detector.push(predicted.item() == 0)
                proc_print(predicted.item())
                if detector.is_ready():
                    proc_print('JUMP!')
                    relay.send('jj')
