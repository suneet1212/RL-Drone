import os
import sys
from ctypes import *
import builtins
import argparse
import threading
from pathlib import Path
from typing import Any
import copy

# Add the coppeliasim directory to path (for imports), 
# also change directory to coppeliasim directory 
# to help recognize the simulator files (.so or .dll)
curr_dir, _ = os.path.split(os.path.abspath(__file__))

# if os.path.dirname(os.getcwd()) != "CoppeliaSimEdu":
coppeliaPath = Path(os.path.join(curr_dir, "..", "..", "CoppeliaSimEdu")).resolve()
sys.path.append(str(coppeliaPath))
os.chdir(coppeliaPath) 

# Import necessary coppeliasim libraries
import coppeliasim.cmdopt
parser = argparse.ArgumentParser(description='CoppeliaSim client.')

# libcoppeliaSim.so is only in linux, but it would not matter. 
# It gets replaced in the .add function
coppeliasim.cmdopt.add(parser, os.path.join(str(coppeliaPath), 'libcoppeliaSim.so'))
args = parser.parse_args()
builtins.coppeliasim_library = args.coppeliasim_library
from coppeliasim.lib import *
import coppeliasim.bridge

options = coppeliasim.cmdopt.parse(args)
appDir = os.path.dirname(args.coppeliasim_library)

class SimWrapper():

    def __init__(self, sim = None):
        self.sim = sim

    def simStart(self):
        ''' 
            Starts the simulation
        '''
        if self.sim.getSimulationState() == self.sim.simulation_stopped:
            self.sim.startSimulation()

    def simStep(self):
        ''' 
            Increments the time of the simulator by 0.05 simulation seconds
        '''
        if self.sim.getSimulationState() != self.sim.simulation_stopped:
            t = self.sim.getSimulationTime()
            while t == self.sim.getSimulationTime():
                simLoop(None, 0)

    def simStop(self):
        '''
            Ends the simulation
        '''
        while self.sim.getSimulationState() != self.sim.simulation_stopped:
            self.sim.stopSimulation()
            simLoop(None, 0)

    def simThreadFunc(self, scenePath, fastSimulation):
        '''
            This is the function which starts coppeliasim simulator.\n
            Need to call this from a thread, check startThread
        '''
        simInitialize(c_char_p(appDir.encode('utf-8')), 0)

        coppeliasim.bridge.load()

        # fetch CoppeliaSim API sim-namespace functions:
        # global sim
        self.sim = coppeliasim.bridge.require('sim')
        self.sim.setBoolParam(self.sim.boolparam_display_enabled, not fastSimulation)
        v = self.sim.getInt32Param(self.sim.intparam_program_full_version)
        version = '.'.join(str(v // 100**(3-i) % 100) for i in range(4))
        self.sim.loadScene(scenePath)
        print('CoppeliaSim version is:', version)

        # To set the amount of time the simulator is running
        self.simStart()
        droneHandle = self.sim.getObject("/Quadcopter")
        targetHandle = self.sim.getObject("/target")
        print(f"Target Position is : {self.sim.getObjectPosition(targetHandle)}")
        for i in range(500):
            t = self.sim.getSimulationTime()
            pos = self.sim.getObjectPosition(droneHandle)
            print(f'Simulation time: {t:.2f} [s] and drone position at {pos}')
            self.simStep()
        self.simStop()
        simDeinitialize()
        
        # example: simply run CoppeliaSim (runs until the simulator is closed)
        # while not simGetExitRequest():
        #     simLoop(None, 0)
        # simDeinitialize()

    def playSim(self, scenePath, fastSimulation):
        '''
            Starts the simulator

            scenePath: Path to coppeliasim scene which is to be loaded \n
            fastSimulation: If true then don't render the changes in gui
        '''
        t = threading.Thread(target=self.simThreadFunc, args=(scenePath, fastSimulation))
        t.start()
        simRunGui(options) # Need to check how to run headless
        t.join()
        print("Done")

    def simThreadFuncStart(self, scenePath, fastSimulation):
        simInitialize(c_char_p(appDir.encode('utf-8')), 0)
        coppeliasim.bridge.load()

        # fetch CoppeliaSim API sim-namespace functions:
        # global sim
        self.sim = coppeliasim.bridge.require('sim')
        self.sim.setBoolParam(self.sim.boolparam_display_enabled, not fastSimulation)
        v = self.sim.getInt32Param(self.sim.intparam_program_full_version)
        version = '.'.join(str(v // 100**(3-i) % 100) for i in range(4))
        self.sim.loadScene(scenePath)
        self.simStart()
        self.simStep()
        # sim_copy = copy.deepcopy(sim)
        # queue.put(sim)
        print('CoppeliaSim version is:', version)

    def initializeSim(self, scenePath, fastSimulation):
        print("Initializing")
        t = threading.Thread(target=self.simThreadFuncStart, args=(scenePath, fastSimulation))
        t.start()
        simRunGui(options) # Need to check how to run headless
        t.join()

    def deInitializeSim(self):
        print("De Initializing Simulator. Bye")
        self.simStop()
        simDeinitialize()
        