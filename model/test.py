import os
from model import *
import pandas as pd
import torch
import numpy as np


def load_model(path='model_demo_95.pt'):
    assert os.path.exists(path), 'train the model first'
    # if not os.path.exists(path):
    #     return None, None

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


model, device = load_model()

# load data
# file_name = 'test-data/false/28C4C347-C8E1-4E85-BAF5-95EDE8985944.csv'
# raw_data = pd.read_csv(file_name)
# raw_data_np = raw_data.to_numpy()
# if raw_data_np.shape[0] > 149:
#     raw_data_np = raw_data_np[:149, :]
#
# input_data = torch.from_numpy(raw_data_np).unsqueeze(0).to(device)
#
# # predict
# output = model(input_data.float())
# _, predicted = torch.max(output.data, 1)
# print(predicted.item())  # 0: RaiseArm, 1: Others
