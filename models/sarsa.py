import numpy as np

class SARSA:
  def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
    self.state_size = state_size
    self.action_size = action_size
    self.learning_rate = learning_rate
    self.discount_factor = discount_factor
    self.exploration_rate = exploration_rate
    self.exploration_decay = exploration_decay
    self.min_exploration_rate = min_exploration_rate
    self.q_table = np.zeros((state_size, action_size))

  def choose_action(self, state):
    if np.random.rand() < self.exploration_rate:
      return np.random.choice(self.action_size)
    return np.argmax(self.q_table[state])

  def learn(self, state, action, reward, next_state, next_action, done):
    td_target = reward + self.discount_factor * self.q_table[next_state, next_action] * (1 - done)
    td_error = td_target - self.q_table[state, action]
    self.q_table[state, action] += self.learning_rate * td_error

    if done:
      self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

  def save(self, filename):
    np.save(filename, self.q_table)
    
  def load(self, filename):
    self.q_table = np.load(filename)
