import os

curr_dir, _ = os.path.split(os.path.abspath(__file__))
print(curr_dir)

# Import necessary coppeliasim libraries
import coppeliasim.cmdopt
parser = argparse.ArgumentParser(description='CoppeliaSim client.')
coppeliasim.cmdopt.add(parser, __file__)
args = parser.parse_args()
builtins.coppeliasim_library = args.coppeliasim_library

from drone.envs.env import DroneEnv

import coppeliasim.cmdopt
parser = argparse.ArgumentParser(description='CoppeliaSim client.')
coppeliasim.cmdopt.add(parser, __file__)
args = parser.parse_args()
builtins.coppeliasim_library = args.coppeliasim_library
scenePath = os.path.join(curr_dir, "envScene.ttt")

env = DroneEnv(scenePath)
