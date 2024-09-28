import pygame
import random
import heapq  # Para el algoritmo A*

from assets import *  # Asegúrate de que esto incluya las imágenes para blackSquare y whiteSquare

pygame.init()
running = True
clock = pygame.time.Clock()

# DIMENSIONES DE LA VENTANA
WIDTH, HEIGHT = 1200, 800  # Extiende el ancho para añadir el área de información

# COLORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (200, 200, 200)
TEXT_COLOR = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

blockSize = 40

# Fuente para mostrar información
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 24)

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI SMART AGENT")

# Cargar el tileset después de crear la ventana
tileset_image = pygame.image.load("assets/pokeballs.png").convert_alpha()

# Cargar asset de agente
agent_image = pygame.image.load("assets/agent.png").convert_alpha()
agent_image = pygame.transform.scale(agent_image, (45, 45))  # Escalar al tamaño del bloque


# Mapa
map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
]


# Posición inicial del jugador
coordX, coordY = (1, 1)
player_pos = pygame.Vector2(coordX * blockSize, coordY * blockSize)

# Inicializar la posición del coleccionable
def get_random_collectible_position():
    while True:
        x = random.randint(1, 19)  # Coordenada x aleatoria
        y = random.randint(1, 19)  # Coordenada y aleatoria
        if map[y][x] == 0:  # Asegúrate de que es una posición válida
            return x, y

# Obtener un tile aleatorio del tileset
def get_random_tile():
    tile_x = random.randint(0, 3) * 45  # 4 tiles en el ancho del tileset
    tile_y = random.randint(0, 3) * 45  # 4 tiles en la altura del tileset
    return tileset_image.subsurface((tile_x, tile_y, 45, 45))

# Inicializa la posición del coleccionable y el tile
collectible_coordX, collectible_coordY = get_random_collectible_position()
collectible_tile = get_random_tile()

# Lista para almacenar los datos de movimiento
movement_log = []

# Función para dibujar el mapa
def drawMap(map):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x * blockSize, y * blockSize, blockSize, blockSize))
            else:
                pygame.draw.rect(screen, WHITE, (x * blockSize, y * blockSize, blockSize, blockSize))

# Función para dibujar el mapa con bordes en las celdas, el costo y la heurística
def drawMap(map, goal):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            if cell == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Celda negra (muro)
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Celda blanca (camino)
                
                # Calcular la heurística para la celda actual
                heuristic_value = heuristic((x, y), goal)

                # Agregar el texto "1" (costo) en la esquina inferior izquierda de las celdas de camino
                text_surface = font2.render("1", True, RED)
                screen.blit(text_surface, (x * blockSize, y * blockSize + blockSize - 15))

                # Agregar el valor de la heurística en la esquina inferior derecha
                heuristic_surface = font2.render(str(heuristic_value), True, GREEN)
                screen.blit(heuristic_surface, (x * blockSize + blockSize - 20, y * blockSize + blockSize - 15))

            # Agregar el borde
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)  # Borde gris oscuro

# Función para verificar si el movimiento es válido
def is_valid_move(nextX, nextY, map):
    if 0 <= nextY < len(map) and 0 <= nextX < len(map[0]):
        return map[nextY][nextX] == 0
    return False

# Algoritmo A* y Heurística
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, map):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    # Variable para contar los costos
    movement_log.clear()  # Limpiar el registro anterior
    print("\nIniciando nuevo cálculo de costos:\n")
    while open_list:
        current_priority, current = heapq.heappop(open_list)

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

                    # Log the movement data
                    movement_log.append((current, next_node, new_cost, priority))

                    # Imprimir el costo (heurística) en la terminal
                    print(f"Desde {current} hasta {next_node}, Costo acumulado: {new_cost}, Heurística: {priority}")

    # Reconstruct path
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Function to display movement information
def display_info(movement_log):
    info_x_start = 820  # Starting x position for the info
    y_offset = 20
    screen.fill(BACKGROUND, (info_x_start, 0, WIDTH - 820, HEIGHT))  # Clear the info section

    for i, (start, end, cost, heuristic) in enumerate(movement_log[-10:]):  # Show the last 10 moves
        text = font.render(f"{start} -> {end} | Cost: {cost}, Heur: {heuristic}", True, TEXT_COLOR)
        screen.blit(text, (info_x_start, y_offset * (i + 1)))

# Movimiento del jugador
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
    drawMap(map, (collectible_coordX, collectible_coordY))  # Pasar la posición del coleccionable

    # Dibujar el coleccionable usando el tile seleccionado
    collectible_pos = (collectible_coordX * blockSize + (blockSize - 45) // 2, collectible_coordY * blockSize + (blockSize - 45) // 2)
    screen.blit(collectible_tile, collectible_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player along the path to the collectible
    move_player(path_to_collectible)

    # Check if the player reached the collectible
    if (coordX, coordY) == (collectible_coordX, collectible_coordY):
        # Reposicionar el coleccionable y recalcular el path
        collectible_coordX, collectible_coordY = get_random_collectible_position()
        collectible_tile = get_random_tile()  # Cambia el tile solo al recoger
        path_to_collectible = a_star((coordX, coordY), (collectible_coordX, collectible_coordY), map)

    # Dibujar al jugador centrado en la celda usando la imagen del agente
    screen.blit(agent_image, player_pos)

    # Mostrar información de movimiento
    display_info(movement_log)

    pygame.display.update()
    clock.tick(7)  # Acelerar el movimiento un poco para hacerlo visible

pygame.quit()
