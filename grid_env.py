import pygame
import json
import numpy as np
from typing import Tuple, Dict

class GridEnvironment:
    def __init__(self, grid_path: str, max_steps_multiplier=10, render=False):
        with open('D:\\code\\Python\\python-project\\q-learning\\mazes\\' + grid_path, 'r') as file:
            grid = json.load(file)
        
        self.grid = np.array(grid).flatten()  # Convert grid to a flattened numpy array
        self.grid_size = int(np.sqrt(self.grid.size))  # Calculate grid size from flattened array
        self.state = None  # Agent's current position
        self.start = None  # Start position
        self.finish = None  # Finish position
        self.steps = 0
        self.max_steps = max_steps_multiplier * self.grid_size
        self.done = False
        self.reward = 0
        self.agent_image = "player.png"  # Replace this with the agent image path
        self.render_flag = render  # Flag to control if rendering is enabled

        if self.render_flag:
            pygame.init()  # Initialize Pygame if render is enabled
            CELL_SIZE = 40
            self.screen = pygame.display.set_mode((self.grid_size * CELL_SIZE, self.grid_size * CELL_SIZE))
            pygame.display.set_caption("Grid Environment")

        # Locate start and finish points
        self.start, self.finish = self._find_special_points()
        self.reset()

    def _find_special_points(self) -> Tuple[int, int]:
        start = np.argwhere(self.grid == 2)[0][0]
        finish = np.argwhere(self.grid == 3)[0][0]
        return start, finish

    def reset(self) -> int:
        """Resets the environment to the initial state."""
        self.state = self.start
        self.steps = 0
        self.done = False
        self.reward = 0
        return self.state

    def step(self, action: int) -> Tuple[int, int, bool, Dict]:
        """Takes an action and returns the new state, reward, done, and info."""
        if self.done:
            raise Exception("Environment is already finished. Call reset() to restart.")
        
        x, y = divmod(self.state, self.grid_size)
        new_x, new_y = x, y
        
        if action == 0:  # Up
            new_x -= 1
        elif action == 1:  # Right
            new_y += 1
        elif action == 2:  # Down
            new_x += 1
        elif action == 3:  # Left
            new_y -= 1

        # Check if new position is valid
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size and self.grid[new_x * self.grid_size + new_y] != 1:
            self.state = new_x * self.grid_size + new_y
        
        # Update rewards
        if self.state == self.finish:
            self.reward = 100  # Reward for reaching the finish
            self.done = True
        elif self.steps >= self.max_steps:
            self.reward = -50  # Penalty for exceeding max steps
            self.done = True
        else:
            self.reward = -1  # Small penalty for each step taken

        self.steps += 1

        return self.state, self.reward, self.done, {}

    def render(self):
        """Displays the grid environment using Pygame."""
        if not self.render_flag:
            return

        CELL_SIZE = 40
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        
        # Draw grid
        for index, cell in enumerate(self.grid):
            x, y = divmod(index, self.grid_size)
            color = (255, 255, 255)  # Default: white
            if cell == 1:  # Wall
                color = (100, 100, 100)
            elif cell == 2:  # Start
                color = (144, 238, 144)
            elif cell == 3:  # Finish
                color = (255, 105, 180)
            
            pygame.draw.rect(self.screen, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, (200, 200, 200), (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Draw agent
        agent_x, agent_y = divmod(self.state, self.grid_size)
        agent_rect = pygame.Rect(agent_y * CELL_SIZE, agent_x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        agent_image = pygame.image.load(self.agent_image)
        agent_image = pygame.transform.scale(agent_image, (CELL_SIZE, CELL_SIZE))
        self.screen.blit(agent_image, agent_rect.topleft)

        pygame.display.flip()
        pygame.time.delay(100)  # Delay to slow down the rendering for visibility

    def get_metadata(self) -> Dict:
        """Returns metadata about the environment."""
        return {
            "num_states": self.grid.size,
            "num_actions": 4,
        }

    def quit(self):
        """Clean up the Pygame resources when done rendering."""
        if self.render_flag:
            pygame.quit()
