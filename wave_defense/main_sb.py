import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from envs.wave_defense import WaveDefenseTabular

# Parallel environments
env = WaveDefenseTabular()
#env = make_vec_env(env, n_envs=4)

model = PPO("MlpPolicy", env, tensorboard_log="./logs/ppo_tabular_tensorboard/")
model.learn(total_timesteps=25000, tb_log_name="ppo_tabular_local")
model.save("ppo_tabular_wave_defense")

