# python
from drone.envs.drone_env import Drone
import time
import numpy as np
from os.path import dirname, join, abspath

SCENE_FILE = join(dirname(abspath(__file__)),
                  'drone/envs/env_scene.ttt')

env = Drone(SCENE_FILE,False)
print(env.observation_space.shape)
print(env.action_space)
print("target ", env.targetHandle)
# print("Sleeping for 10sec")
# time.sleep(10)
print("Start -> ")

for i in range(1000):
    ns, r, done, info = env.step(5*np.random.rand(4))
    print(ns[0:3], " reward = ",r,"done = ",done)
    if(done):
        env.reset()

state = env.reset()
print(state)
print("Reset Done")
# time.sleep(10)

env.shutdown()
print("Done")