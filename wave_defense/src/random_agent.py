from wave_defense.envs.wave_defense import WaveDefense
import gym


# EXAMPLE RANDOM AGENT

env = gym.make("WaveDefense-v1")
env.reset()
env.render()
done = False
steps = 0

while done is False:
    steps += 1
    obs, rew, done, info = env.step(env.action_space.sample()) # take a random action
    env.render()
env.close()
print("in " + str(steps) + " steps")