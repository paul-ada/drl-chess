"""
Game Module.
"""

from pettingzoo.classic import chess_v5

import numpy as np

from agent import Agent, StockFish
from config import Config


class Game():
    # Add attributes depending on type of players

    def __init__(self, players):
        self.game_env = chess_v5.env()
        self.chess_env = self.game_env.env.env.env.env
        self.game_env.reset()
        self.players = players

    def board(self):
        return self.chess_env.board

    def play(self):
        history = []

        player_idx = 0
        for _ in self.game_env.agent_iter(max_iter=Config().max_iters):
            observation, reward, done, info = self.game_env.last()

            move = self.players[player_idx].move(observation, game.board())
            self.game_env.step(move)

            print(game.board())
            print()
            history.append((observation, reward))

            player_idx = 1 - player_idx


# players = tuple of 2 players: random / stockfish / deepk / human
players = (StockFish(), Agent())
game = Game(players)

game.play()






# # Encoding function
# import hashlib
# def encode_state(observation):
#     # encode observation as bytes
#     obs_bytes = str(observation).encode('utf-8')
#     # create md5 hash
#     m = hashlib.md5(obs_bytes)
#     # return hash as hex digest
#     state = m.hexdigest()
#     return(state)
## To encode endgame board state (to add in game function):
            # state = encode_state(self.game_env.render(mode = 'ansi'))
            # print(state)
