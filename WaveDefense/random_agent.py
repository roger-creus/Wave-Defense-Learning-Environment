import gym
import WaveDefense

env = gym.make("WaveDefense-v0")
env.seed(50)

obs = env.reset()
done = False

while not done:
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    obs = env.render()

