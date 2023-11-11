import os
from model import *
import pandas as pd
import torch
import numpy as np

assert os.path.exists('../../personal/python-relay-ceg5205/model/model_demo.pt'), 'train the model first'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

# load model
input_size = 9
hidden_size = 64
num_layers = 2
num_classes = 2
model = GRUModel(input_size, hidden_size, num_layers, num_classes)
model.load_state_dict(torch.load('../../personal/python-relay-ceg5205/model/model_demo.pt', map_location=torch.device('cpu')))
model.to(device)
model.eval()

# load data
file_name = 'data_input_example.csv'
raw_data = pd.read_csv(file_name)
raw_data_np = raw_data.to_numpy()
print(raw_data_np.shape)
if raw_data_np.shape[0] > 149:
    raw_data_np = raw_data_np[:149, :]

input_data = torch.from_numpy(raw_data_np).unsqueeze(0).to(device)

# predict
output = model(input_data.float())
_, predicted = torch.max(output.data, 1)
print(predicted.item())  # 0: RaiseArm, 1: Others
