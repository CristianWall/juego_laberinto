import pygame
import sys
import random
from opciones import mostrar_opciones  # Importamos la función mostrar_opciones de opciones.py

# Inicializamos pygame
pygame.init()

# Iniciar el mezclador de sonido
pygame.mixer.init()

# Cargar y reproducir música en bucle
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)  # -1 indica que la música se reproducirá en bucle infinito

# Definir colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Cargar imagen de fondo
fondo = pygame.image.load("fondo.png")  # Asegúrate de que la imagen esté en la misma carpeta

# Cargar imagen de fuegos para animación
fuegos = pygame.image.load("fuego.png")
fuegos_rect = fuegos.get_rect()  # Obtener rectángulo que contiene la imagen
fuegos_rect.topleft = (random.randint(0, ANCHO_PANTALLA - fuegos_rect.width),
                       random.randint(0, ALTO_PANTALLA - fuegos_rect.height))

# Variables para controlar la velocidad de movimiento
velocidad_x = random.choice([-1, 1]) * random.randint(2, 5)  # Velocidad aleatoria en X
velocidad_y = random.choice([-1, 1]) * random.randint(2, 5)  # Velocidad aleatoria en Y

# Configurar fuente
fuente = pygame.font.Font(None, 40)
fuente_titulo = pygame.font.Font(None, 80)  # Fuente más grande para el título

# Definir clase Boton
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
        pantalla.blit(texto_render, (self.rect.x + 20, self.rect.y + 10))

    def es_clic(self, mouse_pos, evento):
        if self.rect.collidepoint(mouse_pos) and evento.type == pygame.MOUSEBUTTONDOWN:
            return True
        return False

# Crear botones
boton_jugar = Boton("Empezar Juego", (300, 200), (200, 80), AZUL, VERDE)
boton_opciones = Boton("Opciones", (300, 300), (200, 80), AZUL, VERDE)
boton_salir = Boton("Salir", (300, 400), (200, 80), AZUL, ROJO)

# Función para mostrar el menú principal
def menu_principal():
    global velocidad_x, velocidad_y

    while True:
        # Dibujar fondo
        pantalla.blit(fondo, (0, 0))  # Dibuja la imagen en la esquina superior izquierda (0, 0)

        # Actualizar posición de fuegos
        fuegos_rect.x += velocidad_x
        fuegos_rect.y += velocidad_y

        # Comprobar si la imagen toca los bordes y cambiar la dirección
        if fuegos_rect.left <= 0 or fuegos_rect.right >= ANCHO_PANTALLA:
            velocidad_x = -velocidad_x  # Invertir la dirección horizontal
        if fuegos_rect.top <= 0 or fuegos_rect.bottom >= ALTO_PANTALLA:
            velocidad_y = -velocidad_y  # Invertir la dirección vertical

        # Dibujar la imagen de fuegos en su nueva posición
        pantalla.blit(fuegos, fuegos_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Dibujar título
        titulo_render = fuente_titulo.render("Calobazos y Dragones", True, BLANCO)
        pantalla.blit(titulo_render, (100, 50))  # Posición del título

        # Dibujar botones
        boton_jugar.dibujar(pantalla, mouse_pos)
        boton_opciones.dibujar(pantalla, mouse_pos)
        boton_salir.dibujar(pantalla, mouse_pos)

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Al hacer clic en "Empezar Juego", mostramos el menú de opciones
            if boton_jugar.es_clic(mouse_pos, evento):
                return mostrar_opciones()  # Llamar a mostrar_opciones y salir del menú principal

            # Al hacer clic en "Opciones", mostramos el menú de opciones
            if boton_opciones.es_clic(mouse_pos, evento):
                return mostrar_opciones()  # Llamar a mostrar_opciones y salir del menú principal

            # Al hacer clic en "Salir", cerramos el juego
            if boton_salir.es_clic(mouse_pos, evento):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# Ejecutar el menú principal
menu_principal()
