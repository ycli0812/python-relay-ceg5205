import torch

class GRUModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(GRUModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes

        self.gru1 = torch.nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.gru2 = torch.nn.GRU(hidden_size, hidden_size, num_layers, batch_first=True)
        self.ac = torch.nn.ReLU()
        self.fc1 = torch.nn.Linear(hidden_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, hidden_size)
        self.fc3 = torch.nn.Linear(hidden_size, num_classes)


    def forward(self, x):

        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        h1 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, h0 = self.gru1(x, h0)
        out, h1 = self.gru2(out, h1)
        out = self.ac(out)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.fc3(out[:, -1, :])

        return out