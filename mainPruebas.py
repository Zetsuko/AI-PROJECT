import pygame
import random
import heapq  # Necesario para el algoritmo A*

from assets import *  # Make sure this includes the images for blackSquare and whiteSquare

pygame.init()
running = True
clock = pygame.time.Clock()

# WINDOW DIMENSIONS
WIDTH, HEIGHT = 800, 800

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (200, 200, 200)

blockSize = 80

# Map
map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI SMART AGENT")

# Initial player position
coordX, coordY = (1, 1)
player_pos = pygame.Vector2(coordX * blockSize, coordY * blockSize)

# Initialize collectible position
def get_random_collectible_position():
    while True:
        x = random.randint(1, 8)  # Random x coordinate
        y = random.randint(1, 8)  # Random y coordinate
        if map[y][x] == 0:  # Ensure it's a valid position
            return x, y

collectible_coordX, collectible_coordY = get_random_collectible_position()

# Function to draw the map
def drawMap(map):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x * blockSize, y * blockSize, blockSize, blockSize))
            else:
                pygame.draw.rect(screen, WHITE, (x * blockSize, y * blockSize, blockSize, blockSize))

# Function to check if the move is valid
def is_valid_move(nextX, nextY, map):
    if 0 <= nextY < len(map) and 0 <= nextX < len(map[0]):
        return map[nextY][nextX] == 0
    return False

#Algoritmo A* y Heurística
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, map):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            break

        # Posibles movimientos
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in neighbors:
            next_node = (current[0] + dx, current[1] + dy)
            if is_valid_move(next_node[0], next_node[1], map):
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(next_node, goal)
                    heapq.heappush(open_list, (priority, next_node))
                    came_from[next_node] = current

    # Reconstruct path
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Movement function
def move_player(path):
    global coordX, coordY, player_pos
    if path:
        next_step = path.pop(0)
        coordX, coordY = next_step
        player_pos.x = coordX * blockSize
        player_pos.y = coordY * blockSize

# Main game loop
path_to_collectible = a_star((coordX, coordY), (collectible_coordX, collectible_coordY), map)

while running:
    screen.fill(BACKGROUND)
    drawMap(map)

    # Draw the collectible
    collectible_pos = (collectible_coordX * blockSize + blockSize // 2,
                       collectible_coordY * blockSize + blockSize // 2)
    pygame.draw.circle(screen, "gold", collectible_pos, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player along the path to the collectible
    move_player(path_to_collectible)

    # Check if the player reached the collectible
    if (coordX, coordY) == (collectible_coordX, collectible_coordY):
        # Reposition the collectible and recalculate the path
        collectible_coordX, collectible_coordY = get_random_collectible_position()
        path_to_collectible = a_star((coordX, coordY), (collectible_coordX, collectible_coordY), map)

    # Draw the player centered in the cell
    pygame.draw.circle(screen, "red", (int(player_pos.x + blockSize // 2), int(player_pos.y + blockSize // 2)), 20)
    pygame.display.update()
    clock.tick(6)  # Slow down the movement a bit to make it visible

pygame.quit()

