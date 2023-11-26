from settings import *
import sys
from juego import Juego
from tablero import Tablero
from preview import Preview
from puntajes import Puntajes
from random import choice
from os import path

class Main:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((ANCHO_VENTANA, ALTURA_VENTANA))
        self.reloj = pygame.time.Clock()
        pygame.display.set_caption("Tetris")
        
        self.formas_siguientes = [choice(list(TETROMINOS.keys())) for forma in range(3)]
        
        self.juego = Juego(self.obtener_forma_siguiente, self.actualizar_tablero)
        self.tablero = Tablero()
        self.preview = Preview()
        self.puntajes = Puntajes()
        
    def actualizar_tablero(self, lineas, puntaje, nivel):
        self.tablero.lineas = lineas
        self.tablero.puntaje = puntaje
        self.tablero.nivel = nivel
        
    def obtener_forma_siguiente(self):
        forma_siguiente = self.formas_siguientes.pop(0)
        self.formas_siguientes.append(choice(list(TETROMINOS.keys())))
        return forma_siguiente
    
    def run(self):
        flag_sql = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.display.fill(GRIS)
            
            if not flag_sql:
                with sqlite3.connect(path.join("./src/basedatos", "bd_tetris.db")) as conexion:
                        flag_sql = True
                        try:
                            sentencia = ''' CREATE TABLE puntajes
                            (
                                id integer primary key autoincrement,
                                nombre text,
                                puntaje integer
                            )
                            '''
                            conexion.execute(sentencia)
                            print("Se creo la tabla de puntajes")
                        except sqlite3.OperationalError:
                            print("La tabla de puntajes ya estaba creada")
            
            self.juego.run()
            self.tablero.run()
            self.preview.run(self.formas_siguientes)
            self.puntajes.run()
            
            pygame.display.update()
            self.reloj.tick()
        
if __name__ == '__main__':
    main = Main()
    main.run()