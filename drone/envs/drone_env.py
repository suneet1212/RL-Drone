# python
import gym
from gym import spaces
from pyrep import PyRep
from pyrep.objects.shape import Shape
from pyrep.objects.object import Object
import numpy as np
import os
from os.path import join, abspath, dirname

from scipy.spatial.distance import euclidean
from drone.envs import sim
import random

MAX_PROPELLER_MOTOR_VEL = 10

class Drone(gym.Env):
    metadata = {}

    def __init__(self, scene_file, headless:bool) -> None:
        super().__init__()

        self.isCrashed = False
        self.goalReached = False

        # Observation Space = [droneX,droneY,droneZ,droneYaw,dronePitch,droneRoll,targetX,targetY,targetZ,targetYaw,targetPitch,targetRoll]
        self.obsLow = np.array([-2.5,-2.5,0,-np.pi,0,-np.pi,-2.5,-2.5,0,-np.pi,0,-np.pi])
        self.obsHigh = np.array([2.5,2.5,5,np.pi,np.pi,np.pi,2.5,2.5,10,np.pi,np.pi,np.pi])
        self.observation_space = spaces.Box(low=np.float32(self.obsLow),high=np.float32(self.obsHigh))
        
        actLow = np.array([-1,-1,-1,-1])
        actHigh = np.array([1,1,1,1])
        self.action_space = spaces.Box(low=np.float32(actLow),high=np.float32(actHigh))

        self.pr = PyRep()
        self.pr.launch(scene_file, headless=headless)
        self.pr.start()

        self.droneObject = self.load_drone()
        self.targetObject = self.load_target()

        sim.simxFinish(-1) # just in case, close all opened connections
        self.clientID=sim.simxStart("127.0.0.1",19997,True,True,5000,5) # start a connection
        if self.clientID==-1:
            raise Exception("Could not connect to remote API server")
        print("Connected to remote API server")
        
        val1 = Object.exists("Quadricopter")
        if(not val1):
            raise Exception("Quadricopter model could not be found. Model not loaded properly")
        
        val2 = Object.exists("Quadricopter_target")
        if(not val2):
            raise Exception("Quadricopter target could not be found. Check if the scene has a quadricopter target in it.")
        
        val1 = Object.exists("Quadricopter_propeller_respondable1")
        if(not val1):
            raise Exception("Quadricopter model could not be found. Model not loaded properly")
        else:
            print("Object exists, hope to connect to script")
        
        self.quadHandle = self.droneObject.get_handle()
        self.targetHandle = self.targetObject.get_handle()


        
    def shutdown(self):
        self.pr.stop()
        self.pr.shutdown()

    def load_drone(self):
        return self.pr.import_model(join(dirname(abspath(__file__)),
                  'quadricopterModel.ttm'))

    def load_target(self):
        return self.pr.import_model(join(dirname(abspath(__file__)),
                  'quadricopterTarget.ttm'))

    def reset(self):
        # for obj in self.droneObjectList:
        #     obj.reset_dynamic_object()
        # self.pr.set_configuration_tree(self.initConfig)
        self.isCrashed = False
        self.goalReached = False
        print("old position",self.droneObject.get_position())
        
        new_drone_pos = self.random_trio(self.obsLow[0:3],self.obsHigh[0:3])
        new_drone_ori = self.random_trio(self.obsLow[3:6],self.obsHigh[3:6])
        self.droneObject.set_position(new_drone_pos,None,True)
        self.droneObject.set_orientation(new_drone_ori,None,True)

        print("new position",self.droneObject.get_position())

        new_target_pos = self.random_trio(self.obsLow[6:9],self.obsHigh[6:9])
        new_target_ori = self.random_trio(self.obsLow[9:12],self.obsHigh[9:12])
        self.targetObject.set_position(new_target_pos,None,True)
        self.targetObject.set_orientation(new_target_ori,None,True)

        new_state = np.concatenate((new_drone_pos,new_drone_ori,new_target_pos,new_target_ori))
        self.state = new_state

        return new_state

    def step(self,action):
        # self.pr.script_call()

        # For making it fast check this, not sure if it is useful
        # https://forum.coppeliarobotics.com/viewtopic.php?t=5419
        sim.simxCallScriptFunction(self.clientID, "Quadricopter_propeller_respondable1",
                                    sim.sim_scripttype_childscript,"sysCall_actuation",inputInts=[] ,inputFloats=[action[0]],
                                    inputStrings=[],inputBuffer=bytearray(),operationMode=sim.simx_opmode_blocking)
        sim.simxCallScriptFunction(self.clientID, "Quadricopter_propeller_respondable2",
                                    sim.sim_scripttype_childscript,"sysCall_actuation",inputInts=[] ,inputFloats=[action[1]],
                                    inputStrings=[],inputBuffer=bytearray(),operationMode=sim.simx_opmode_blocking)
        sim.simxCallScriptFunction(self.clientID, "Quadricopter_propeller_respondable3",
                                    sim.sim_scripttype_childscript,"sysCall_actuation",inputInts=[] ,inputFloats=[action[2]],
                                    inputStrings=[],inputBuffer=bytearray(),operationMode=sim.simx_opmode_blocking)
        sim.simxCallScriptFunction(self.clientID, "Quadricopter_propeller_respondable4",
                                    sim.sim_scripttype_childscript,"sysCall_actuation",inputInts=[] ,inputFloats=[action[3]],
                                    inputStrings=[],inputBuffer=bytearray(),operationMode=sim.simx_opmode_blocking)
        self.pr.step()
        dronePos = self.droneObject.get_position()
        droneOrien = self.droneObject.get_orientation()
        targetPos = self.targetObject.get_position()
        targetOrien = self.targetObject.get_orientation()
        
        self.state = np.concatenate((dronePos,droneOrien,targetPos,targetOrien))
        done = self.isDone()
        reward = self.computeReward()
        return self.state, reward, done, {}
        
    
    def isDone(self):
        if(self.state[2] <= 0.02):
            self.isCrashed = True
            return True
        self.distance = euclidean(self.state[0:6],self.state[6:12])
        if(self.distance < 0.05):
            self.goalReached = True
            return True
        return False

    def computeReward(self):
        reward = 0
        reward -= euclidean(self.state[0:6],self.state[6:12])
        if(self.isCrashed):
            reward -= 10
        elif(self.goalReached):
            reward += 10
        return reward
        
    @staticmethod
    def random_trio(low,high):
        assert(len(low) == 3)
        assert(len(high) == 3)
        trio = [0,0,0]
        for i in range(3):
            trio[i] = random.uniform(low[i],high[i])
        return trio
