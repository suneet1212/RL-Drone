import gymnasium as gym
from gymnasium import spaces
from utils.simFunctions import *
import numpy as np
from queue import Queue
import time
import copy

# queue = Queue(1)

# TODO: ThreadEnv needs DroneEnv class which needs simFunctions.
# Need to define another class which will import all 3 of these classes
# and it can start ThreadEnv object.

class DroneEnv(gym.Env):
    def __init__(self, sim, scenePath, fastSim = True) -> None:
        super().__init__()

        # playSim(scenePath, fastSim)
        self.simWrapper = SimWrapper(sim)
        # TODO: Fix the observation space
        low = -1*np.ones(15)
        high = np.ones(15)
        self.observation_space = spaces.Box(low, high)

        actionLow = -1*np.ones(4)
        actionHigh = np.ones(4)
        self.action_space = spaces.Box(actionLow, actionHigh)

        self.time_limit = 600
        self.X_min = -1000
        self.X_max = 1000
        self.Y_min = -1000
        self.Y_max = 1000
        self.Z_min = -1000
        self.Z_max = 1000

        self.C_theta = 100
        self.C_omega = 100

        # sim = queue.get()
        # simStart()
        # simStep()
        self.sim = sim
        print("Trying to get the object handles")
        self.droneHandle = sim.getObject("/Quadcopter")
        self.targetHandle = sim.getObject("/target")
        print(f"Drone Handle: {self.droneHandle} and Target Handle: {self.targetHandle}")

        self.propellerHandle0 = self.sim.getObject("/Quadcopter/joint")
        self.propellerHandle1 = self.sim.getObject("/Quadcopter/propeller[1]/joint")
        self.propellerHandle2 = self.sim.getObject("/Quadcopter/propeller[2]/joint")
        self.propellerHandle3 = self.sim.getObject("/Quadcopter/propeller[3]/joint")

        self.prev_linear_velocity = np.zeros(3)

        print(self.propellerHandle0, self.propellerHandle1, self.propellerHandle2, self.propellerHandle3)

        self.maxPropellerThrust = 100

        self.reset()


        # TODO: Remove this before training
        # self.simWrapper.deInitializeSim()


    def reset(self):
        # TODO: Check how to use random seed
        # TODO: Reset all the variables required
        print("Reseting")
        dronePos = np.random.rand(3)
        targetPos = np.random.rand(3)
        print("dronePos = ", dronePos)
        print("targetPos = ", targetPos)

        self.sim.setObjectPosition(self.droneHandle, list(dronePos))
        self.sim.setObjectPosition(self.targetHandle, list(targetPos))

        self.get_obs()
        print("Actual Drone Pos = ", self.sim.getObjectPosition(self.droneHandle))
        print("Actual target Pos = ", self.sim.getObjectPosition(self.targetHandle))
    
    def get_reward(self):
        return max(0, 1 - np.linalg.norm(self.agent_location - self.target_location)) - self.C_theta * np.linalg.norm(self.euler_angles) - self.C_omega * np.linalg.norm(self.angular_velocity)

    def get_obs(self):
        self.agent_location = np.array(self.sim.getObjectPosition(self.droneHandle))
        self.euler_angles = np.array(self.sim.getObjectOrientation(self.droneHandle))
        self.target_location = np.array(self.sim.getObjectPosition(self.targetHandle))
        self.linear_velocity, self.angular_velocity = np.array(self.sim.getObjectVelocity(self.droneHandle))
        self.linear_acceleration = self.compute_acc()
        self.observation = np.concatenate((self.agent_location, self.linear_velocity, self.linear_acceleration, self.euler_angles, self.angular_velocity))

        print("agent location: ", self.agent_location)
        # print("euler angles: ", self.euler_angles)
        # print("target location: ", self.target_location)
        # print("linear vel: ", self.linear_velocity)
        # print("angular vel: ", self.angular_velocity)
        # print("observation", self.observation)

    def compute_acc(self):
        acc = (self.linear_velocity - self.prev_linear_velocity)/self.sim.getSimulationTimeStep()
        self.prev_linear_velocity = self.linear_velocity
        return acc
    
    def get_terminated(self):
        return True if np.linalg.norm(self.agent_location - self.target_location) < 0.1 else False

    def get_truncated(self):
        return not (self.X_min <= self.agent_location[0] <= self.X_max and self.Y_min <= self.agent_location[1] <= self.Y_max and self.Z_min <= self.agent_location[2] <= self.Z_max and self.sim.getSimulationTime() < self.time_limit)

    def step(self, action):
        # Playing out the action
        # print("Starting a step")
        # setting the propeller thrusts
        self.sim.setJointTargetVelocity(self.propellerHandle0, action[0] * self.maxPropellerThrust, [])
        self.sim.setJointTargetVelocity(self.propellerHandle1, action[1] * self.maxPropellerThrust, [])
        self.sim.setJointTargetVelocity(self.propellerHandle2, action[2] * self.maxPropellerThrust, [])
        self.sim.setJointTargetVelocity(self.propellerHandle3, action[3] * self.maxPropellerThrust, [])
        # print("Set Joint velocity")

        
        self.simWrapper.simStep()
        time.sleep(0.05)
        # print("finished step")
        # getting observations
        self.get_obs()
        
        # An episode is done iff the agent has reached the target
        terminated = self.get_terminated()
        reward = self.get_reward()

        truncated = self.get_truncated()

        self.info = None

        # if self.render_mode == "human":
        #     self._render_frame()

        return self.observation, reward, terminated, truncated, self.info

