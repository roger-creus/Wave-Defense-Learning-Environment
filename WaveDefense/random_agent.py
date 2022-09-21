import gym
from envs.wave_defense_tabular import WaveDefenseTabular

env = WaveDefenseTabular()

obs = env.reset()
done = False
steps = 0
while not done:
    steps+=1
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
    print(reward)

print(steps)