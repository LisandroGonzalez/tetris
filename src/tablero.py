from settings import *
from os import path

class Tablero:
    def __init__(self):
        self.superficie = pygame.Surface((SIDEBAR_ANCHO, ALTURA_JUEGO * TABLERO_ALTURA_FRACCION - PADDING))
        self.rect = self.superficie.get_rect(bottomright = (ANCHO_VENTANA - (PADDING * 2 + SIDEBAR_ANCHO), ALTURA_VENTANA - PADDING))
        self.superficie_display = pygame.display.get_surface()
        
        self.fuente = pygame.font.Font(path.join('./src/imagenes','BebasNeue-Regular.ttf'),20)
        
        self.incremento_altura = self.superficie.get_height() / 4
        
        self.nombre = "Pepe"
        self.puntaje = 0
        self.nivel = 1
        self.lineas = 0
    
    def display_texto(self, posicion, texto):
        texto_superficie = self.fuente.render(f'{texto[0]}: {texto[1]}', True, 'white')
        rect_texto = texto_superficie.get_rect(center = posicion)
        self.superficie.blit(texto_superficie, rect_texto)
    
    def run(self):
        self.superficie.fill(GRIS)
        for i, texto in enumerate([('Jugador', self.nombre) ,('Puntaje', self.puntaje), ('Nivel', self.nivel), ('Lineas', self.lineas)]):
            x = self.superficie.get_width() / 2
            y = self.incremento_altura / 2 + i * self.incremento_altura
            self.display_texto((x,y), texto)
        
        self.superficie_display.blit(self.superficie,self.rect)
        pygame.draw.rect(self.superficie_display, BLANCO, self.rect, 4,4)
