import pygame
import os
import sys
import juego  # Importar el módulo de juego
import subprocess  # Para ejecutar el archivo del menú

# Inicializamos pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Configurar fuente
fuente = pygame.font.Font(None, 40)

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
        pantalla.blit(texto_render, (self.rect.x + 10, self.rect.y + 10))

    def es_clic(self, mouse_pos, evento):
        if self.rect.collidepoint(mouse_pos) and evento.type == pygame.MOUSEBUTTONDOWN:
            return True
        return False

# Obtener archivos de la carpeta "laberintos"
def obtener_archivos_laberintos():
    ruta = "./laberintos"
    archivos = []
    for archivo in os.listdir(ruta):
        if archivo.endswith(".txt") or archivo.endswith(".maze"):  # Filtrar por extensiones si es necesario
            archivos.append(archivo)
    return archivos

# Crear botones basados en los archivos de la carpeta "laberintos"
def crear_botones_laberintos():
    archivos = obtener_archivos_laberintos()
    botones = []
    y_offset = 150  # Espaciado vertical entre botones
    for i, archivo in enumerate(archivos):
        boton = Boton(archivo, (300, y_offset + i * 60), (200, 50), AZUL, VERDE)
        botones.append(boton)
    return botones

# Función para mostrar el menú de opciones
def mostrar_opciones():
    botones_laberintos = crear_botones_laberintos()
    
    # Crear el botón de volver
    boton_volver = Boton("Volver", (350, ALTO_PANTALLA - 60), (100, 50), AZUL, VERDE)

    while True:
        pantalla.fill(NEGRO)
        mouse_pos = pygame.mouse.get_pos()

        # Dibujar botones de archivos
        for boton in botones_laberintos:
            boton.dibujar(pantalla, mouse_pos)

        # Dibujar el botón de volver
        boton_volver.dibujar(pantalla, mouse_pos)

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar clics en los botones de archivos
            for boton in botones_laberintos:
                if boton.es_clic(mouse_pos, evento):
                    archivo_seleccionado = boton.texto
                    # Llamar a la función en juego.py para mostrar el laberinto
                    juego.mostrar_laberinto(archivo_seleccionado)  # Pasar el archivo seleccionado a la función
                    return  # Salir del menú de opciones

            # Detectar clic en el botón de volver
            if boton_volver.es_clic(mouse_pos, evento):
                pygame.quit()  # Cierra el juego actual
                subprocess.run(["python", "menu.py"])  # Ejecuta el menú principal
                sys.exit()  # Asegura que el juego se cierre completamente

        pygame.display.flip()
