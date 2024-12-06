import pygame
import json
from tkinter import Tk, simpledialog
import os



def print_instructions():
    print("Instructions:")
    print("1. Press 'W' to toggle Wall mode and place walls.")
    print("2. Press 'S' to set the Start point (only one allowed).")
    print("3. Press 'F' to set the Finish point (only one allowed).")
    print("4. Press 'Enter' to save the grid to a JSON file and exit.")
    print("5. Use the mouse to click on cells and modify the grid.")


# Draw grid on the screen
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if grid[y][x] == EMPTY else GRAY
            if grid[y][x] == WALL:
                color = GRAY
            elif grid[y][x] == START:
                color = GREEN
            elif grid[y][x] == FINISH:
                color = RED

            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Save grid to a JSON file
def save_grid(g):
    
    if g:
        grid = g
    # Ensure the directory exists
    os.makedirs("./mazes", exist_ok=True)
    
    # Find the next available filename
    i = 1
    while os.path.exists(f"./mazes/grid_maze_{i}.json"):
        i += 1
    
    filename = f"./mazes/grid_maze_{i}.json"
    with open(filename, "w") as f:
        json.dump(grid, f)
    print(f"Grid saved as {filename}")


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Constants for grid colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (144, 238, 144)  # Light green
    RED = (255, 105, 180)    # Hot pink
    GRAY = (100, 100, 100)   # Dark gray

    # Prompt user for grid size using Tkinter
    Tk().withdraw()  # Hide the Tkinter root window
    grid_size = simpledialog.askinteger("Grid Size", "Enter the grid size (e.g., 10 for 10x10):")
    if not grid_size or grid_size < 3:
        print("Invalid grid size. Using default size of 10.")
        grid_size = 10
        # Game loop
        running = True
        
    # Grid settings
    CELL_SIZE = 40
    GRID_WIDTH = grid_size
    GRID_HEIGHT = grid_size
    SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
    SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

    print_instructions()
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Maze Editor")

    # Create a grid with all cells as empty

    EMPTY = 0
    WALL = 1
    START = 2
    FINISH = 3
    grid = [[WALL if x == 0 or y == 0 or x == GRID_WIDTH - 1 or y == GRID_HEIGHT - 1 else EMPTY 
            for x in range(GRID_WIDTH)] 
            for y in range(GRID_HEIGHT)]

    # Variables to track selection mode
    current_mode = "WALL"  # Modes: WALL, START, FINISH
    start_set = False
    finish_set = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    current_mode = "WALL"
                elif event.key == pygame.K_s:
                    current_mode = "START"
                elif event.key == pygame.K_f:
                    current_mode = "FINISH"
                elif event.key == pygame.K_RETURN:
                    save_grid()
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

                if current_mode == "WALL":
                    if grid[grid_y][grid_x] == START:
                        start_set = False
                    grid[grid_y][grid_x] = WALL
                    

                elif current_mode == "START":
                    if not start_set:
                        grid[grid_y][grid_x] = START
                        start_set = True
                    else:
                        print("Start point already set!")

                elif current_mode == "FINISH":
                    if not finish_set:
                        grid[grid_y][grid_x] = FINISH
                        finish_set = True
                    else:
                        print("Finish point already set!")

        # Update screen
        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()

    pygame.quit()
