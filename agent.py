import torch
from stable_baselines3 import PPO
device = 'cuda' if torch.cuda.is_available() else 'cpu'

################## HYPERPARAMTERS #####################
# NUM_EPISODES = 1000
# LR = 0.0005
# GAMMA = 0.99
#######################################################

class Agent(PPO):
    def __init__(self, env, modelPath:str = None) -> None:
        super().__init__("MlpPolicy", env, verbose=1, tensorboard_log="./runs")
        self.env = env
        if modelPath:
            self.set_parameters(modelPath)
        
        x = self.env.reset()
        print(x)

    def train_model(self):
        self.learn(5, log_interval=1)