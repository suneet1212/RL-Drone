import os
import threading
import time
import numpy as np
from agent import Agent

# On importing DroneEnv, it will change the curr directory,
# so get the curr directory before importing
curr_dir, _ = os.path.split(os.path.abspath(__file__))
scenePath = os.path.join(curr_dir, "envScene1.ttt")

from utils.simFunctions import SimWrapper
from drone.envs.env import DroneEnv
## Final script to train the agent

# from drone.envs.env import ThreadEnv
# from drone.envs.env import ThreadSim

class Simulator(SimWrapper):
    def __init__(self) -> None:
        super().__init__()

    # def initializeSim(self, scenePath, fastSimulation):
    #     print("Initializing")
    #     threadSim = ThreadSim(scenePath, False)
    #     threadSim.start()

    #     time.sleep(20)
    #     threadEnv = ThreadEnv(self.sim, scenePath, False)
    #     threadEnv.start()
    #     t = threading.Thread(target=self.simThreadFuncStart, args=(scenePath, fastSimulation))
    #     t.start()
    #     simRunGui(options) # Need to check how to run headless
    #     t.join()


    # def deInitializeSim(self):
    #     self.simStop()
    #     simDeinitialize()
        
    def start(self, scenePath, fastSim):
        threadSim = ThreadSim(self, scenePath, fastSim)
        threadSim.start()
        time.sleep(25)

        threadEnv = ThreadEnv(self.sim, scenePath, fastSim)
        threadEnv.start()

        
class ThreadSim(threading.Thread):
    def __init__(self, simWrapper: Simulator, scenePath, fastSimulation) -> None:
        threading.Thread.__init__(self)
        self.scenePath = scenePath
        self.fastSimulation = fastSimulation
        self.simWrapper = simWrapper

    def run(self):
        print("On Sim thread, starting sim")
        self.simWrapper.initializeSim(self.scenePath, self.fastSimulation)

    # def getSim(self):
    #     return self.simWrapper.sim    

class ThreadEnv(threading.Thread):
    def __init__(self, sim, scenePath, fastSimulation):
        threading.Thread.__init__(self)
        self.scenePath = scenePath
        self.fastSimulation = fastSimulation
        self.sim = sim

    def run(self):
        # print("On Env thread, sleeping for 25 sec")
        print("On Env thread, starting env")
        self.env = DroneEnv(self.sim, self.scenePath, self.fastSimulation)
        
        agent = Agent(self.env)
        agent.train()
        # for i in range(100):
        #     action = list(np.random.rand(4))
        #     obs, reward, terminated, truncated, info = self.env.step(action)

        #     print(obs, reward, terminated, truncated)

        # self.env.simWrapper.deInitializeSim()


    def getEnv(self):
        return self.env

if __name__ == "__main__":
    simulator = Simulator()
    simulator.start(scenePath, False)

