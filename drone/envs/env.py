import gymnasium as gym
from gymnasium import spaces
from utils.simFunctions import *
import numpy as np
from queue import Queue
import time

# queue = Queue(1)

# TODO: ThreadEnv needs DroneEnv class which needs simFunctions.
# Need to define another class which will import all 3 of these classes
# and it can start ThreadEnv object.

class DroneEnv(gym.Env):
    def __init__(self, sim, scenePath, fastSim = True) -> None:
        super().__init__()

        # playSim(scenePath, fastSim)

        # TODO: Fix the observation space
        low = -1*np.ones(10)
        high = np.ones(10)
        self.observation_space = spaces.Box(low, high)

        actionLow = -1*np.ones(4)
        actionHigh = np.ones(4)
        self.action_space = spaces.Box(actionLow, actionHigh)

        # sim = queue.get()
        # simStart()
        # simStep()
        self.sim = sim
        print("Trying to get the object handles")
        self.droneHandle = sim.getObject("/Quadcopter")
        self.targetHandle = sim.getObject("/target")
        print(f"Drone Handle: {self.droneHandle} and Target Handle: {self.targetHandle}")

        # for i in range(5):
        #     self.reset()
        #     time.sleep(10)


    def reset(self):
        # TODO: Check how to use random seed
        # TODO: Reset all the variables required
        print("Reseting")
        dronePos = np.random.rand(3)
        targetPos = np.random.rand(3)
        print("dronePos = ", dronePos)
        print("targetPos = ", targetPos)

        self.sim.setObjectPosition(self.droneHandle, dronePos)
        self.sim.setObjectPosition(self.targetHandle, targetPos)

        print("Actual Drone Pos = ", self.sim.getObjectPosition(self.droneHandle))
        print("Actual target Pos = ", self.sim.getObjectPosition(self.targetHandle))

    def isDone(self):
        pass
    
    def reward(self):
        pass

    def step(self, action):
        pass
