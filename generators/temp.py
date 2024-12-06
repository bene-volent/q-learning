import random
from collections import deque
from grid_generator import save_grid
# Define constants for maze elements
EMPTY = 0
WALL = 1
START = 2
FINISH = 3

# Directions for movement (right, down, left, up)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def generate_maze(size):
    # Initialize the maze with walls (1) for all cells
    maze = [[WALL for _ in range(size)] for _ in range(size)]
    
    # Helper function to check if a position is within the maze bounds
    def in_bounds(x, y):
        return 1 <= x < size-1 and 1 <= y < size-1

    # Recursive backtracking to carve paths in the inner grid
    def carve_path(x, y):
        maze[x][y] = EMPTY  # Mark current cell as part of the path
        
        # Shuffle the directions to create a random maze
        random.shuffle(DIRECTIONS)

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if in_bounds(nx, ny) and maze[nx][ny] == WALL:
                # Carve a path by marking the neighboring cells as part of the path
                maze[x + dx][y + dy] = EMPTY
                carve_path(nx, ny)

    # Start carving from a random odd cell within the inner grid
    start_x, start_y = random.randrange(1, size-1, 2), random.randrange(1, size-1, 2)
    carve_path(start_x, start_y)

    # Choose random finish position within the inner grid
    finish_x, finish_y = random.randrange(1, size-1, 2), random.randrange(1, size-1, 2)
    maze[finish_x][finish_y] = FINISH

    # Place the start position
    maze[start_x][start_y] = START

    # Turn the outer rows and columns into walls
    for i in range(size):
        maze[0][i] = WALL  # Top row
        maze[size-1][i] = WALL  # Bottom row
        maze[i][0] = WALL  # Left column
        maze[i][size-1] = WALL  # Right column

    return maze

def is_solvable(maze, size):
    # Find the start and finish positions
    start_pos = None
    finish_pos = None
    for i in range(size):
        for j in range(size):
            if maze[i][j] == START:
                start_pos = (i, j)
            if maze[i][j] == FINISH:
                finish_pos = (i, j)

    # Use BFS to check if there's a path from start to finish
    if not start_pos or not finish_pos:
        return False

    queue = deque([start_pos])
    visited = set([start_pos])

    while queue:
        x, y = queue.popleft()
        
        # If we reach the finish
        if (x, y) == finish_pos:
            return True
        
        # Explore neighbors
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited and maze[nx][ny] != WALL:
                visited.add((nx, ny))
                queue.append((nx, ny))
    
    return False

def print_maze(maze):
    for row in maze:
        print(' '.join(str(cell) for cell in row))

# Generate and print mazes for different sizes
for size in [10, 15, 20, 25]:
    print(f"Maze of size {size}x{size}:")
    
    # Generate the maze and check solvability
    maze = generate_maze(size)
    
    # Ensure the maze is solvable by checking for a valid path from start to finish
    while not is_solvable(maze, size):
        print("Maze is not solvable, regenerating...")
        maze = generate_maze(size)

    print_maze(maze)
    print("\n" + "="*40 + "\n")


    
    save_grid(maze)
    
