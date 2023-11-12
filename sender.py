import numpy as np
import torch
import os
from model.model import GRUModel

from utils import proc_print
from model.test import load_model


def load_model(path='./model/model_demo.pt'):
    assert os.path.exists(path), 'train the model first'

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


def send(q, bind_port=7777, remote_port=8888):
    if q is None:
        proc_print('This function must be run in a sub-process and require a Queue.')
        return

    # load model
    model, device = load_model(path='./model/model_demo.pt')

    # create server and wait for connection
    # TODO: connect to Unity socket
    # relay = RelayServer.RelayServer(host='127.0.0.1', port=bind_port)
    # relay.connect(host='127.0.0.1', port=remote_port)

    buffer = []

    # ready to receive
    while True:
        while not q.empty():
            data = q.get()
            # TODO: store data
            buffer.append(data)
            # TODO: feed data into the model
            if len(buffer) >= 150:
                frame = buffer[-150:]
                feed = torch.from_numpy(np.array(frame)).unsqueeze(0).to(device)
                output = model(feed.float())
                _, predicted = torch.max(output.data, 1)
                buffer = buffer[-150:]
                # TODO: send data to Unity client
                proc_print(predicted.item())
            # proc_print('Sender:', sum(data))
