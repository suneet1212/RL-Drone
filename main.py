import sys
import os
import threading

from ctypes import *

####### 
# Add the local coppeliasim directory to the path. Also need to change directory to it
# If this is not done then libcoppeliasim.so doesn't recognise some libraries.
curr_dir, _ = os.path.split(os.path.abspath(__file__))
# print("main.py: ", __file__)
scenePath = os.path.join(curr_dir, "envScene.ttt")
# sys.path.append(os.path.join(curr_dir, "..", "CoppeliaSimEdu"))
# os.chdir("../CoppeliaSimEdu") # 

from utils.simFunctions import *

options = coppeliasim.cmdopt.parse(args)
appDir = os.path.dirname(args.coppeliasim_library)

# Starts the simulation thread
fastSimulation = False
t = threading.Thread(target=simThreadFunc, args=(appDir, scenePath, fastSimulation))
t.start()
simRunGui(options) # Need to check how to run headless
t.join()

print("success")