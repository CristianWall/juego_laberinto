import pygame
import subprocess
import sys
import time
from resolver_stack_logica import MazeStackFrontier
from resolver_queue_logica import MazeQueueFrontier
from resolver_goloso_logica import MazeGreedyFrontier
from resolver_A_logica import MazeAStarFrontier
from mostrar_mensaje import mostrar_resultados

# Inicializamos pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CELESTE = (0, 255, 255)

# Dimensiones de la pantalla y celdas
ANCHO_CELDA = 25
ALTO_CELDA = 25
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Variables para ajustar tamaño de la letra y botones
TAMANO_LETRA = 30
TAMANO_BOTON = (100, 30)  # Tamaño común para los botones

# Configurar fuente
fuente = pygame.font.Font(None, TAMANO_LETRA)

class Boton:
    def __init__(self, texto, pos, tamano, color_normal, color_hover):
        self.texto = texto
        self.pos = pos
        self.tamano = tamano
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.rect = pygame.Rect(self.pos, self.tamano)

    def dibujar(self, pantalla, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_normal

        pygame.draw.rect(pantalla, color, self.rect)
        texto_render = fuente.render(self.texto, True, BLANCO)
        pantalla.blit(texto_render, (self.rect.x + 10, self.rect.y + 10))

    def es_clic(self, mouse_pos, evento):
        if self.rect.collidepoint(mouse_pos) and evento.type == pygame.MOUSEBUTTONDOWN:
            return True
        return False

def cargar_laberinto(nombre_archivo):
    with open(f"./laberintos/{nombre_archivo}", "r") as archivo:
        laberinto = archivo.readlines()
    return laberinto

def mostrar_laberinto(nombre_archivo):
    laberinto = cargar_laberinto(nombre_archivo)

    # Encontrar la posición inicial del cuadrado rojo (A)
    for fila, linea in enumerate(laberinto):
        if 'A' in linea:
            x_inicial = linea.index('A')
            y_inicial = fila
            break

    # Botones (ajustados al nuevo tamaño común)
    boton_volver = Boton("Volver", (20, ALTO_PANTALLA - 60), TAMANO_BOTON, AZUL, AMARILLO)
    boton_jugar = Boton("Jugar", (130, ALTO_PANTALLA - 60), TAMANO_BOTON, AZUL, AMARILLO)
    boton_resolver = Boton("Stack", (240, ALTO_PANTALLA - 60), TAMANO_BOTON, AZUL, AMARILLO)
    boton_resolver_q = Boton("Queue", (350, ALTO_PANTALLA - 60), TAMANO_BOTON, AZUL, AMARILLO)
    boton_resolver_goloso = Boton("Goloso", (460, ALTO_PANTALLA - 60), TAMANO_BOTON, AZUL, AMARILLO)
    boton_resolver_A = Boton("A*", (570, ALTO_PANTALLA - 60), TAMANO_BOTON, AZUL, AMARILLO)

    x_cuadrado = x_inicial
    y_cuadrado = y_inicial
    moviendo = False
    velocidad = 1
    direccion = None
    jugando = False
    inicio_juego = 0
    pasos_juego = 0

    def es_celda_valida(x, y):
        if 0 <= x < len(laberinto[0].strip()) and 0 <= y < len(laberinto):
            return laberinto[y][x] != '#'
        return False

    def mover_cuadrado():
        nonlocal x_cuadrado, y_cuadrado, moviendo, pasos_juego
        if direccion == "IZQUIERDA":
            nueva_x = x_cuadrado - velocidad
            nueva_y = y_cuadrado
        elif direccion == "DERECHA":
            nueva_x = x_cuadrado + velocidad
            nueva_y = y_cuadrado
        elif direccion == "ARRIBA":
            nueva_x = x_cuadrado
            nueva_y = y_cuadrado - velocidad
        elif direccion == "ABAJO":
            nueva_x = x_cuadrado
            nueva_y = y_cuadrado + velocidad
        else:
            return

        if es_celda_valida(nueva_x, nueva_y):
            x_cuadrado = nueva_x
            y_cuadrado = nueva_y
            pasos_juego += 1
            moviendo = False

    def draw_cell(x, y, color):
        pygame.draw.rect(pantalla, color, (x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))

    def mostrar_mensaje(mensaje, posicion):
        texto_render = fuente.render(mensaje, True, BLANCO)
        pantalla.blit(texto_render, posicion)

    ejecutando = True
    tiempo_mensaje_mostrar = 0
    tiempo_mensaje_ocultar = 0
    tiempo_total = 0
    pasos_total = 0

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if boton_volver.es_clic(mouse_pos, evento):
                pygame.quit()  # Cierra el juego actual
                subprocess.run(["python", "menu.py"])  # Ejecuta el menú de opciones
                sys.exit()  # Asegura que el juego se cierre completamente

            if boton_jugar.es_clic(mouse_pos, evento):
                jugando = True
                inicio_juego = time.time()
                pasos_juego = 0  # Reiniciar contador de pasos

            if boton_resolver.es_clic(mouse_pos, evento):
                maze = MazeStackFrontier(f"./laberintos/{nombre_archivo}")
                tiempo_total, pasos_total = maze.solve(pantalla, ANCHO_CELDA, ALTO_CELDA, draw_cell)
                tiempo_mensaje_mostrar = time.time()
                tiempo_mensaje_ocultar = tiempo_mensaje_mostrar + 5  # Mostrar información por 5 segundos

            if boton_resolver_q.es_clic(mouse_pos, evento):
                maze = MazeQueueFrontier(f"./laberintos/{nombre_archivo}")
                tiempo_total, pasos_total = maze.solve(pantalla, ANCHO_CELDA, ALTO_CELDA, draw_cell)
                tiempo_mensaje_mostrar = time.time()
                tiempo_mensaje_ocultar = tiempo_mensaje_mostrar + 5  # Mostrar información por 5 segundos
            
            if boton_resolver_goloso.es_clic(mouse_pos, evento):
                maze = MazeGreedyFrontier(f"./laberintos/{nombre_archivo}")
                tiempo_total, pasos_total = maze.solve(pantalla, ANCHO_CELDA, ALTO_CELDA, draw_cell)
                tiempo_mensaje_mostrar = time.time()
                tiempo_mensaje_ocultar = tiempo_mensaje_mostrar + 5  # Mostrar información por 5 segundos
            if boton_resolver_A.es_clic(mouse_pos, evento):
                maze = MazeAStarFrontier(f"./laberintos/{nombre_archivo}")
                tiempo_total, pasos_total = maze.solve(pantalla, ANCHO_CELDA, ALTO_CELDA, draw_cell)
                tiempo_mensaje_mostrar = time.time()
                tiempo_mensaje_ocultar = tiempo_mensaje_mostrar + 5  # Mostrar información por 5 segundos

            if evento.type == pygame.KEYDOWN and jugando:
                if evento.key == pygame.K_LEFT:
                    direccion = "IZQUIERDA"
                    moviendo = True
                elif evento.key == pygame.K_RIGHT:
                    direccion = "DERECHA"
                    moviendo = True
                elif evento.key == pygame.K_UP:
                    direccion = "ARRIBA"
                    moviendo = True
                elif evento.key == pygame.K_DOWN:
                    direccion = "ABAJO"
                    moviendo = True

            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    moviendo = False
                    direccion = None

        if moviendo and jugando:
            mover_cuadrado()

        pantalla.fill(NEGRO)

        # Dibujar laberinto
        for y, fila in enumerate(laberinto):
            for x, celda in enumerate(fila.strip()):
                if celda == '#':
                    color = GRIS
                elif celda == 'A':
                    color = ROJO
                elif celda == 'B':
                    color = AZUL
                else:
                    color = BLANCO
                draw_cell(x, y, color)

        # Dibujar cuadrado rojo
        draw_cell(x_cuadrado, y_cuadrado, ROJO)

        # Dibujar botones
        boton_volver.dibujar(pantalla, mouse_pos)
        boton_jugar.dibujar(pantalla, mouse_pos)
        boton_resolver.dibujar(pantalla, mouse_pos)
        boton_resolver_q.dibujar(pantalla, mouse_pos)
        boton_resolver_goloso.dibujar(pantalla, mouse_pos)
        boton_resolver_A.dibujar(pantalla, mouse_pos)

        # Mostrar mensaje de tiempo y pasos si ha resuelto
        if tiempo_mensaje_mostrar != 0 and time.time() < tiempo_mensaje_ocultar:
            mostrar_mensaje(f"Tiempo: {tiempo_total:.2f}s, Pasos: {pasos_total}", (10, 300))

        # Actualizar pantalla
        pygame.display.flip()

