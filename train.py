import os

curr_dir, _ = os.path.split(os.path.abspath(__file__))
print(curr_dir)

from drone.envs.env import DroneEnv

scenePath = os.path.join(curr_dir, "envScene.ttt")

env = DroneEnv(scenePath, False)
