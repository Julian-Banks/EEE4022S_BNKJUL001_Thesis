import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.logger import Video

environment_name = 'CartPole-v1'
env = gym.make(environment_name, render_mode = "rgb_array")


episodes = 5
for episode in range (1,episodes+1):
  state=env.reset()
  terminated = False
  truncated = False
  score=0

  while not terminated and not truncated:
    action = env.action_space.sample()
    n_state,reward,terminated,truncated,info = env.step(action)
    env.render() 
    score += reward
  print('Episode:{} Score: {}'.format(episode, score))
env.close()

while not terminated and not truncated:
    action = env.action_space.sample()
    n_state,reward,terminated,truncated,info = env.step(action)
    env.render("human") 
    score += reward
print('Episode:{} Score: {}'.format(1, score))

model = A2C("MlpPolicy", env, verbose =1)
model.learn(total_timesteps=10_000)
vec_env = model.get_env()
obs = vec_env.reset()
for i in range (1000):
  action,_state = model.predict(obs,deterministic = True)
  obs,reward,done,info = vec_env.step(action)
  vec_env.render("human")