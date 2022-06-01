"""
Agent module.
"""

import random
import numpy as np
import chess.engine
from pettingzoo.classic.chess import chess_utils
import torch

from config import CFG
from engine import Engine
import network

class Agent():
    def __init__(self):
        pass

    def move(self, observation, board):
        pass

    def feed(self, sars):
        pass


class DeepKasp_Lin(Agent):
    def __init__(self):
        super().__init__()
        self.net = network.Lin()
        self.opt = torch.optim.Adam(self.net.parameters(), lr=0.0001)


    def feed(self, obs_old, act, rwd, obs_new):
        """
        Learn from a single observation sample.
        """

        obs_old = torch.tensor(obs_old)
        obs_new = torch.tensor(obs_new)

        # We get the network output
        out = self.net(torch.tensor(obs_new))[act]

        # We compute the target
        with torch.no_grad():
            exp = rwd + CFG.gamma * self.net(obs_new).max()

        # Compute the loss
        loss = torch.square(exp - out)

        # Perform a backward propagation.
        self.opt.zero_grad()
        loss.sum().backward()
        self.opt.step()


    def move(self, new_obs, board):
        """
        Run an epsilon-greedy policy for next actino selection.
        """
        # Return random action with probability epsilon
        if random.uniform(0, 1) < CFG.epsilon:
            return board.sample()
        # Else, return action with highest value
        with torch.no_grad():
            val = self.net(torch.tensor(new_obs))
            return torch.argmax(val).numpy()


class DeepKasp_Conv(Agent):
    def __init__(self):
        super().__init__()
        self.net = network.Conv()
        self.opt = torch.optim.Adam(self.net.parameters(), lr=0.0001)


    def feed(self, obs_old, act, rwd, obs_new):
        """
        Learn from a single observation sample.
        """

        print(obs_old)
        print(obs_new)
        exit()

        obs_old = torch.tensor(obs_old)
        obs_new = torch.tensor(obs_new)



        # We get the network output
        out = self.net(torch.tensor(obs_new))[act]
        # print(out)

        # We compute the target
        with torch.no_grad():
            exp = rwd + CFG.gamma * self.net(obs_new).max()

        # Compute the loss
        loss = torch.square(exp - out)

        # Perform a backward propagation.
        self.opt.zero_grad()
        loss.sum().backward()
        self.opt.step()


    def move(self, new_obs, board):
        """
        Run an epsilon-greedy policy for next actino selection.
        """
        # Return random action with probability epsilon
        if random.uniform(0, 1) < CFG.epsilon:
            return random.choice(new_obs["action_mask"])
        # Else, return action with highest value

        with torch.no_grad():
            val = self.net(torch.tensor(new_obs['observation']).type(torch.FloatTensor))
            print(val)
            #print(val.shape)
            valid_actions = torch.tensor(np.squeeze(np.argwhere(new_obs['action_mask'] == 1).T, axis=0))
            print(valid_actions)
            #print(new_obs['action_mask'])
            valid_q = torch.index_select(val, 0, valid_actions)
            print(valid_q)
            best_q = torch.argmax(valid_q).numpy()
            print(best_q)
            #print(valid_actions[best_q].numpy())
            #exit()
            return valid_actions[best_q]


class RandomA(Agent):
    def __init__(self):
        super().__init__()

    def move(self, observation, board):
        print("Random Move")
        return random.choice(np.flatnonzero(observation['action_mask']))


class StockFish(Agent):
    def __init__(self):
        super().__init__()
        self.engine = Engine().engine
        self.time_to_play = CFG.time_to_play

    @staticmethod
    def move_to_act(move):
        """
        Convert a string-like move to an action.
        """
        x, y = chess_utils.square_to_coord(move.from_square)
        panel = chess_utils.get_move_plane(move)
        return (x * 8 + y) * 73 + panel

    def move(self, observation, board):
        if board.turn == False:
            board = board.mirror()
        SF_move = self.engine.play(board=board,
                                   limit=chess.engine.Limit(time=self.time_to_play),
                                   info=chess.engine.Info(1)
                                   )
        print("Stockfish Engine Move: ", SF_move.move)
        return StockFish.move_to_act(SF_move.move)
