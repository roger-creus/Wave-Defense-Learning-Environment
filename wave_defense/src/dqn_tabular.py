import gym
import numpy as np
from wave_defense.envs.wave_defense_tabular import WaveDefenseTabular
from collections import namedtuple
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from torchvision.transforms import ToTensor, Lambda, Normalize
from torchvision import transforms
import wandb
import random
import os
import matplotlib.pyplot as plt
from IPython import embed


os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple(
    'Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQN(nn.Module):
    def __init__(self, inputs, outputs, hidden_size=128):
        super(DQN, self).__init__()

        self.affine1 = nn.Linear(25, 64)
        self.affine2 = nn.Linear(64, 64)
        self.affine3 = nn.Linear(64, 4)

    def forward(self, x):
        x = F.relu(self.affine1(x))
        x = F.relu(self.affine2(x))
        x = self.affine3(x)

        return x

def compute_eps_threshold(step, eps_start, eps_end, eps_decay):
    return eps_end + (eps_start - eps_end) * math.exp(-1. * step / eps_decay)


def select_action(policy, state, eps_greedy_threshold, n_actions):
    # TODO: Select action using an epsilon-greedy strategy
    if random.random() > eps_greedy_threshold:

        with torch.no_grad():
            # t.max(1) will return largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            action = policy(state).max(1)[1].view(1,1)
            
    else:
        action = torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)
    return action

    
def train(policy_net, target_net, optimizer, memory, batch_size, gamma):
    if len(memory) < batch_size:
        return 0
    transitions = memory.sample(batch_size)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(
        tuple(map(lambda s: s is not None, batch.next_state)), 
        device=device, 
        dtype=torch.bool)
    
    non_final_next_states = torch.cat(
        [s for s in batch.next_state if s is not None])
    
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t) for all a, then we select 
    # the columns of actions taken. These are the actions which would've been 
    # taken for each batch state according to policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute Q(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    # Note the call to detach() on Q(s_{t+1}), which prevents gradient flow
    
    next_state_values = torch.zeros(batch_size, device=device)
    
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()

    expected_state_action_values = reward_batch + (gamma*next_state_values)

    # Compute Huber loss between predicted Q values and targets y
    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    # Take an SGD step
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()
    
    
def test(env, policy, render=False):
    state, ep_reward, done = env.reset(), 0, False
    steps = 0
    while not done and steps < hparams["num_steps"]:
        if render:
            env.render()
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        action = select_action(policy_net, state, 0., 1)
        state, reward, done, _ = env.step(action.item())
        ep_reward += reward
        steps += 1
    env.close()
    return ep_reward


hparams = {
    'gamma' : 0.99,             # discount factor
    'log_interval' : 100,        # controls how often we log progress, in episodes
    'episodes': 1000000,          # number of steps to train on
    'num_steps': 100000,
    'batch_size': 128,          # batch size for optimization
    'lr' : 1e-3,                # learning rate
    'eps_start': 1.0,           # initial value for epsilon (in epsilon-greedy)
    'eps_end': 0.1,             # final value for epsilon (in epsilon-greedy)
    'eps_decay': 20000,         # length of epsilon decay, in env steps
    'target_update': 20000,      # how often to update target net, in env steps
    'replay_size': 50000,       # replay memory size
}

# Create environment
env = WaveDefenseTabular()

# Get number of actions from gym action space
n_inputs = env.observation_space.shape[0]
n_actions = env.action_space.n

# Initialize wandb run
wandb.finish() # execute to avoid overlapping runnings (advice: later remove duplicates in wandb)
wandb.init(project="WaveDefenseTabular", config=hparams)

# Initialize policy and target networks
policy_net = DQN(n_inputs, n_actions).to(device)
target_net = DQN(n_inputs, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = torch.optim.Adam(policy_net.parameters(), lr=hparams['lr'])
memory = ReplayMemory(hparams['replay_size'])

step_count = 0
running_reward = 0

episode = 0
best_reward = 0

ep_rew_history = []
i_episode, ep_reward = 0, -float('inf')
while episode < hparams['episodes']:
    # Initialize the environment and state
    state, done = env.reset(), False
    state = torch.from_numpy(state).float().unsqueeze(0).to(device)
    reward_episode = 0
    losses = []
    game_steps = 0
    while not done and game_steps <  hparams['num_steps']:
        # Select an action
        eps_greedy_threshold = compute_eps_threshold(step_count, hparams['eps_start'], hparams['eps_end'], hparams['eps_decay'])
        action = select_action(policy_net, state, eps_greedy_threshold, n_actions)

        # Perform action in env
        next_state, reward, done, _ = env.step(action.item())

        # Bookkeeping
        if done:
            # train() treats states as terminal when next_state is None
            next_state = None
        else:
            next_state = torch.from_numpy(next_state).float().unsqueeze(0).to(device)
        
        reward = torch.tensor([reward], device=device)
        step_count += 1
        game_steps += 1
        
        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Reward episode
        reward_episode += reward.item()

        # Perform one step of the optimization (on the policy network)
        loss = train(policy_net, target_net, optimizer, memory, hparams['batch_size'], hparams['gamma'])
        losses.append(loss)
        # Update the target network, copying all weights and biases in DQN
        if step_count % hparams['target_update'] == 0:
            target_net.load_state_dict(policy_net.state_dict())
    
    i_episode += 1  
    episode =+ 1
    
    running_reward = 0.05 * reward_episode + (1 - 0.05) * running_reward

    if reward_episode > best_reward:
        if not os.path.exists('checkpoints'):
            os.makedirs('checkpoints')
        torch.save(policy_net.state_dict(), f'checkpoints/dqn.pt')
        best_reward = reward_episode
        print("Saved model with reward: " + str(reward_episode))
                

    wandb.log(
        {
        'loss': np.mean(losses),
        'running_reward': running_reward,
        'ep_reward': reward_episode,
        'epsilon': eps_greedy_threshold  
        })
    
    # Evaluate greedy policy
    if i_episode % hparams['log_interval'] == 0:
        test_env = WaveDefenseTabular()
        ep_reward = test(test_env, policy_net)
        ep_rew_history.append(ep_reward)
        print(f'Episode {i_episode}\tSteps: {step_count/1000:.2f}k\tEval reward: {ep_reward}\tRunning reward: {running_reward:.2f}')

wandb.finish()
print(f"Finished training! Eval reward: {ep_reward}")
if not os.path.exists('checkpoints'):
    os.makedirs('checkpoints')
torch.save(policy_net.state_dict(), f'checkpoints/dqn.pt')