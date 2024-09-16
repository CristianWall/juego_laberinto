import pygame  # Importar pygame

def es_celda_valida(laberinto, x, y):
    """Verifica si la celda (x, y) es válida y no es una pared."""
    if 0 <= x < len(laberinto[0].strip()) and 0 <= y < len(laberinto):
        return laberinto[y][x] != '#'
    return False

def mover_cuadrado(x_cuadrado, y_cuadrado, direccion, laberinto):
    """Mueve el cuadrado en la dirección indicada si la celda destino es válida."""
    velocidad = 1
    nueva_x, nueva_y = x_cuadrado, y_cuadrado
    
    if direccion == "IZQUIERDA":
        nueva_x -= velocidad
    elif direccion == "DERECHA":
        nueva_x += velocidad
    elif direccion == "ARRIBA":
        nueva_y -= velocidad
    elif direccion == "ABAJO":
        nueva_y += velocidad
    
    if es_celda_valida(laberinto, nueva_x, nueva_y):
        return nueva_x, nueva_y
    return x_cuadrado, y_cuadrado

def dibujar_cuadrado(pantalla, x, y, color, ancho_celda, alto_celda):
    """Dibuja un cuadrado en la posición (x, y) con el color especificado."""
    pygame.draw.rect(pantalla, color, (x * ancho_celda, y * alto_celda, ancho_celda, alto_celda))
