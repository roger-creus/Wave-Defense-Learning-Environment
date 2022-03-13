import gym
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from wave_defense.envs.wave_defense_tabular import WaveDefenseTabular

# Parallel environments
env = make_vec_env("WaveDefense-v1", n_envs=64)

policy_kwargs = dict(activation_fn=torch.nn.ReLU, net_arch=[256, 128, dict(vf=[128], pi=[128])])

model = PPO("MlpPolicy", env, batch_size=256, policy_kwargs=policy_kwargs, tensorboard_log="./logs/ppo_tabular_tensorboard/")
model.learn(total_timesteps=50000000, tb_log_name="ppo_tabular_50M_64env_2048steps_256bs")
model.save("./models/ppo_tabular_50M_64env_2048steps_256bs")

