import gym
from gym import spaces
import threading
from utils.simFunctions import *

class DroneEnv(gym.Env):
    def __init__(self, scenePath, fastSim = True) -> None:
        super().__init__()

        startThread(scenePath, fastSim)
