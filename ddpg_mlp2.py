import gym
import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from ddpg_agent import DDPGAgent
from fcn_train_test import train, test
from archs.mlp2_models import Actor, Critic
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", type=str, choices=['train', 'test'],
                    default='train', help="train or test?")

args = parser.parse_args()
env = gym.make('BipedalWalker-v3')
agent = DDPGAgent(Actor, Critic, state_size = env.observation_space.shape[-1], action_size=env.action_space.shape[-1])
env.seed(0)
print("Action dimension : ",env.action_space.shape)
print("State  dimension : ",env.observation_space.shape)
print("Action sample : ",env.action_space.sample())
print("State sample  : \n ",env.reset())    

if args.flag == 'train':   
	scores = train(env, agent, trainer_name='mlp2')
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.plot(np.arange(1, len(scores)+1), scores)
	plt.ylabel('Score')
	plt.xlabel('Episode #')
	plt.show()
	env.close()
elif args.flag == 'test':
	try:
	    agent.train_actor.load_state_dict(torch.load(os.path.join('models', 'best_mlp2_actor.pth'), map_location={'cuda:0': 'cpu'}))
	    agent.train_critic.load_state_dict(torch.load(os.path.join('models', 'best_mlp2_critic.pth'), map_location={'cuda:0': 'cpu'}))
	except:
	    agent.train_actor.load_state_dict(torch.load(os.path.join('models', 'mlp2_actor.pth'), map_location={'cuda:0': 'cpu'}))
	    agent.train_critic.load_state_dict(torch.load(os.path.join('models', 'mlp2_critic.pth'), map_location={'cuda:0': 'cpu'}))

	scores = test(env, agent)

	env.close()
else:
	print('Wrong flag!')
