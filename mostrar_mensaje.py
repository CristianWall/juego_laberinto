import pygame
import sys

# Inicializamos pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

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

def mostrar_resultados(tiempo, pasos, nombre_laberinto):
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Resultados")

    boton_reintentar = Boton("Reintentar", (350, 500), (150, 50), AZUL, AMARILLO)

    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if boton_reintentar.es_clic(mouse_pos, evento):
                # Regresar a juego.py con el mismo archivo de laberinto
                from juego import mostrar_laberinto
                mostrar_laberinto(nombre_laberinto)  # Pasar el archivo del laberinto
                return

        pantalla.fill(NEGRO)

        # Mostrar los resultados
        texto_m = fuente.render(f"Felicidades Terminaste!!", True, BLANCO)
        texto_tiempo = fuente.render(f"Tiempo total: {tiempo:.2f} s", True, BLANCO)
        texto_pasos = fuente.render(f"Pasos totales: {pasos}", True, BLANCO)
        pantalla.blit(texto_m, (250, 150))
        pantalla.blit(texto_tiempo, (250, 200))
        pantalla.blit(texto_pasos, (250, 250))

        # Dibujar botón de reintentar
        boton_reintentar.dibujar(pantalla, mouse_pos)

        pygame.display.flip()


# Este archivo mostrará los resultados cuando se llame la función 'mostrar_resultados'
