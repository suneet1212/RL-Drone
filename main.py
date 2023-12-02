import sys
import os
import builtins
import argparse
import threading

from pathlib import Path
from ctypes import *

####### 
# Add the local coppeliasim directory to the path. Also need to change directory to it
# If this is not done then libcoppeliasim.so doesn't recognise some libraries.
curr_dir, _ = os.path.split(os.path.abspath(__file__))

scenePath = os.path.join(curr_dir, "envScene.ttt")
sys.path.append(os.path.join(curr_dir, "..", "CoppeliaSim_Edu_V4_6_0_rev2_Ubuntu20_04"))
os.chdir("../CoppeliaSim_Edu_V4_6_0_rev2_Ubuntu20_04") # 

# Import necessary coppeliasim libraries
import coppeliasim.cmdopt
parser = argparse.ArgumentParser(description='CoppeliaSim client.')
coppeliasim.cmdopt.add(parser, __file__)
args = parser.parse_args()
builtins.coppeliasim_library = args.coppeliasim_library

from utils.simFunctions import *

options = coppeliasim.cmdopt.parse(args)
appDir = os.path.dirname(args.coppeliasim_library)

# Starts the simulation thread
t = threading.Thread(target=simThreadFunc, args=(appDir, scenePath))
t.start()
simRunGui(options) # Need to check how to run headless
t.join()


print("success")