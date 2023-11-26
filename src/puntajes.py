from settings import *
from os import path

class Puntajes:
    def __init__(self):
        self.superficie_puntajes = pygame.Surface((SIDEBAR_ANCHO, PUNTAJES_ALTO))
        self.rect_p = self.superficie_puntajes.get_rect(bottomright = (ANCHO_VENTANA - PADDING, ALTURA_JUEGO + PADDING))
        self.superficie_puntajes_display = pygame.display.get_surface()
        
        self.superficie_top5 = pygame.Surface((SIDEBAR_ANCHO, TOP5_ALTO))
        self.rect_top5 = self.superficie_top5.get_rect(topright = (ANCHO_VENTANA - PADDING, PADDING))
        self.superficie_top5_display = pygame.display.get_surface()
        
        self.fuente_puntajes = pygame.font.Font(path.join('./src/imagenes','BebasNeue-Regular.ttf'),18)
        self.fuente_top5 = pygame.font.Font(path.join('./src/imagenes','BebasNeue-Regular.ttf'),50)
        self.incremento_altura = self.superficie_puntajes.get_height() / 5

    def display_nombre_jugador(self, posicion,top ,nombre):
        texto_nombre = f"Top {top}: {nombre}"
        texto_superficie = self.fuente_puntajes.render(texto_nombre, True, 'white')
        rect_texto_nombre = texto_superficie.get_rect(center = posicion)
        self.superficie_puntajes.blit(texto_superficie, rect_texto_nombre)
        
    def display_puntaje_jugador(self, posicion, puntaje):
        texto_puntaje = f"Puntaje: {puntaje}"
        texto_superficie = self.fuente_puntajes.render(texto_puntaje, True, 'white')
        rect_texto_puntaje = texto_superficie.get_rect(center = posicion)
        self.superficie_puntajes.blit(texto_superficie, rect_texto_puntaje)
        
    def titulo_top5(self):
        texto_sup = self.fuente_top5.render("TOP 5", True, 'white')
        rect_txt = texto_sup.get_rect(center = (SIDEBAR_ANCHO / 2, TOP5_ALTO / 2))
        self.superficie_top5.blit(texto_sup, rect_txt)
        self.superficie_top5_display.blit(self.superficie_top5,self.rect_top5)
                
    def run(self):
        self.superficie_puntajes.fill(GRIS)
        self.superficie_top5.fill(GRIS)
        
        with sqlite3.connect(path.join("./src/basedatos", "bd_tetris.db")) as conexion:
            cursor = conexion.execute("SELECT * FROM puntajes ORDER BY puntaje DESC")
        
        items = cursor.fetchmany(5)
        
        for i in range(len(items)):
            x = self.superficie_puntajes.get_width() / 2
            y_nombre = self.incremento_altura / 5 + i * self.incremento_altura
            y_jugador = self.incremento_altura / 5 + i *self.incremento_altura + 20
            self.display_nombre_jugador((x,y_nombre), i+1 ,items[i][1])
            self.display_puntaje_jugador((x, y_jugador), items[i][2])
        
        self.superficie_puntajes_display.blit(self.superficie_puntajes,self.rect_p)
        pygame.draw.rect(self.superficie_puntajes_display, BLANCO, self.rect_p, 4,4)
        
        self.titulo_top5()