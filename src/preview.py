from settings import *
from os import path

class Preview:
    def __init__(self):
        self.superficie_display = pygame.display.get_surface()
        self.superficie = pygame.Surface((SIDEBAR_ANCHO, ALTURA_JUEGO * PREVIEW_ALTURA_FRACCION - PADDING))
        self.rect = self.superficie.get_rect(topright = (ANCHO_VENTANA - (PADDING * 2 + SIDEBAR_ANCHO), PADDING))

        
        self.forma_superficies = {forma: pygame.image.load(path.join('./src/imagenes',f'{forma}.png')).convert_alpha() for forma in TETROMINOS.keys()}
           
        self.altura_fragmento = self.superficie.get_height() / 3
            
    def display_formas(self, formas):
        for i, forma in enumerate(formas):
            superficie_forma = self.forma_superficies[forma]
            x = self.superficie.get_width() / 2
            y = self.altura_fragmento / 2 + i * self.altura_fragmento
            rect = superficie_forma.get_rect(center = (x,y))
            self.superficie.blit(superficie_forma,rect)
        
    def run(self, formas_siguientes):
        self.superficie.fill(GRIS)
        self.display_formas(formas_siguientes)
        self.superficie_display.blit(self.superficie,self.rect)
        pygame.draw.rect(self.superficie_display, BLANCO, self.rect, 4, 4)