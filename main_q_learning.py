import numpy as np
from grid_env import GridEnvironment
from models.q_learning import QLearning

# Create the environment
env = GridEnvironment('./grid_maze_10.json', render=True)

# Initialize Q-learning agent
env_metadata = env.get_metadata()
state_size = env_metadata['num_states']
action_size = env_metadata['num_actions']

agent = QLearning(
  state_size, 
  action_size, 
  learning_rate=0.09049795281994832, 
  discount_factor=0.8217216403588687, 
  exploration_rate=0.5237087177545426, 
  exploration_decay=0.9192058384004347, 
  min_exploration_rate=0.015814477128200038
)

# Training parameters
num_episodes = 10001
max_steps_per_episode = env.max_steps

for episode in range(num_episodes):
  state = env.reset()
  done = False
  total_reward = 0

  for step in range(max_steps_per_episode):
    action = agent.choose_action(state)
    next_state, reward, done, _ = env.step(action)
    agent.learn(state, action, reward, next_state, done)
    state = next_state
    total_reward += reward

    if episode % 2000 == 1:
      env.render()
    
    if done:
      break

  print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

env.quit()