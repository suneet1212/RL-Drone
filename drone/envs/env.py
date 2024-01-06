import gymnasium as gym
from gymnasium import spaces
from utils.simFunctions import *
import numpy as np
from queue import Queue
import time

# queue = Queue(1)

class ThreadSim(threading.Thread):
    def __init__(self, scenePath, fastSimulation) -> None:
        threading.Thread.__init__(self)
        self.scenePath = scenePath
        self.fastSimulation = fastSimulation

    def run(self):
        print("On Sim thread, starting sim")
        initializeSim(self.scenePath, self.fastSimulation)

class ThreadEnv(threading.Thread):
    def __init__(self, scenePath, fastSimulation):
        threading.Thread.__init__(self)
        self.scenePath = scenePath
        self.fastSimulation = fastSimulation

    def run(self):
        print("On Env thread, sleeping for 25 sec")
        time.sleep(25)
        print("On Env thread, done sleeping, starting env")
        self.env = DroneEnv(self.scenePath, self.fastSimulation)

    def getEnv(self):
        return self.env

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

        # sim = queue.get()
        # simStart()
        # simStep()

        self.droneHandle = sim.getObject("/Quadcopter")
        self.targetHandle = sim.getObject("/target")

        for i in range(5):
            self.reset()
            time.sleep(10)

    def reset(self):
        # TODO: Check how to use random seed
        # TODO: Reset all the variables required
        print("Reseting")
        dronePos = np.random.rand(3)
        targetPos = np.random.rand(3)
        print("dronePos = ", dronePos)
        print("targetPos = ", targetPos)

        sim.setObjectPosition(self.droneHandle, dronePos)
        sim.setObjectPosition(self.targetHandle, targetPos)

        print("Actual Drone Pos = ", sim.getObjectPosition(self.droneHandle))
        print("Actual target Pos = ", sim.getObjectPosition(self.targetHandle))

    def isDone(self):
        pass
    
    def reward(self):
        pass

    def step(self, action):
        pass
