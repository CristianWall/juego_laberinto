
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
TAMANO_LETRA = 20
TAMANO_BOTON = (100, 40)  # Tamaño común para los botones

# Configurar fuente
fuente = pygame.font.Font(None, 40)

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

    # Botones
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

# Función para mostrar un mensaje con fondo negro
    def mostrar_mensaje(mensaje, posicion):
        # Definir el área que ocupará el mensaje
        texto_render = fuente.render(mensaje, True, BLANCO)
        rect_mensaje = texto_render.get_rect(topleft=posicion)
        
        # Dibujar el fondo negro detrás del mensaje
        pygame.draw.rect(pantalla, (0, 0, 0), rect_mensaje)
        
        # Dibujar el mensaje sobre el fondo negro
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

            # Al llegar a 'B' (en tu lógica de detección de objetivo final)
            if laberinto[y_cuadrado][x_cuadrado] == 'B':
                moviendo = False
                mostrar_resultados(tiempo_transcurrido, pasos_juego, nombre_archivo)  # Enviar nombre del archivo
                return  # Esto detiene el ciclo actual del juego y envía al jugador a mostrar los resultados.

        # Limpiar pantalla
        pantalla.fill(NEGRO)
        pared_img = pygame.image.load("pared.png")
        pared_img = pygame.transform.scale(pared_img, (ANCHO_CELDA, ALTO_CELDA))  # Ajustar al tamaño de la celda
        # Dibujar laberinto
        for fila, linea in enumerate(laberinto):
            for columna, celda in enumerate(linea.strip()):
                if celda == '#':
                    pantalla.blit(pared_img, (columna * ANCHO_CELDA, fila * ALTO_CELDA))
                elif celda == ' ':
                    draw_cell(columna, fila, BLANCO)
                elif celda == 'A':
                    draw_cell(columna, fila, ROJO)
                elif celda == 'B':
                    draw_cell(columna, fila, AZUL)

                # Cargar la imagen del personaje
        personaje_img = pygame.image.load("personaje.png")
        personaje_img = pygame.transform.scale(personaje_img, (ANCHO_CELDA, ALTO_CELDA))  # Ajustar al tamaño de la celda
        pantalla.blit(personaje_img, (x_cuadrado * ANCHO_CELDA, y_cuadrado * ALTO_CELDA))

        # Dibujar botones
        boton_volver.dibujar(pantalla, mouse_pos)
        boton_jugar.dibujar(pantalla, mouse_pos)
        boton_resolver.dibujar(pantalla, mouse_pos)
        boton_resolver_q.dibujar(pantalla, mouse_pos)
        boton_resolver_goloso.dibujar(pantalla, mouse_pos)
        boton_resolver_A.dibujar(pantalla, mouse_pos)

        if tiempo_mensaje_mostrar > 0 and time.time() < tiempo_mensaje_ocultar:
            mostrar_mensaje(f"Tiempo total: {tiempo_total:.2f} segundos", (10, 420))
            mostrar_mensaje(f"Número de pasos: {pasos_total}", (10, 450))
        elif time.time() >= tiempo_mensaje_ocultar:
            tiempo_mensaje_mostrar = 0
            tiempo_mensaje_ocultar = 0

        if jugando:
            tiempo_transcurrido = time.time() - inicio_juego
            mostrar_mensaje(f"Tiempo: {tiempo_transcurrido:.2f} s", (10, 420))
            mostrar_mensaje(f"Pasos: {pasos_juego}", (10, 450))
            
        


        pygame.display.flip()



