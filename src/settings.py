import pygame
import sqlite3

#Tamaño del juego
COLUMNAS = 10
FILAS = 20
TAM_CELDA = 45
ANCHO_JUEGO, ALTURA_JUEGO = COLUMNAS * TAM_CELDA, FILAS * TAM_CELDA

#Tamaño SideBar
SIDEBAR_ANCHO = 200
PREVIEW_ALTURA_FRACCION = 0.7
TABLERO_ALTURA_FRACCION = 1 - PREVIEW_ALTURA_FRACCION

#Tamaño TOP 5
TOP5_ALTO = 100
PUNTAJES_ALTO = 800

#ventana
PADDING = 20
ANCHO_VENTANA = ANCHO_JUEGO + SIDEBAR_ANCHO * 2 + PADDING * 4
ALTURA_VENTANA = ALTURA_JUEGO + PADDING * 2

# comportamiento del juego
ACTUALIZAR_VELOCIDAD_PRINCIPIO = 400
TIEMPO_ESPERA_MOVER = 200
TIEMPO_ESPERA_ROTAR = 200
OFFSET_BLOQUE = pygame.Vector2(COLUMNAS // 2, -1)

#colores
ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
MAGENTA = (255,0,255)
AMARILLO = (255,255,0)
CYAN = (0,255,255)
GRIS = (128,128,128)

# FORMAS DE LOS BLOQUES
TETROMINOS = {
    'T': {'forma': [(0,0),(-1,0),(1,0),(0,-1)], 'color': MAGENTA},
    'O': {'forma': [(0,0),(0,-1),(1,0),(1,-1)], 'color': AMARILLO},
    'J': {'forma': [(0,0),(0,-1),(0,1),(-1,1)], 'color': AZUL},
    'L': {'forma': [(0,0),(0,-1),(0,1),(1,1)], 'color': NEGRO},
    'I': {'forma': [(0,0),(0,-1),(0,-2),(0,1)], 'color': CYAN},
    'S': {'forma': [(0,0),(-1,0),(0,-1),(1,-1)], 'color': VERDE},
    'Z': {'forma': [(0,0),(1,0),(0,-1),(-1,-1)], 'color': ROJO},
}

DATA_PUNTAJE = {1:40, 2:100, 3:300, 4:1200}