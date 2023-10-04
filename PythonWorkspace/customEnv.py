import numpy as np
import gymnasium as gym
from gymnasium import spaces

class GoLeftEnv(gym.Env):
    metadata = {'render_modes': ['console']}

    LEFT = 0
    RIGHT = 1

    def __init__(self, grid_size=10, render_mode = "console"):
        super(GoLeftEnv, self).__init__()
        self.render_mode = render_mode

        # Size of the 1D-grid
        self.grid_size = grid_size
        # Initialize the agent at the right of the grid
        self.agent_pos = grid_size - 1

        # Define action and observation space
        # They must be gym.spaces objects
        n_actions = 2
        self.action_space = spaces.Discrete(n_actions)
        # The observation will be the coordinate of the agent
        # this can be described both by Discrete and Box space
        self.observation_space = spaces.Box(low=0, high=self.grid_size,shape=(1,), dtype = np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
          # Initialize the agent at the right of the grid
        self.agent_pos = self.grid_size - 1
          # here we convert to float32 to make it more general (in case we want to use continuous actions)
        return np.array([self.agent_pos]).astype(np.float32), {}  # empty info dict
        
    def step(self, action):
        if action == self.LEFT:
            self.agent_pos -= 1
        elif action == self.RIGHT:
            self.agent_pos += 1
        else:
            raise ValueError(
            f"Recived invalid action = {action} which is not part of the action space"
            )
        self.agent_pos = np.clip(self.agent_pos, 0,self.grid_size)
        terminated = bool(self.agent_pos == 0)
        truncated = False # see if I can get some sort of time limit in to test

        reward = 1 if self.agent_pos == 0 else 0

        info = {'key1':'Yo this is my first environment'}

        return (
        np.array([self.agent_pos]).astype(np.float32),
        reward,
        terminated, 
        truncated,
        info,
        )
        
    def render(self):
        if self.render_mode == "console":
            print('.'*self.agent_pos, end = "")
            print('X', end = "")
            print('.'*(self.grid_size-self.agent_pos))


    def close(self):
        pass


from stable_baselines3.common.env_checker import check_env

env = GoLeftEnv()

check_env(env, warn = True)

env = GoLeftEnv(grid_size = 10)

obs,_ = env.reset()
env.render()

print(env.observation_space)
print(env.action_space)
print(env.action_space.sample())

GO_LEFT = 0 

n_steps = 20 
for step in range(n_steps):
    print(f"Step: {step + 1}")
    obs, reward, terminated, truncated, info = env.step(GO_LEFT)
    done = terminated or truncated
    print("obs=", obs, "reward=", reward, "done=",done, "info=", info)
    env.render()
    if done:
        print("Goal reached!", "reward=", reward)   
        break


env = GoLeftEnv(grid_size=10)



from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.env_util import make_vec_env

vec_env = make_vec_env(GoLeftEnv, n_envs = 1, env_kwargs = dict(grid_size=10))

model  = A2C("MlpPolicy", vec_env, verbose = 1)

n_steps = 20 
obs = env.reset()

for step in range(n_steps):
    action, _ = model.predict(obs, deterministic = True)
    print(f"Step: {step + 1}")
    print("Action: ", action)
    obs, reward, terminated, truncated, info = env.step(action)
    print('obs=', obs, 'reward=', reward, 'terminated=', terminated, 'truncated=', truncated, 'info=', info)
    env.render()
    if terminated or truncated:
        print("Goal reached!", "reward=", reward)
        break 