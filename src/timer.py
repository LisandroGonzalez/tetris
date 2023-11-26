from settings import *

class Timer:
    def __init__(self, duracion, repetir = False, func = None):
        self.repetir = repetir
        self.func = func
        self.duracion = duracion
        
        self.tiempo_comienzo = 0
        self.activo = False
        
    def activar(self):
        self.activo = True
        self.tiempo_comienzo = pygame.time.get_ticks()
        
    def deactivar(self):
        self.activo = False
        self.tiempo_comienzo = 0
        
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_comienzo >= self.duracion and self.activo:
            if self.func and self.tiempo_comienzo != 0:
                self.func()
                
            #resetear timer
            self.deactivar()
            
            if self.repetir:
                self.activar()