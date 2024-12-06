import numpy as np
from grid_env import GridEnvironment
from models.sarsa import SARSA

# Create the environment
env = GridEnvironment('./grid_maze_10.json', render=True)

# Initialize SARSA agent
env_metadata = env.get_metadata()
state_size = env_metadata['num_states']
action_size = env_metadata['num_actions']



agent = SARSA(
  state_size, 
  action_size, 
  learning_rate=0.09862094725702668, 
  discount_factor=0.8702459663357671, 
  exploration_rate=0.15011484516160972, 
  exploration_decay=0.9484188666937521, 
  min_exploration_rate=0.022193724898777682
)

# Training parameters
num_episodes = 10001
max_steps_per_episode = env.max_steps



for episode in range(num_episodes):
  state = env.reset()
  action = agent.choose_action(state)
  done = False
  total_reward = 0

  for step in range(max_steps_per_episode):
    next_state, reward, done, _ = env.step(action)
    next_action = agent.choose_action(next_state)
    agent.learn(state, action, reward, next_state, next_action, done)
    state = next_state
    action = next_action
    total_reward += reward

    if episode % 2000 == 1:
      env.render()
    
    if done:
      break

  print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

env.quit()