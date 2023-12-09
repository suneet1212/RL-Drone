import gym
from gym import spaces
import threading
from utils.simFunctions import *

# options = coppeliasim.cmdopt.parse(args)
# appDir = os.path.dirname(args.coppeliasim_library)

class DroneEnv(gym.Env):
    def __init__(self, scenePath, fastSim = True) -> None:
        super().__init__()

        startThread()
