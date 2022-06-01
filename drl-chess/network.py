""""
Neural Network
"""

import torch.nn as nn
import torch.nn.functional as F


# Version Paul

class Net(nn.Module):
    """
    CNN DQN
    """

    def __init__(self):
        super(Net, self).__init__()

        self.net = nn.Sequential(
          nn.Conv2d(111, 50, 3, 2),
          nn.ReLU(),
          nn.Conv2d(50, 25, 3, 2),
          nn.ReLU(),
          nn.Linear(4672,1),
          )

    def forward(self, x):
        return self.net(x)


class DQN(nn.Module):
    """
    A simple Deep Q-Network with 3 linear layers.
    """

    def __init__(self, x_dim, y_dim):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(x_dim, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, y_dim),
            nn.ReLU(inplace=True),
        )

    def forward(self, obs):
        return self.net(obs)
