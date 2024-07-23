import pygame
import sys
import random
from pyfiglet import Figlet
from collections import deque
from rich.progress import track
from rich import print
from time import sleep
from rich.console import Console
# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ALGORITHMS ILLUMINATED")
clock = pygame.time.Clock()

def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    
    def carve_path(x, y):
        maze[y][x] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
                maze[y+dy][x+dx] = 0
                carve_path(nx, ny)
    
    carve_path(1, 1)
    return maze

def bfs(maze, start, end):
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        (y, x), path = queue.popleft()
        
        if (y, x) == end:
            yield visited, path
            return
        
        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < ROWS and 0 <= nx < COLS and maze[ny][nx] != 1 and (ny, nx) not in visited:
                queue.append(((ny, nx), path + [(ny, nx)]))
                visited.add((ny, nx))
        
        yield visited, path
    
    return None

def draw_maze(maze, visited, path, start, end):
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif (y, x) == start:
                pygame.draw.rect(screen, GREEN, rect)
            elif (y, x) == end:
                pygame.draw.rect(screen, RED, rect)
            elif (y, x) in visited:
                pygame.draw.rect(screen, YELLOW, rect)
    
    for y, x in path:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLUE, rect)
    
    pygame.display.flip()

def main():
    maze = generate_maze()
    start = None
    end = None
    bfs_generator = None
    path = []
    visited = set()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= CELL_SIZE
                y //= CELL_SIZE
                # print(f"Mouse click at: ({x}, {y})")  
                if start is None:
                    start = (y, x)
                    # print(f"Start set to: {start}") 
                elif end is None:
                    end = (y, x)
                    # print(f"End set to: {end}")
                    bfs_generator = bfs(maze, start, end)
        
        if bfs_generator:
            try:
                visited, path = next(bfs_generator)
            except StopIteration:
                bfs_generator = None
        
        draw_maze(maze, visited, path, start, end)
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    f = Figlet(font='slant')
    print(f.renderText('MAZE EXPLORER'))

    console = Console()

    with console.status("[magenta]RUNNING GAME ENGINE", spinner='hearts') as status:
        tasks = [f"task {n}" for n in range(1, 11)]
        main()
        while tasks:
            task = tasks.pop(0)
            