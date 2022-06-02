""""
Neural Network
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


# Version Paul

class Conv(nn.Module):
    """
    CNN DQN
    """

    def __init__(self):
        super(Conv, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(8, 111, 8, 8),
            nn.ReLU(),
            #nn.Conv2d(111, 25, 3, 1),
            #nn.ReLU(),
            # n.Linear(1443, 1),
            # nn.Linear(4672,1),
          )

        self.linear = nn.Sequential(
            nn.Linear(1443, 2048),
            nn.Linear(2048, 4672),
          )

    def forward(self, x):
        y = torch.flatten(self.conv(x))
        return self.linear(y)


class Lin(nn.Module):
    """
    A simple Deep Q-Network with 3 linear layers.
    """
    def __init__(self):
        super(Lin, self).__init__()

        self.net = nn.Sequential(
            nn.Flatten(1, 1),
            nn.Linear(111, 20),
            nn.ReLU(inplace=True),
            nn.Linear(20, 20),
            nn.ReLU(inplace=True),
            nn.Linear(20, 4672),
            nn.ReLU(inplace=True)
            )

    def forward(self, x):
        return self.net(x)