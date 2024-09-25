import pygame
import random
import time

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
                screen.blit(blackSquare, (x * blockSize, y * blockSize))
            else:
                screen.blit(whiteSquare, (x * blockSize, y * blockSize))

# Function to check if the move is valid
def is_valid_move(nextX, nextY, map):
    if 0 <= nextY < len(map) and 0 <= nextX < len(map[0]):
        return map[nextY][nextX] == 0
    return False

while running:
    screen.fill(BACKGROUND)  # Clear the screen
    drawMap(map)  # Draw the map

    # Draw the collectible
    collectible_pos = (collectible_coordX * blockSize + blockSize // 2,
                       collectible_coordY * blockSize + blockSize // 2)
    pygame.draw.circle(screen, "gold", collectible_pos, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    next_coordX, next_coordY = coordX, coordY

    if keys[pygame.K_w]:
        next_coordY -= 1
    if keys[pygame.K_s]:
        next_coordY += 1
    if keys[pygame.K_a]:
        next_coordX -= 1
    if keys[pygame.K_d]:
        next_coordX += 1

    if is_valid_move(next_coordX, next_coordY, map):
        coordX, coordY = next_coordX, next_coordY
        player_pos.x = coordX * blockSize
        player_pos.y = coordY * blockSize

    # Check for collision with the collectible
    if (coordX, coordY) == (collectible_coordX, collectible_coordY):
        collectible_coordX, collectible_coordY = get_random_collectible_position()

    # Draw the player centered in the cell
    pygame.draw.circle(screen, "red", (int(player_pos.x + blockSize // 2), int(player_pos.y + blockSize // 2)), 20)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
