import os
import sys
from ctypes import *
import builtins
import argparse
import threading

curr_dir, _ = os.path.split(os.path.abspath(__file__))

if os.path.dirname(os.getcwd()) != "CoppeliaSimEdu":
    sys.path.append(os.path.join(curr_dir, "..", "..", "CoppeliaSimEdu"))
    os.chdir(os.path.join("..", "CoppeliaSimEdu")) 

# Import necessary coppeliasim libraries
import coppeliasim.cmdopt
parser = argparse.ArgumentParser(description='CoppeliaSim client.')
coppeliasim.cmdopt.add(parser, os.path.basename(__file__))
args = parser.parse_args()
builtins.coppeliasim_library = args.coppeliasim_library
from coppeliaSim import *

from coppeliasim.lib import *
import coppeliasim.bridge

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

def simThreadFunc(appDir, scenePath, fastSimulation):
    '''
        This is the function which starts coppeliasim simulator.
    '''
    simInitialize(c_char_p(appDir.encode('utf-8')), 0)

    coppeliasim.bridge.load()

    # fetch CoppeliaSim API sim-namespace functions:
    global sim
    sim = coppeliasim.bridge.require('sim')
    sim.setBoolParam(sim.boolparam_display_enabled, not fastSimulation)
    v = sim.getInt32Param(sim.intparam_program_full_version)
    version = '.'.join(str(v // 100**(3-i) % 100) for i in range(4))
    sim.loadScene(scenePath)
    print('CoppeliaSim version is:', version)

    # To set the amount of time the simulator is running
    simStart()
    for i in range(500):
        t = sim.getSimulationTime()
        droneHandle = sim.getObject("/Quadcopter")
        pos = sim.getObjectPosition(droneHandle)
        print(f'Simulation time: {t:.2f} [s] and drone position at {pos}')
        simStep()
    simStop()
    simDeinitialize()
    
    # example: simply run CoppeliaSim (runs until the simulator is closed)
    # while not simGetExitRequest():
    #     simLoop(None, 0)
    # simDeinitialize()

def startThread(scenePath, fastSimulation):
    options = coppeliasim.cmdopt.parse(args)
    appDir = os.path.dirname(args.coppeliasim_library)
    t = threading.Thread(target=simThreadFunc, args=(appDir, scenePath, fastSimulation))
    t.start()
    simRunGui(options) # Need to check how to run headless
    t.join()