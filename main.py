import pygame
import random
import time

from assets import *


pygame.init()
running = True
dt = 0
clock = pygame.time.Clock()

#DIMENSIONS OF THE WINDOW
WIDTH, HEIGTH = 800, 800

#COLOURS
WHITE = (255,255,255)
BLACK = (0,0,0)
BACKROUND = (200,200,200)

blockSize= 80

map= [
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 0, 1, 1, 0, 0, 1, 0, 1 ],
    [ 1, 0, 0, 1, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 0, 1, 1, 1, 0, 1, 0, 1 ],
    [ 1, 0, 0, 1, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 0, 1, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 0, 1, 0, 0, 1, 0, 1, 1 ],
    [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
]

screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("AI SMART AGENT")

playerX = 1 * blockSize / 2 

playerY = 1 * blockSize / 2

player_pos = pygame.Vector2(playerX, playerY)


def drawMap(map):
    for y, row in enumerate(map):
        for x, cell in enumerate (row):
            if cell == 1:
                screen.blit(blackSquare, (x * blockSize, y*blockSize))
            else:
                screen.blit(whiteSquare, (x* blockSize, y*blockSize))



while running:
    drawMap(map)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.draw.circle(screen, "red", player_pos, 20)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 80
    if keys[pygame.K_s]:
        player_pos.y += 80 
    if keys[pygame.K_a]:    
        player_pos.x -= 80 
    if keys[pygame.K_d]:
        player_pos.x += 80 
    pygame.display.update()
    dt = clock.tick(60) /1000 
    time.sleep(.01)

pygame.quit