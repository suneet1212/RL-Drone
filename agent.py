import torch
from stable_baselines3 import PPO
device = 'cuda' if torch.cuda.is_available() else 'cpu'

import os
curr_dir, _ = os.path.split(os.path.abspath(__file__))
################## HYPERPARAMTERS #####################
# NUM_EPISODES = 1000
# LR = 0.0005
# GAMMA = 0.99
#######################################################

class Agent(PPO):
    def __init__(self, env, modelPath:str = None) -> None:
        super().__init__("MlpPolicy", env, verbose=1, tensorboard_log="./runs", n_steps=128)
        self.env = env
        if modelPath:
            self.set_parameters(modelPath)
        
        x = self.env.reset()
        print(x)

    def train_model(self):
        self.learn(500, log_interval=1)
        self.save(os.path.join(curr_dir, "model/ppo_test"))
        print("Saved to ", os.path.join(curr_dir, "model/ppo_test"))
