import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from wave_defense.envs.wave_defense_tabular import WaveDefenseTabular

env = WaveDefenseTabular()

model = PPO.load("./models/ppo_tabular_50M_64env_2048steps_256bs.zip")

obs = env.reset()
reward = 0
done = False
i = 0
while not done:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    reward += rewards
    env.render()
print(reward)
