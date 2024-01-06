import os

## Tried to start the simulator with this script but sim is not recognized in this

# On importing util.simFunctions, it will change the curr directory,
# so get the curr directory before importing
curr_dir, _ = os.path.split(os.path.abspath(__file__))
scenePath = os.path.join(curr_dir, "envScene.ttt")

from utils.simFunctions import *

# Starts the simulation thread
fastSimulation = False # True => doesn't render the changes in the simulator
initializeSim(scenePath, fastSimulation)
print("success")