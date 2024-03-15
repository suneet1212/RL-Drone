import gymnasium as gym
from gymnasium import spaces
from utils.simFunctions import *
import numpy as np
from queue import Queue
import time
import copy

# queue = Queue(1)

# TODO: num_envs is hardcoded as one. Fix for vectorization

class DroneEnv(gym.Env):
    def __init__(self, sim, scenePath, fastSim = True) -> None:
        super().__init__()
        self.num_envs = 1

        # playSim(scenePath, fastSim)
        self.simWrapper = SimWrapper(sim)
        # TODO: Fix the observation space
        low = -1*np.ones(18)
        high = np.ones(18)
        self.observation_space = spaces.Box(low, high)


        self.actionStep = 1

        self.numActions = 7
        self.action_space = spaces.Discrete(self.numActions)

        self.time_limit = 1000
        self.X_min = -2
        self.X_max = 2
        self.Y_min = -2
        self.Y_max = 2
        self.Z_min = 0.2
        self.Z_max = 3

        self.pos_min = np.array([self.X_min, self.Y_min, self.Z_min])
        self.pos_max = np.array([self.X_max, self.Y_max, self.Z_max])

        self.C_theta = 100
        self.C_omega = 100

        # sim = queue.get()
        # simStart()
        # simStep()
        self.sim = sim
        print("Trying to get the object handles")
        self.droneHandle = sim.getObject("/Quadcopter")
        self.targetHandle = sim.getObject("/target")
        self.droneToTargetDistance = self.computeDistance(self.droneHandle, self.targetHandle)
        self.prevDroneToTargetDistance = self.droneToTargetDistance
        print(f"Drone Handle: {self.droneHandle} and Target Handle: {self.targetHandle}")

        self.propellerHandle0 = self.sim.getObject("/Quadcopter/joint")
        self.propellerHandle1 = self.sim.getObject("/Quadcopter/propeller[1]/joint")
        self.propellerHandle2 = self.sim.getObject("/Quadcopter/propeller[2]/joint")
        self.propellerHandle3 = self.sim.getObject("/Quadcopter/propeller[3]/joint")

        self.prev_linear_velocity = np.zeros(3)

        self.scriptHandle = self.sim.getScript(self.sim.scripttype_childscript, self.droneHandle)

        print(self.propellerHandle0, self.propellerHandle1, self.propellerHandle2, self.propellerHandle3)

        self.maxPropellerThrust = 10

        self.state,  = self.reset()


    def reset(self, seed=0):
        # TODO: Check how to use random seed
        # TODO: Reset all the variables required
        print("Resetting")
        dronePos = np.random.rand(3)*(self.pos_max-self.pos_min) + self.pos_min
        targetPos = np.random.rand(3)*(self.pos_max-self.pos_min) + self.pos_min

        self.sim.setObjectPosition(self.droneHandle, list(dronePos))
        self.sim.setObjectPosition(self.targetHandle, list(targetPos))
        
        state = self.get_obs()
        return state

    
    def get_reward(self):
        reward = 0
        # a positive reward if the distance to the target is reduced, otherwise a negative reward
        self.prevDroneToTargetDistance = self.DroneToTargetDistance
        self.droneToTargetDistance = self.computeDistance(self.droneHandle, self.targetHandle)
        if(self.droneToTargetDistance < self.prevDroneToTargetDistance):
            reward = 10
        elif(self.droneToTargetDistance > self.prevDroneToTargetDistance):
            reward = -10
        else:
            reward = 0
        return reward

        
        # reward = 100*np.expand_dims(max(0, 1 - np.linalg.norm(self.agent_location - self.target_location)) - self.C_theta * np.linalg.norm(self.euler_angles) - self.C_omega * np.linalg.norm(self.angular_velocity), 0)
        # if self.truncated:
        #    reward -= 10000
        #else:
        #    reward += 10000
        # if self.terminated:
        #    reward += 1000000
        # return reward

    def computeDistance(self, handle1, handle2):
        location1 = self.sim.getObjectPosition(handle1)
        location2 = self.sim.getObjectPosition(handle2)
        
        location1np = np.array(location1)
        location2np = np.array(location2)
        
        dis = np.linalg.norm(location1np - location2np)
        return dis
    	    	
    def get_obs(self):
        self.agent_location = np.array(self.sim.getObjectPosition(self.droneHandle))
        self.euler_angles = np.array(self.sim.getObjectOrientation(self.droneHandle))
        self.target_location = np.array(self.sim.getObjectPosition(self.targetHandle))
        self.linear_velocity, self.angular_velocity = np.array(self.sim.getObjectVelocity(self.droneHandle))
        self.linear_acceleration = self.compute_acc()
        observation = np.concatenate((self.agent_location, self.linear_velocity, self.linear_acceleration, self.euler_angles, self.angular_velocity, self.target_location))
        self.observation = observation.reshape((self.num_envs, -1))

        print("agent location: ", self.agent_location)
        # print("euler angles: ", self.euler_angles)
        # print("target location: ", self.target_location)
        # print("linear vel: ", self.linear_velocity)
        # print("angular vel: ", self.angular_velocity)
        # print("observation", self.observation)
        return self.observation

    def compute_acc(self):
        acc = (self.linear_velocity - self.prev_linear_velocity)/self.sim.getSimulationTimeStep()
        self.prev_linear_velocity = self.linear_velocity
        return acc
    
    def get_terminated(self):
        return True if( np.linalg.norm(self.agent_location - self.target_location) < 0.1) or () else False

    def get_truncated(self):
        return not (self.X_min <= self.agent_location[0] <= self.X_max and self.Y_min <= self.agent_location[1] <= self.Y_max and self.Z_min <= self.agent_location[2] <= self.Z_max and self.sim.getSimulationTime() < self.time_limit)
    
    def _get_info(self):
        return [{"distance": np.linalg.norm(self.agent_location - self.target_location, ord=1)}]

    def step(self, action):
        # Playing out the action
        # print("Starting a step")
        # setting the propeller thrusts
        # print("Set Joint velocity")
        # action = np.squeeze(action)
        # self.sim.callScriptFunction("handlePropeller", self.scriptHandle, 1, action[0] * self.maxPropellerThrust)
        # self.sim.callScriptFunction("handlePropeller", self.scriptHandle, 2, action[1] * self.maxPropellerThrust)
        # self.sim.callScriptFunction("handlePropeller", self.scriptHandle, 3, action[2] * self.maxPropellerThrust)
        # self.sim.callScriptFunction("handlePropeller", self.scriptHandle, 4, action[3] * self.maxPropellerThrust)
        
        # action is in range 0 to 6: one step in 3*2 directions and one hovering action
        
        position = self.sim.getObjectPosition(self.droneHandle)
        if(action == 0):
            position[0] += self.actionStep
        elif(action == 1):
            position[0] -= self.actionStep
        elif(action == 2):
            position[1] += self.actionStep
        elif(action == 3):
            position[1] -= self.actionStep
        elif(action == 4):
            position[2] += self.actionStep
        elif(action == 5):
            position[2] -= self.actionStep
        elif(action == 6):
            pass
        else:
            print("not an accepted action")
            
        # playing out the action
        
        self.sim.setObjectPosition(self.droneHandle, position)
        
        self.simWrapper.simStep()
        time.sleep(0.05)
        # print("finished step")
        # getting observations
        self.get_obs()
        
        # An episode is done iff the agent has reached the target
        self.terminated = self.get_terminated()

        self.truncated = self.get_truncated()
        reward = self.get_reward()

        # print(truncated, " & ", terminated, "&", (terminated or truncated))

        self.info = self._get_info()

        # if self.render_mode == "human":
        #     self._render_frame()

        return self.observation, reward, np.expand_dims(self.terminated or self.truncated, axis=0), self.info

