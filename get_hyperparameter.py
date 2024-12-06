import optuna
import numpy as np
from grid_env import GridEnvironment
from q_learning import QLearning
from sarsa import SARSA

def objective(trial):
  # Define the search space for hyperparameters
  learning_rate = trial.suggest_loguniform('learning_rate', 1e-5, 1e-1)
  discount_factor = trial.suggest_uniform('discount_factor', 0.8, 0.99)
  exploration_rate = trial.suggest_uniform('exploration_rate', 0.1, 1.0)
  exploration_decay = trial.suggest_uniform('exploration_decay', 0.9, 0.999)
  min_exploration_rate = trial.suggest_uniform('min_exploration_rate', 0.01, 0.1)

  # Create the environment
  env = GridEnvironment('grid_maze_1.json', render=False)

  # Initialize SARSA agent with the trial hyperparameters
  env_metadata = env.get_metadata()
  state_size = env_metadata['num_states']
  action_size = env_metadata['num_actions']

  agent = SARSA(
    state_size,
    action_size,
    learning_rate=learning_rate,
    discount_factor=discount_factor,
    exploration_rate=exploration_rate,
    exploration_decay=exploration_decay,
    min_exploration_rate=min_exploration_rate
  )

  # Training parameters
  num_episodes = 10000
  max_steps_per_episode = env.max_steps
  total_reward = 0

  for episode in range(num_episodes):
    state = env.reset()
    action = agent.choose_action(state)
    done = False
    episode_reward = 0

    for step in range(max_steps_per_episode):
      next_state, reward, done, _ = env.step(action)
      next_action = agent.choose_action(next_state)
      agent.learn(state, action, reward, next_state, next_action, done)
      state = next_state
      action = next_action
      total_reward += reward
      episode_reward += reward

      if done:
        break
    
    # print(f"Episode {episode + 1}/{num_episodes}, Reward: {episode_reward}")
  
  print(f"Average reward: {total_reward / num_episodes}")
  return total_reward / num_episodes

# Create a study and optimize the objective function
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

# Print the best hyperparameters
print("Best hyperparameters: ", study.best_params)