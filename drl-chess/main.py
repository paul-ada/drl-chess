import math
import os
import matplotlib.pyplot as plt

import game
import agent
from config import CFG
from data import DAT
import utils



def stop_eng():
    if CFG.engine is not None:
        CFG.engine.stop_engine()


def main(agt=None):

    CFG.init(net_type='conv', debug=False, reward_SF=True,  small_obs=True,
             learning_rate = 0.1)

    if agt is None:
        agt = (agent.DeepK(), agent.StockFish())
    env = game.Game(agt)

    while True:

        for n in range(50):
            CFG.epsilon = math.exp(-CFG.epsilon_decay * n)
            env.play()

        print(f"loss : {DAT.stats['loss'][-1]}")
        eval(agt[0])


def gen_data():

    DAT.reset(True)
    CFG.init(net_type="conv", debug=False, reward_SF=False)

    agt = (agent.ObservationGenerator(), agent.ObservationGenerator())
    env = game.Game(agt)
    obs = []

    for _ in range(50):
        env.play()

        obs += agt[0].obs
        obs += agt[1].obs

        agt[0].obs.clear()
        agt[1].obs.clear()

    utils.to_disk(obs) # Push obs batch to ../data/


def load_agent():

    CFG.init(net_type="conv", debug=False, reward_SF=False, small_obs=False,   # Check reward SF dependencies
             depth=1, learning_rate = 0.1)

    agt = agent.DeepK()
    dir = os.path.join(os.path.dirname(__file__), f'../data')
    for idx, dir in enumerate(utils.get_files(dir)):
        print(dir)
        for obs in utils.from_disk(dir):
            agt.obs.append(obs)
            if len(agt.obs) >= CFG.batch_size:
                agt.learn()
                agt.obs = []
        print(f"Training loss: {DAT.stats['loss'][-1]}")
        if idx % 3 == 0:
            eval(agt)

    return agt


def eval(agt, n_eval=10):
    DAT.eval_idx += 1
    CFG.train = False
    agt.net.eval()
    env = game.Game((agt, agent.StockFish()))

    for _ in range(n_eval):
        env.play()
    winner = DAT.stats['outcome'][-n_eval:]
    wins = winner.count('1-0')
    draw = winner.count('1/2-1/2')
    print(f'{DAT.eval_idx}: Wins {wins}, Losses {5 - wins - draw}, Draws {draw} \n')
    if wins > 0:
        print("KASPAROV!!!!!!! \n \n \n")

    agt.net.train()
    CFG.train=True
    agt.obs = []




# while True:
#     gen_data()

# for _ in range(10):
#     gen_data()
# stop_eng()

load_agent()

# main()

# utils.plot_stats(DAT)
