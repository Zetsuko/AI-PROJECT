import turtle
import random
import heapq  # Necesario para el algoritmo A*

# Configuración de la cuadrícula del laberinto
laberinto = [
    "XOXXXXXXX",
    "XOOOOOOOX",
    "XXXXXXXOX",
    "XXXXXXXOX",
    "XOOOOOOOX",
    "XOOOXOOOX",
    "XXOXXXXOX",
    "XXOXXXXOX"
]

# Configuración de la ventana
ventana = turtle.Screen()
ventana.title("Laberinto con Turtle")
ventana.bgcolor("white")

# Configuración del tamaño de cada celda
celda_size = 40
turtle.setup(width=500, height=500)

# Función para dibujar una celda (pared o espacio)
def dibujar_celda(x, y, es_pared):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    if es_pared:
        turtle.fillcolor("black")
        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(celda_size)
            turtle.right(90)
        turtle.end_fill()
    else:
        for _ in range(4):
            turtle.forward(celda_size)
            turtle.right(90)

# Dibujar el laberinto
def dibujar_laberinto():
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    
    start_x = -len(laberinto[0]) * celda_size / 2
    start_y = len(laberinto) * celda_size / 2

    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            x = start_x + j * celda_size
            y = start_y - i * celda_size
            if celda == "X":
                dibujar_celda(x, y, True)
            else:
                dibujar_celda(x, y, False)

# Función para obtener coordenadas centradas en la cuadrícula
def obtener_coordenadas_centradas(fila, columna):
    start_x = -len(laberinto[0]) * celda_size / 2
    start_y = len(laberinto) * celda_size / 2
    x = start_x + columna * celda_size + celda_size / 2
    y = start_y - fila * celda_size - celda_size / 2
    return x, y

# Configuración del personaje (punto azul)
jugador = turtle.Turtle()
jugador.shape("circle")
jugador.color("blue")
jugador.penup()

# Posición inicial del jugador
posicion_jugador = [1, 1]  # Coordenadas de la cuadrícula
jugador.goto(obtener_coordenadas_centradas(posicion_jugador[0], posicion_jugador[1]))

# Función para verificar si el jugador puede moverse
def puede_moverse(fila, columna):
    if 0 <= fila < len(laberinto) and 0 <= columna < len(laberinto[0]):
        return laberinto[fila][columna] == "O"
    return False

# Configuración del objeto recolectable (triángulo amarillo)
objeto = turtle.Turtle()
objeto.shape("triangle")
objeto.color("yellow")
objeto.penup()

# Posición inicial del objeto recolectable (se coloca en una celda libre "O")
def nueva_posicion_objeto():
    while True:
        fila = random.randint(0, len(laberinto) - 1)
        columna = random.randint(0, len(laberinto[0]) - 1)
        if laberinto[fila][columna] == "O":
            objeto.goto(obtener_coordenadas_centradas(fila, columna))
            return [fila, columna]

# Posición global del objeto recolectable
posicion_objeto = nueva_posicion_objeto()

# Verificar si el jugador ha recolectado el objeto
def verificar_recoleccion():
    global posicion_objeto
    if posicion_jugador == posicion_objeto:
        print("Objeto recolectado!")
        posicion_objeto = nueva_posicion_objeto()
        return True
    return False

# Heurística para A* (distancia de Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementación del algoritmo A*
def a_star(inicio, objetivo):
    open_list = []
    heapq.heappush(open_list, (0, inicio))
    
    came_from = {}
    costo_hasta_ahora = {}
    
    came_from[tuple(inicio)] = None
    costo_hasta_ahora[tuple(inicio)] = 0
    
    while open_list:
        _, actual = heapq.heappop(open_list)
        
        if actual == objetivo:
            break
        
        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in vecinos:
            siguiente = [actual[0] + dx, actual[1] + dy]
            
            if puede_moverse(siguiente[0], siguiente[1]):
                nuevo_costo = costo_hasta_ahora[tuple(actual)] + 1
                
                if tuple(siguiente) not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[tuple(siguiente)]:
                    costo_hasta_ahora[tuple(siguiente)] = nuevo_costo
                    prioridad = nuevo_costo + heuristica(siguiente, objetivo)
                    heapq.heappush(open_list, (prioridad, siguiente))
                    came_from[tuple(siguiente)] = actual
    
    camino = []
    actual = objetivo
    while actual != inicio:
        camino.append(actual)
        actual = came_from[tuple(actual)]
    camino.reverse()
    return camino

# Movimiento automático basado en A*
def mover_automaticamente():
    if verificar_recoleccion():
        return  # Si se recoge el objeto, detiene el movimiento para reposicionar el objeto.
    
    camino = a_star(posicion_jugador, posicion_objeto)
    
    if camino:
        for paso in camino:
            posicion_jugador[0], posicion_jugador[1] = paso
            jugador.goto(obtener_coordenadas_centradas(paso[0], paso[1]))
            
            if verificar_recoleccion():
                break  # Si se recolecta el objeto, salimos del ciclo
    
    # Reiniciar el movimiento después de 500ms
    ventana.ontimer(mover_automaticamente, 500)

# Dibujar el laberinto y el jugador
dibujar_laberinto()

# Iniciar el movimiento automático
mover_automaticamente()

# Mantener la ventana abierta
ventana.mainloop()
