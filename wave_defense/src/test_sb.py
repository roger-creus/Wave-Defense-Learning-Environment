import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from wave_defense.envs.wave_defense_tabular import WaveDefenseTabular

env = WaveDefenseTabular()

model = PPO.load("./models/ppo_tabular_500M_4env.zip")

obs = env.reset()
reward = 0
done = False
while not done:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    print(rewards)
    reward += rewards
    env.render()

print(reward)