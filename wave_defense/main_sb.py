import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from envs.wave_defense import WaveDefense

# Parallel environments
env = WaveDefense()
#env = make_vec_env(env, n_envs=4)

model = PPO("CnnPolicy", env, tensorboard_log="./logs/ppo_tensorboard/")
model.learn(total_timesteps=500000, tb_log_name="ppo_0.1")
model.save("ppo_wave_defense")

