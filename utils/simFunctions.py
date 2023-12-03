# from coppeliaSim import *
import coppeliasim.bridge
from coppeliasim.lib import *
import os
import sys
from ctypes import *

curr_dir = os.path.abspath(__file__)
sys.path.append(os.path.join(curr_dir, "../..", "CoppeliaSim_Edu"))
os.chdir("../CoppeliaSim_Edu") # 

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
        print(f'Simulation time: {t:.2f} [s] (simulation running synchronously to client, i.e. stepped)')
        simStep()
    simStop()
    simDeinitialize()
    
    # example: simply run CoppeliaSim (runs until the simulator is closed)
    # while not simGetExitRequest():
    #     simLoop(None, 0)
    # simDeinitialize()
