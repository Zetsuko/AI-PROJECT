import pygame

blockSize = 80

blackSquare = pygame.image.load('assets/BLACK.jpg')
blackSquare = pygame.transform.scale(blackSquare, (blockSize, blockSize))


whiteSquare = pygame.image.load('assets/WHITE.jpg')
whiteSquare = pygame.transform.scale(whiteSquare, (blockSize, blockSize))