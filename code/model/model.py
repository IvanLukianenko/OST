import torch
from torch import nn


class GRU(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(GRU, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.randn(self.num_layers, x.shape[0],  self.hidden_dim)
        out, (hn) = self.gru(x, h0)
        out = self.fc(out[:, -1, :])
        out = torch.sigmoid(out)
        return out


def train(model, train_dl, num_epochs, opt, loss_fn):
    losses = []
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    for epoch in range(num_epochs):
        model.train()
        for i, (xb, yb) in enumerate(train_dl):
            xb, yb = xb.to(device), yb.to(device)
            pred = model(xb)
            opt.zero_grad()
            loss = loss_fn(pred, yb)
            loss.backward()
            opt.step()

        losses.append(loss.detach().item())
        print(f'Epoch: {epoch} | Loss: {loss.detach().item()}')
    return losses


def test(model,
         test_dl: torch.utils.data.DataLoader):
    r"""

    Args:
        model:
        test_dl:
        metrics:
        metrics_funcs:

    Returns:
        predictions: list of predictions for testing data
        true_values: list of true labels for testing data

    Testing cycle for HailNet

    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    with torch.no_grad():
        model.eval()
        predictions = []
        true_values = []
        for xt, yt in test_dl:
            xt, yt = xt.to(device), yt.to(device)
            predictions.append(model(xt))
            true_values.append(yt)
    return predictions, true_values
