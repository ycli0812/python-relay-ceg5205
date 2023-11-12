import torch

class GRUModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(GRUModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes

        self.gru = torch.nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.ac = torch.nn.ReLU()
        self.fc = torch.nn.Linear(hidden_size, num_classes)

    def forward(self, x):

        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, h0 = self.gru(x, h0)
        out = self.ac(out)

        out = self.fc(out[:, -1, :])
        return out