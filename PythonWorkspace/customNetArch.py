
import gymnasium as gym
import torch as th

from stable_baselines3 import PPO

policy_kwargs = dict(activation_fn=th.nn.ReLU,net_arch=[dict(pi=[32,32],vf=[32,32])])

model = PPO("MlpPolicy", 'CartPole-v1', policy_kwargs=policy_kwargs, verbose=1)
print(model.policy)

model2 = PPO("MlpPolicy", 'CartPole-v1', verbose=1)
print(model2.policy)
'''
env = model.get_env()
model.learn(total_timesteps=20_000)

model.save("ppo_cartpole_custom_arch")

del model

model = PPO.load("ppo_cartpole_custom_arch", env=env)
print(model.policy)

'''