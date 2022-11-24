import gym
import WaveDefense
from envs.wave_defense_tabular import WaveDefenseTabular
from envs.wave_defense import WaveDefense
import matplotlib.pyplot as plt
from IPython import embed

#env = WaveDefenseTabular(seed = 200)
env = gym.make("WaveDefense-v1")
env.seed(50)

obs = env.reset()
done = False
steps = 0


while not done:
    steps+=1
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()

print(steps)
