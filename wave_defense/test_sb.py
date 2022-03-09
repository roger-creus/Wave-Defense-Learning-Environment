import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from wave_defense import WaveDefense

model = PPO.load("ppo_wave_defense")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()