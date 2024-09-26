import pygame
import random
import time

from assets import *


pygame.init()
running = True
dt = 0
clock = pygame.time.Clock()

#DIMENSIONS OF THE WINDOW
WIDTH, HEIGHT = 1000, 800  # Ancho para incluir el panel lateral
PANEL_WIDTH = 200  # Espacio a la derecha para mostrar el contador

#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND = (200, 200, 200)
BORDER = (100, 100, 100)
PANEL_COLOR = (220, 220, 220)

blockSize = 40  # Tamaño de los bloques
font = pygame.font.SysFont(None, 48)  # Definir la fuente para el texto

# Contador de esferas recogidas
balls_collected = 0

# Generar un mapa con un pasillo principal y salas a los lados
def generate_hospital_map(rows, cols):
    new_map = [[1 for _ in range(cols)] for _ in range(rows)]  # Lleno de paredes inicialmente

    # Crear el pasillo principal de al menos 3 de ancho
    main_corridor_y = rows // 2 - 1  # Posición vertical del pasillo principal (centrado)
    for y in range(main_corridor_y, main_corridor_y + 3):  # Pasillo de 3 bloques de ancho
        for x in range(cols):
            new_map[y][x] = 0

    # Crear salas a los lados del pasillo principal y conectarlas
    rooms = []
    def create_room(x, y, width, height):
        for i in range(y, y + height):
            for j in range(x, x + width):
                if 0 < i < rows and 0 < j < cols:  # Asegurarse de que la sala esté dentro de los límites
                    new_map[i][j] = 0

    # Generar varias salas en los lados del pasillo
    room_width, room_height = 5, 5  # Tamaño estándar de las salas

    # Lado izquierdo del pasillo
    rooms.append((1, main_corridor_y - room_height - 1, room_width, room_height))  # Sala 1
    rooms.append((1, main_corridor_y + 3 + 1, room_width, room_height))  # Sala 2
    rooms.append((10, main_corridor_y - room_height - 1, room_width, room_height))  # Sala 3
    rooms.append((10, main_corridor_y + 3 + 1, room_width, room_height))  # Sala 4

    # Lado derecho del pasillo
    rooms.append((cols - room_width - 1, main_corridor_y - room_height - 1, room_width, room_height))  # Sala 5
    rooms.append((cols - room_width - 1, main_corridor_y + 3 + 1, room_width, room_height))  # Sala 6
    rooms.append((cols - room_width - 1 - 9, main_corridor_y - room_height - 1, room_width, room_height))  # Sala 7
    rooms.append((cols - room_width - 1 - 9, main_corridor_y + 3 + 1, room_width, room_height))  # Sala 8

    for room in rooms:
        create_room(*room)

    # Conectar las salas al pasillo principal
    for x in range(cols):
        if new_map[main_corridor_y - 1][x] == 0:  # Si hay un pasillo en la fila superior del pasillo principal
            for room in rooms:
                room_x, room_y, room_width, room_height = room
                if room_x < x < room_x + room_width and room_y <= main_corridor_y - 1 < room_y + room_height:
                    new_map[room_y + room_height][x] = 0  # Conectar el pasillo debajo de la sala
        if new_map[main_corridor_y + 3][x] == 0:  # Si hay un pasillo en la fila inferior del pasillo principal
            for room in rooms:
                room_x, room_y, room_width, room_height = room
                if room_x < x < room_x + room_width and room_y <= main_corridor_y + 3 < room_y + room_height:
                    new_map[room_y - 1][x] = 0  # Conectar el pasillo arriba de la sala

    return new_map

# Generar el mapa con pasillo y salas
map = generate_hospital_map(20, 25)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI SMART AGENT")

# Posición inicial del jugador
playerX = 1
playerY = map.index(next(filter(lambda r: 0 in r, map)))  # Buscar la primera casilla vacía en Y
player_pos = pygame.Vector2(playerX * blockSize + blockSize // 2, playerY * blockSize + blockSize // 2)

# Generar la posición inicial del objeto (esfera)
def generate_random_position():
    while True:
        x = random.randint(1, 23)
        y = random.randint(1, 18)
        if map[y][x] == 0:  # Asegurarse de que sea una casilla vacía
            return pygame.Vector2(x * blockSize + blockSize // 2, y * blockSize + blockSize // 2)

object_pos = generate_random_position()

# Función para dibujar el mapa con bordes
def drawMap(map):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            if cell == 1:
                screen.blit(blackSquare, (x * blockSize, y * blockSize))
            else:
                screen.blit(whiteSquare, (x * blockSize, y * blockSize))
            pygame.draw.rect(screen, BORDER, rect, 2)  # Dibujar borde después de las imágenes

# Función para dibujar el panel lateral
def draw_panel():
    panel_rect = pygame.Rect(WIDTH - PANEL_WIDTH, 0, PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)  # Dibuja el panel
    pygame.draw.rect(screen, BLACK, panel_rect, 3)  # Borde del panel

    # Mostrar el texto del contador
    text = font.render(f"Bolas: {balls_collected}", True, BLACK)
    screen.blit(text, (WIDTH - PANEL_WIDTH + 20, 20))

while running:
    screen.fill(BACKGROUND)
    drawMap(map)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Dibuja al jugador (personaje más pequeño)
    pygame.draw.circle(screen, RED, player_pos, 15)  # Hacer el círculo más pequeño
    
    # Dibuja el objeto (esfera)
    pygame.draw.circle(screen, GREEN, object_pos, 15)
    
    # Dibuja el panel lateral
    draw_panel()
    
    # Movimiento del jugador por casilla
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w] and map[int(playerY) - 1][int(playerX)] == 0:  # Mover hacia arriba si no es pared
        playerY -= 1
    if keys[pygame.K_s] and map[int(playerY) + 1][int(playerX)] == 0:  # Mover hacia abajo si no es pared
        playerY += 1
    if keys[pygame.K_a] and map[int(playerY)][int(playerX) - 1] == 0:  # Mover hacia la izquierda si no es pared
        playerX -= 1
    if keys[pygame.K_d] and map[int(playerY)][int(playerX) + 1] == 0:  # Mover hacia la derecha si no es pared
        playerX += 1

    # Actualizar la posición del jugador
    player_pos = pygame.Vector2(playerX * blockSize + blockSize // 2, playerY * blockSize + blockSize // 2)
    
    # Verificar si el jugador ha tomado el objeto
    if player_pos.distance_to(object_pos) < 30:  # Distancia mínima para tomar el objeto
        object_pos = generate_random_position()  # Mover el objeto a una nueva posición
        balls_collected += 1  # Incrementar el contador
    
    pygame.display.update()
    dt = clock.tick(60) / 1000
    time.sleep(0.1)  # Añadir un pequeño retardo para evitar que se mueva demasiado rápido

pygame.quit()