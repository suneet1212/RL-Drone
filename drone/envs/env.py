import gymnasium as gym
from gymnasium import spaces
from utils.simFunctions import *
import numpy as np

import time

class DroneEnv(gym.Env):
    def __init__(self, scenePath, fastSim = True) -> None:
        super().__init__()

        # playSim(scenePath, fastSim)

        # TODO: Fix the observation space
        low = -1*np.ones(10)
        high = np.ones(10)
        self.observation_space = spaces.Box(low, high)

        actionLow = -1*np.ones(4)
        actionHigh = np.ones(4)
        self.action_space = spaces.Box(actionLow, actionHigh)

        initializeSim(scenePath, fastSim)
        # initializeSim(scenePath, fastSim)
        print("Simulation has been initialized")
        self.droneHandle = sim.getObject("/Quadcopter")
        self.targetHandle = sim.getObject("/target")


        for i in range(10):
            self.reset()
            time.sleep(5)

        deInitializeSim()
            

    def reset(self):
        # TODO: Check how to use random seed
        # TODO: Reset all the variables required
        sim.setObjectPosition(self.droneHandle, np.random.rand(3))
        sim.setObjectPosition(self.targetHandle, np.random.rand(3))

    def isDone(self):
        pass
    
    def reward(self):
        pass

    def step(self, action):
        pass
