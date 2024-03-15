def step(self, action):

   # takes action as argument
   # returns    observation,
   #		reward,
   #		terminated,
   #		truncated,
   #		info,
   #		done

   # Action: Thrust of the four motors [0, 1]^4
   # Observation: 15 dimensional vector:
   #		position,
   #		velocity,
   #		acceleration,
   #		angular displacement,
   #		angular velocity
   		

    
    
    # logic to act out the action
    pass
    
    # termination
    terminated = np.array_equal(self._agent_location, self._target_location)
    
    # truncation logic
    pass
    
    # done logic
    pass
    
    # reward logic
    reward = max(0, 1 - np.norm(self._agent_location, self._target_location)) - self.C_theta* np.norm(self._angular_displacement) - self.C_omega* np.norm(self.angular_velocity)

    # get observations
    observation = self._get_obs()
    
    info = self._get_info()

    
    if self.render_mode == "human":
        self._render_frame()

    return observation, reward, terminated, truncated, info, done

