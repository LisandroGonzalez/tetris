from settings import *
from random import choice
from timer import Timer
from os import path
from sys import exit

class Juego:
    def __init__(self, obtener_forma_siguiente, actualizar_tablero):
        self.superficie = pygame.Surface((ANCHO_JUEGO, ALTURA_JUEGO))
        self.superficie_display = pygame.display.get_surface()
        self.rect = self.superficie.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()
        
        self.obtener_forma_siguiente = obtener_forma_siguiente
        self.actualizar_tablero = actualizar_tablero
        
        self.superficie_linea = self.superficie.copy()
        self.superficie_linea.fill(VERDE)
        self.superficie_linea.set_colorkey(VERDE)
        self.superficie_linea.set_alpha(120)
        
        self.data_campo = [[0 for x in range(COLUMNAS)] for y in range(FILAS)]
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites, self.crear_tetromino, self.data_campo)    
        
        self.velocidad_bajada = ACTUALIZAR_VELOCIDAD_PRINCIPIO
        self.inc_velocidad_bajada = self.velocidad_bajada * 0.3
        self.abajo_presionada = False
        self.timers = {
            'movimiento_vertical': Timer(ACTUALIZAR_VELOCIDAD_PRINCIPIO, True, self.movimiento_descendente),
            'movimiento_horizontal': Timer(TIEMPO_ESPERA_MOVER),
            'rotar': Timer(TIEMPO_ESPERA_ROTAR)
        }
        self.timers['movimiento_vertical'].activar()
        
        self.nivel_actual = 1
        self.puntaje_actual = 0
        self.lineas_actuales = 0
        self.nombre_jugador = "LISANDRO GONZALEZ"
        
    def calculo_tablero(self, num_lineas):
        self.lineas_actuales += num_lineas
        self.puntaje_actual += DATA_PUNTAJE[num_lineas] * self.nivel_actual
        
        if self.lineas_actuales / 10 > self.nivel_actual and self.nivel_actual <= 3:
            self.nivel_actual += 1
            self.velocidad_bajada += 1
            self.inc_velocidad_bajada = self.velocidad_bajada * 0.5
            self.timers['movimiento_vertical'].duracion = self.velocidad_bajada
        
        self.actualizar_tablero(self.lineas_actuales, self.puntaje_actual, self.nivel_actual)
    
    def chequear_si_perdiste(self):
        for bloque in self.tetromino.bloques:
            if bloque.posicion.y < 0:
                with sqlite3.connect(path.join("./src/basedatos", "bd_tetris.db")) as conexion:
                    try:
                        conexion.execute("INSERT INTO puntajes(nombre, puntaje) VALUES (?,?)", (self.nombre_jugador, self.puntaje_actual))
                        conexion.commit()
                        print(f"Se guardo el puntaje de {self.nombre_jugador} exitosamente.")
                    except:
                        print("Error al cargar el puntaje en la base de datos.")
                exit()
    
    def crear_tetromino(self):
        self.chequear_si_perdiste()
        self.filas_completas()
        
        self.tetromino = Tetromino(self.obtener_forma_siguiente(), self.sprites, self.crear_tetromino, self.data_campo)
    
    def actualizar_timer(self):
        for timer in self.timers.values():
            timer.update()
        
    def movimiento_descendente(self):
        self.tetromino.movimiento_descendente()
        
    def dibujar_cuadricula(self):
        for columna in range(1, COLUMNAS):
            x = columna * TAM_CELDA
            pygame.draw.line(self.superficie_linea, BLANCO, (x,0), (x, self.superficie.get_height()), 1)
            
        for fila in range(1, FILAS):
            y = fila * TAM_CELDA
            pygame.draw.line(self.superficie_linea, BLANCO, (0,y), (self.superficie.get_width(), y), 1)
        
        self.superficie.blit(self.superficie_linea, (0,0))
      
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers['movimiento_horizontal'].activo:
            if keys[pygame.K_LEFT]:
                self.tetromino.mover_horizontalmente(-1)
                self.timers['movimiento_horizontal'].activar()
            if keys[pygame.K_RIGHT]:
                self.tetromino.mover_horizontalmente(1)
                self.timers['movimiento_horizontal'].activar()
                
        if not self.timers['rotar'].activo:
            if keys[pygame.K_UP]:
                self.tetromino.rotar()
                self.timers['rotar'].activar()
                
        if not self.abajo_presionada and keys[pygame.K_DOWN]:
            self.abajo_presionada = True
            self.timers['movimiento_vertical'].duracion = self.inc_velocidad_bajada
            
        if self.abajo_presionada and not keys[pygame.K_DOWN]:
            self.abajo_presionada = False
            self.timers['movimiento_vertical'].duracion = self.velocidad_bajada
      
    def filas_completas(self):
        filas_eliminadas = []
        for i,fila in enumerate(self.data_campo):
            if all(fila):
                filas_eliminadas.append(i)
                
        if filas_eliminadas:
            for fila_eliminar in filas_eliminadas:
                for bloque in self.data_campo[fila_eliminar]:
                    bloque.kill()
                    
                for fila in self.data_campo:
                    for bloque in fila:
                        if bloque and bloque.posicion.y < fila_eliminar:
                            bloque.posicion.y += 1
                            
            self.data_campo = [[0 for x in range(COLUMNAS)] for y in range(FILAS)]
            for bloque in self.sprites:
                self.data_campo[int(bloque.posicion.y)][int(bloque.posicion.x)] = bloque
        
            self.calculo_tablero(len(filas_eliminadas))
    
    def run(self):
        self.input()
        self.actualizar_timer()
        self.sprites.update()
        
        self.superficie.fill(GRIS)
        self.sprites.draw(self.superficie)
        
        self.dibujar_cuadricula()
        self.superficie_display.blit(self.superficie, (PADDING,PADDING))
        pygame.draw.rect(self.superficie_display, BLANCO, self.rect, 4,4)
      
class Tetromino:
    def __init__(self, forma, grupo, crear_tetromino, data_campo):
        self.forma = forma
        self.posiciones_bloque = TETROMINOS[forma]['forma']
        self.color = TETROMINOS[forma]['color']
        self.crear_tetromino = crear_tetromino
        self.data_campo = data_campo
        
        self.bloques = [Bloque(grupo, posicion, self.color) for posicion in self.posiciones_bloque]
        
    def hay_colision_horizontal(self, bloques, cantidad):
        colisiones = [bloque.colision_horizontal(int(bloque.posicion.x + cantidad), self.data_campo) for bloque in self.bloques]
        if any(colisiones):
            return True
        else:
            return False
        
    def hay_colision_vertical(self, bloques, cantidad):
        colisiones = [bloque.colision_vertical(int(bloque.posicion.y + cantidad), self.data_campo) for bloque in self.bloques]
        if any(colisiones):
            return True
        else:
            return False
        
    def mover_horizontalmente(self, cantidad):
        if not self.hay_colision_horizontal(self.bloques, cantidad):
            for bloque in self.bloques:
                bloque.posicion.x += cantidad
        
    def movimiento_descendente(self):
        if not self.hay_colision_vertical(self.bloques, 1):
            for bloque in self.bloques:
                bloque.posicion.y += 1
        else:
            for bloque in self.bloques:
                self.data_campo[int(bloque.posicion.y)][int(bloque.posicion.x)] = bloque
            self.crear_tetromino()
  
    def rotar(self):
        if self.forma != 'O':
            posicion_pivot = self.bloques[0].posicion
            
            posicion_nueva = [bloque.rotar(posicion_pivot) for bloque in self.bloques]
            
            for posicion in posicion_nueva:
                if posicion.x < 0 or posicion.x >= COLUMNAS:
                    return
                if self.data_campo[int(posicion.y)][int(posicion.x)]:
                    return
                if posicion.y > FILAS:
                    return
            
            for i, bloque in enumerate(self.bloques):
                bloque.posicion = posicion_nueva[i]

class Bloque(pygame.sprite.Sprite):
    def __init__(self, grupo, posicion, color):
        super().__init__(grupo)
        self.image = pygame.Surface((TAM_CELDA, TAM_CELDA))
        self.image.fill(color)
        
        self.posicion = pygame.Vector2(posicion) + OFFSET_BLOQUE
        x = self.posicion.x * TAM_CELDA
        y = self.posicion.y * TAM_CELDA
        self.rect = self.image.get_rect(topleft = (x,y))
        
    def rotar(self, posicion_pivot):
        distancia = self.posicion - posicion_pivot
        rotado = distancia.rotate(90)
        posicion_nueva = posicion_pivot + rotado
        return posicion_nueva
        
    
    def colision_horizontal(self, x, data_campo):
        if not 0 <= x < COLUMNAS:
            return True
        
        if data_campo[int(self.posicion.y)][x]:
            return True
        
    def colision_vertical(self, y, data_campo):
        if  y >= FILAS:
            return True
        
        if y >= 0 and data_campo[y][int(self.posicion.x)]:
            return True
        
    def update(self):
        self.rect.topleft = self.posicion * TAM_CELDA