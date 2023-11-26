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
curr_dir = os.getcwd()
sys.path.append(os.path.join(curr_dir, "..", "CoppeliaSim_Edu_V4_6_0_rev2_Ubuntu20_04"))
os.chdir("../CoppeliaSim_Edu_V4_6_0_rev2_Ubuntu20_04") # 

# Import necessary coppeliasim libraries
import coppeliasim.cmdopt
parser = argparse.ArgumentParser(description='CoppeliaSim client.')
coppeliasim.cmdopt.add(parser, __file__)
args = parser.parse_args()
builtins.coppeliasim_library = args.coppeliasim_library

# from coppeliaSim import *
import coppeliasim.bridge
from coppeliasim.lib import *

def simStart():
    if sim.getSimulationState() == sim.simulation_stopped:
        sim.startSimulation()

def simStep():
    if sim.getSimulationState() != sim.simulation_stopped:
        t = sim.getSimulationTime()
        while t == sim.getSimulationTime():
            simLoop(None, 0)

def simStop():
    while sim.getSimulationState() != sim.simulation_stopped:
        sim.stopSimulation()
        simLoop(None, 0)

def simThreadFunc(appDir):
    '''
        This is the function which starts coppeliasim simulator.
    '''
    simInitialize(c_char_p(appDir.encode('utf-8')), 0)

    coppeliasim.bridge.load()

    # fetch CoppeliaSim API sim-namespace functions:
    global sim
    sim = coppeliasim.bridge.require('sim')

    v = sim.getInt32Param(sim.intparam_program_full_version)
    version = '.'.join(str(v // 100**(3-i) % 100) for i in range(4))
    sim.loadScene(os.path.join(curr_dir, "envScene.ttt"))
    print('CoppeliaSim version is:', version)

    # To set the amount of time the simulator is running
    simStart()
    for i in range(1000):
        t = sim.getSimulationTime()
        print(f'Simulation time: {t:.2f} [s] (simulation running synchronously to client, i.e. stepped)')
        simStep()
    simStop()
    simDeinitialize()
    
    # example: simply run CoppeliaSim (runs until the simulator is closed)
    # while not simGetExitRequest():
    #     simLoop(None, 0)
    # simDeinitialize()


options = coppeliasim.cmdopt.parse(args)

appDir = os.path.dirname(args.coppeliasim_library)

# Starts the simulation thread
t = threading.Thread(target=simThreadFunc, args=(appDir,))
t.start()
simRunGui(options) # Need to check how to run headless
t.join()


print("success")