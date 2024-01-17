import gymnasium as gym
from gymnasium import spaces
from utils.simFunctions import *
import numpy as np

import time

# TODO: type cast lists to np arrays

class DroneEnv(gym.Env):
    def __init__(self, scenePath, fastSim = True) -> None:
        super().__init__()

        # playSim(scenePath, fastSim)

        # Observation space
        # 15 dimensional: position, velocity, acceleration, 
        # angular displacement (euler angles), angular velocity

        # Actions
        # 4 Thrust values of the motors [0, 1]^4

        # Reward function:
        # Rt = max(0, 1 - |x - xg|) - C_theta* |theta| - C_omega * |omega|
        

        # TODO: set right values for low and high
        low = -1*np.ones(15)
        high = np.ones(15)
        self.observation_space = spaces.Box(low, high)

        actionLow = np.zeros(4)
        actionHigh = np.ones(4)
        self.action_space = spaces.Box(actionLow, actionHigh)

        initializeSim(scenePath, fastSim)
        # initializeSim(scenePath, fastSim)
        print("Simulation has been initialized")
        self.droneHandle = sim.getObject("/Quadcopter")
        self.targetHandle = sim.getObject("/target")

        self.propellerHandle0 = sim.getObject("/Quadcopter/joint")
        self.propellerHandle1 = sim.getObject("/Quadcopter/propeller[1]/joint")
        self.propellerHandle2 = sim.getObject("/Quadcopter/propeller[2]/joint")
        self.propellerHandle3 = sim.getObject("/Quadcopter/propeller[3]/joint")

        # TODO: set this properly
        self.maxPropellerThrust = 100

        
        # initializing self.varibles using function
        self.get_obs()

        for i in range(10):
            self.reset()
            time.sleep(5)

        deInitializeSim()
            
    def reset(self):
        # TODO: Check how to use random seed
        # TODO: Reset all the variables required
        sim.setObjectPosition(self.droneHandle, np.random.rand(3))
        sim.setObjectPosition(self.targetHandle, np.random.rand(3))
    
    def step(self, action):

        # Playing out the action
        # TODO: play out the action

        # setting the propeller thrusts
        sim.setJointTargetVelocity(self.propellerHandle0, action[0] * self.maxPropellerThrust, motionParams = None)
        sim.setJointTargetVelocity(self.propellerHandle1, action[1] * self.maxPropellerThrust, motionParams = None)
        sim.setJointTargetVelocity(self.propellerHandle2, action[2] * self.maxPropellerThrust, motionParams = None)
        sim.setJointTargetVelocity(self.propellerHandle3, action[3] * self.maxPropellerThrust, motionParams = None)

        # getting observations
        self.get_obs()
        
        # An episode is done iff the agent has reached the target
        self.get_terminated()
        self.get_reward()

        self.time_limit = 600
        self.X_min = -1000
        self.X_max = 1000
        self.Y_min = -1000
        self.Y_max = 1000
        self.Z_min = -1000
        self.Z_max = 1000

        self.C_theta = 100
        self.C_omega = 100

        self.get_truncated()

        self.info = None

        # if self.render_mode == "human":
        #     self._render_frame()


        return self.observation, self.reward, self.terminated, self.truncated, self.info
    
    def get_obs(self):
        self.agent_location = sim.getObjectPosition(self.droneHandle, relativeToObjectHandle = sim.handle_world)
        self.euler_angles = sim.getObjectOrientation(self.droneHandle, relativeToObjectHandle = sim.handle_world)
        self.target_location = sim.getObjectPosition(self.targetHandle, relativeToObjectHandle = sim.handle_world)
        self.linear_velocity, self.angular_velocity = sim.getObjectVelocity(self.droneHandle)
        self.linear_acceleration = self.compute_acc()
        self.observation = self.agent_location + self.linear_velocity + self.linear_acceleration + self.euler_angles + self.angular_velocity

    def compute_acc(self):
        acc = (self.linear_velocity - self.prev_linear_velocity)/sim.getSimulationTimeStep()
        self.prev_linear_velocity = self.linear_velocity
        return acc
    
    def get_terminated(self):
        # TODO: set a small range of allowed error
        self.terminated = np.array_equal(self.agent_location, self.target_location)

    def get_reward(self):
        self.reward = max(0, 1 - np.linalg.norm(self.agent_location - self.target_location)) - self.C_theta * np.linalg.norm(self.euler_angles) - self.C_omega * np.linalg.norm(self.angular_velocity)
    
    def get_truncated(self):
        # TODO: check units of returned simulation time and make appropriate changes
        self.truncated =  not (self.X_min <= self.agent_location[0] <= self.X_max and self.Y_min <= self.agent_location[1] <= self.Y_max and self.Z_min <= self.agent_location[2] <= self.Z_max and sim.getSimulationTime() < self.time_limit)
        


