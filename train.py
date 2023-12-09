import os

# On importing DroneEnv, it will change the curr directory,
# so get the curr directory before importing
curr_dir, _ = os.path.split(os.path.abspath(__file__))
scenePath = os.path.join(curr_dir, "envScene.ttt")

from drone.envs.env import DroneEnv

env = DroneEnv(scenePath, False)
