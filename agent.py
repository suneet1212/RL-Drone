import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback

from stable_baselines3.common.type_aliases import MaybeCallback
from stable_baselines3.common.utils import safe_mean
import datetime
import time
import sys
from typing import TypeVar
AgentSelf = TypeVar("AgentSelf", bound="Agent")


device = 'cuda' if torch.cuda.is_available() else 'cpu'

import os
curr_dir, _ = os.path.split(os.path.abspath(__file__))
################## HYPERPARAMTERS #####################
# NUM_EPISODES = 1000
# LR = 0.0005
# GAMMA = 0.99
#######################################################

class Agent(PPO):
    def __init__(self, env, modelPath:str = None) -> None:
        super().__init__("MlpPolicy", env, verbose=1, tensorboard_log="./runs")
        self.env = env
        if modelPath:
            self.set_parameters(modelPath)
        
        x = self.env.reset()
        print(x)

        # starting date to append to the name of saved models
        now = datetime.datetime.now()
        self.dt = now.strftime("%Y%m%d%H%M%S")


    def train_model(self):
        self.learn(9000, log_interval=1, callback=CustomCallBack(self.env), save_intervals = 2)
        path = os.path.join(curr_dir, "model/ppo_train_expt")
        path = os.path.join(path, self.dt, "final")
        self.save(path)

    # save intermediate model functionality has to be added. Since changing the
    # content of library file is not recommended, will add learn method here, copy paste cod from
    # parent class and make the changes
        

    
    def learn(
        self: AgentSelf,
        total_timesteps: int,
        callback: MaybeCallback = None,
        log_interval: int = 1,
        tb_log_name: str = "Agent",
        reset_num_timesteps: bool = True,
        progress_bar: bool = False,
        save_intervals: int = 200000,
    ) -> AgentSelf:
        iteration = 0

        # new addition
        i = 0

        total_timesteps, callback = self._setup_learn(
            total_timesteps,
            callback,
            reset_num_timesteps,
            tb_log_name,
            progress_bar,
        )

        callback.on_training_start(locals(), globals())

        assert self.env is not None

        while self.num_timesteps < total_timesteps:
            print("time step number ", self.num_timesteps)
            continue_training = self.collect_rollouts(self.env, callback, self.rollout_buffer, n_rollout_steps=self.n_steps)

            if not continue_training:
                break

            iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            # Display training infos
            if log_interval is not None and iteration % log_interval == 0:
                assert self.ep_info_buffer is not None
                time_elapsed = max((time.time_ns() - self.start_time) / 1e9, sys.float_info.epsilon)
                fps = int((self.num_timesteps - self._num_timesteps_at_start) / time_elapsed)
                self.logger.record("time/iterations", iteration, exclude="tensorboard")
                if len(self.ep_info_buffer) > 0 and len(self.ep_info_buffer[0]) > 0:
                    self.logger.record("rollout/ep_rew_mean", safe_mean([ep_info["r"] for ep_info in self.ep_info_buffer]))
                    self.logger.record("rollout/ep_len_mean", safe_mean([ep_info["l"] for ep_info in self.ep_info_buffer]))
                self.logger.record("time/fps", fps)
                self.logger.record("time/time_elapsed", int(time_elapsed), exclude="tensorboard")
                self.logger.record("time/total_timesteps", self.num_timesteps, exclude="tensorboard")
                self.logger.dump(step=self.num_timesteps)

            self.train()
            ## new addition
            #### Number of timesteps at the end of train may not be an exact multiple of save_intervals
            if int(self.num_timesteps/save_intervals) > i:
                print("current i :", i)
                i = self.num_timesteps//save_intervals
                save_idx = str(i)
                path = os.path.join(curr_dir, "model/ppo_train_expt")
                path = os.path.join(path, self.dt, save_idx)
                self.save(path)



        callback.on_training_end()

        return self

        

class CustomCallBack(BaseCallback):
    def __init__(self, env, verbose: int = 0):
        self.env = env
        super().__init__(verbose)

    def _on_rollout_start(self) -> None:
        self.env.reset()

    def _on_step(self) -> bool:
        return super()._on_step()