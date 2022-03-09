import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from envs.wave_defense import WaveDefenseTabular

env = WaveDefenseTabular()

model = PPO.load("ppo_tabular_wave_defense.zip")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()