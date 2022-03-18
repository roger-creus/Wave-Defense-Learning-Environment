import gym
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from wave_defense.envs.wave_defense_tabular import WaveDefenseTabular

# Parallel environments
env = make_vec_env("WaveDefense-v0", n_envs=16)

policy_kwargs = dict(net_arch=[256, 256, dict(vf=[128], pi=[128])])

model = PPO("CnnPolicy", env, batch_size=64, policy_kwargs=policy_kwargs, tensorboard_log="./logs/ppo_visual/")
model.learn(total_timesteps=10000000, tb_log_name="ppo_visual_10M_64env_2048steps_256bs")
model.save("./models/ppo_visual_10M_64env_2048steps_256bs")

