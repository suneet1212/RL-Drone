import torch
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import VecEnv
from stable_baselines3.dqn import MlpPolicy
device = 'cuda' if torch.cuda.is_available() else 'cpu'

import os
curr_dir, _ = os.path.split(os.path.abspath(__file__))
################## HYPERPARAMTERS #####################
# NUM_EPISODES = 1000
# LR = 0.0005
# GAMMA = 0.99
#######################################################

class Agent(DQN):
    def __init__(self, env, modelPath:str = None) -> None:
        super().__init__(MlpPolicy, env, verbose=1, tensorboard_log="./runs")
        self.env = env
        if modelPath:
            self.set_parameters(modelPath)
        
        x = self.env.reset()
        print(x)

    def train_model(self):
        print(type(self.env))
        print(type(VecEnv))
        print(self.env)
        assert isinstance(self.env, VecEnv), "not a vecEnv"
        self.learn(5000000, log_interval=1, callback=CustomCallBack(self.env))
        self.save(os.path.join(curr_dir, "model/dqn_train_1"))

class CustomCallBack(BaseCallback):
    def __init__(self, env, verbose: int = 0):
        self.env = env
        super().__init__(verbose)

    def _on_rollout_start(self) -> None:
        self.env.reset()

    def _on_step(self) -> bool:
        return super()._on_step()
