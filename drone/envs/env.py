import gym
from gym import spaces

class DroneEnv(gym.Env):
    def __init__(self) -> None:
        super().__init__()

        