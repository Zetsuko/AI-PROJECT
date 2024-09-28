import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 720, 720
BLOCK_SIZE = 60  # Tamaño inicial de las celdas
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE  # Número inicial de filas y columnas

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor de Mapas")

# Función para recalcular filas, columnas y ajustar el mapa cuando se cambia el tamaño de las celdas
def recalculate_grid():
    global ROWS, COLS, map_matrix
    ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
    # Redimensionar el mapa si cambia el número de filas/columnas
    new_map_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    # Mantener los datos antiguos si es posible
    for row in range(min(len(map_matrix), ROWS)):
        for col in range(min(len(map_matrix[0]), COLS)):
            new_map_matrix[row][col] = map_matrix[row][col]
    
    map_matrix = new_map_matrix

# Crear la matriz del mapa (inicialmente todo es 'camino' (0))
map_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Función para dibujar la cuadrícula
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Función para dibujar el mapa basado en la matriz
def draw_map():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if map_matrix[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Función para cambiar el estado de una celda
def toggle_cell(pos):
    x, y = pos
    row = y // BLOCK_SIZE
    col = x // BLOCK_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        if map_matrix[row][col] == 0:
            map_matrix[row][col] = 1  # Cambiar a muro
        else:
            map_matrix[row][col] = 0  # Cambiar a camino

# Función para imprimir el mapa
def print_map():
    print("\n# Mapa generado:")
    for row in map_matrix:
        print(row)

# Loop principal
running = True
while running:
    screen.fill(BLUE)

    # Dibujar el mapa y la cuadrícula
    draw_map()
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                toggle_cell(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print_map()  # Imprimir la matriz del mapa

            # Cambiar el tamaño de las celdas con + y -
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                if BLOCK_SIZE < 120:  # Limitar el tamaño máximo de las celdas
                    BLOCK_SIZE += 10
                    recalculate_grid()

            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                if BLOCK_SIZE > 20:  # Limitar el tamaño mínimo de las celdas
                    BLOCK_SIZE -= 10
                    recalculate_grid()

    pygame.display.update()

pygame.quit()