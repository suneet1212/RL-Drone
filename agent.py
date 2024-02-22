from typing import Dict, Type
from stable_baselines3.common.buffers import RolloutBuffer
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.type_aliases import Schedule
import torch
# from drone.envs.env import DroneEnv
# from stable_baselines3.common.policies import MlpPolicy
from stable_baselines3 import PPO
from stable_baselines3.common.utils import safe_mean
import os
import time
import sys

from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()
device = 'cuda' if torch.cuda.is_available() else 'cpu'

################## HYPERPARAMTERS #####################
NUM_EPISODES = 1000
LR = 0.0005
GAMMA = 0.99
#######################################################

class Agent(PPO):
    def __init__(self, env, modelPath:str = None) -> None:
        super().__init__("MlpPolicy", env, verbose=1, tensorboard_log="./runs")
        self.env = env
        if modelPath:
            model = PPO.load(modelPath)
        
        self.state = self.env.reset()

    def train(self):
        self.learn(100, log_interval=1)

    # def main(self):
    #     model = PPO1(MlpPolicy, self.env, verbose=1)
    #     model.learn(total_timesteps=25000)
    #     model.save("ppo1_cartpole")

    #     del model # remove to demonstrate saving and loading

    #     model = PPO1.load("ppo1_cartpole")

    #     obs = env.reset()
    #     while True:
    #         action, _states = model.predict(obs)
    #         obs, rewards, dones, info = env.step(action)
    #         env.render()
