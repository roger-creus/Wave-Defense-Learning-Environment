import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from wave_defense.envs.wave_defense_tabular import WaveDefenseTabular

# Parallel environments
env = make_vec_env("WaveDefense-v1", n_envs=16)

model = PPO("MlpPolicy", env, tensorboard_log="./logs/ppo_tabular_tensorboard/")
model.learn(total_timesteps=10000000, tb_log_name="ppo_tabular_10M_16env")
model.save("./models/ppo_tabular_10M_16env")

