from importlib import metadata
import gym
from pyrep import PyRep
from pyrep.objects.shape import Shape
from pyrep.objects.object import Object
from pyrep.robots.arms.panda import Panda
from pyrep.const import PrimitiveShape
import numpy as np
from os.path import dirname, join, abspath

from drone.envs import sim

class Propeller():
    def __init__(self, ) -> None:
        