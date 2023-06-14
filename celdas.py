from grafismo import *
import os
from colorama import Back,Style,Fore
import random
from time import sleep

def CuentaAtomos():
    
    escarolitropicos,gmnesicos = 0,0
    
    for columna in range(10):
        for fila in range(10):
            if globals()['Celda_'+str(columna)+'_'+str(fila)].color == 1:
                 escarolitropicos += globals()['Celda_'+str(columna)+'_'+str(fila)].cantidad
            elif globals()['Celda_'+str(columna)+'_'+str(fila)].color == 2:
                gmnesicos += globals()['Celda_'+str(columna)+'_'+str(fila)].cantidad    
    return escarolitropicos,gmnesicos

def actualizaExplosiones(Todos_los_sprites,Explosion):
    recortes = 0
    for a in range(-1,12):
        for b in range(-1,12):
            try:
                globals()['Explosion_'+str(a)+"_"+str(b)].fotograma += 1
                if globals()['Explosion_'+str(a)+"_"+str(b)].fotograma >= 8 or globals()['Explosion_'+str(a)+"_"+str(b)].fotograma < 0 or globals()['Explosion_'+str(a)+"_"+str(b)].fotograma == None:
                    # Eliminamos el sprite del grupo
                    Todos_los_sprites.remove(globals()['Explosion_'+str(a)+"_"+str(b)])
                else:
                    globals()['Explosion_'+str(a)+"_"+str(b)].image = Explosion[globals()['Explosion_'+str(a)+"_"+str(b)].fotograma]
                    recortes += 1
            
                # Actualizamos el sprite
                globals()['Explosion_'+str(a)+"_"+str(b)].update()
                Todos_los_sprites.update()

            except:
                pass
    
    # Si Todos_los_sprites tiene más de 103 sprites, eliminamos el último
    if len(Todos_los_sprites) > 103 and recortes == 0:
        Todos_los_sprites.remove(Todos_los_sprites.sprites()[-1])
        
def cotejaGanador(PuedeRevisar,Jugadores,PackGanador,ronda):                                                                # Función que coteja si hay ganador
    if PuedeRevisar < 2:                                                                   # Si no se puede revisar
        return                                                                              # No hay ganador
    
    Color = [0,0]                                                                               # Lista que contiene el color del jugador 1 y 2

    for columna in range (10):
        for fila in range (10):    

            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 0:                       # Si Color es 0, seguimos
                continue
            elif globals()['Celda_'+str(columna)+"_"+str(fila)].color == 1:                     # Si Color es 1, lo sumamos en la lista
                Color[0] += globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad             # Sumamos la cantidad de átomos de la celda a la lista
            elif globals()['Celda_'+str(columna)+"_"+str(fila)].color == 2:                     # Si Color es 2, lo sumamos en la lista
                Color[1] += globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad             # Sumamos la cantidad de átomos de la celda a la lista

    if ((Color[0] != 0 and Color[1] != 0)  and ronda < 119) or (Color[0] == 0 and Color[1] == 0):     # Si hay átomos de los dos colores o no hay átomos
        return True                                                                             # No hay ganador
    
    elif (Color[1] == 0 and ronda > 1) or (ronda == 119 and Color[1] < Color[0] and Jugadores[1].turno == True):                                                                         # Si no hay átomos del jugador 1
        PackGanador[0].image = PackGanador[1][1]                                                              # Gana el jugador 2 
        Jugadores[1].EnJuego = False                                                                            # Si hay ganador
        Jugadores[0].EnJuego = False
    elif (Color[0] == 0 and ronda > 1) or (ronda == 119 and Color[0] < Color[1] and Jugadores[1].turno == True):                                                                         # Si no hay átomos del jugador 2
        if Jugadores[1].tipo == 0:                                                              # Si el jugador 2 es humano
            
            PackGanador[0].image = PackGanador[1][2]                                            # Gana el jugador 2
        
        else:                                                                                   # Si el jugador 2 es máquina
            
            PackGanador[0].image = PackGanador[1][3]                                            # Gana la máquina
        Jugadores[0].EnJuego = False
        Jugadores[1].EnJuego = False
    elif ronda == 119 and Color[1] == Color[0] and Jugadores[1].turno == True:
        PackGanador[0].image = PackGanador[1][4]
        Jugadores[0].EnJuego = False
        Jugadores[1].EnJuego = False
        
def CreaCeldas(CeldasSprites,todos_los_sprites):

    for columna in range (10):
        for fila in range (10):

            globals()['Celda_'+str(columna)+"_"+str(fila)] = Celdas(columna,fila,4,CeldasSprites)             # Creamos una variable compuesta por la palabra "celda" y la columna y la fila

            if (columna == 0 or columna == 9 or fila == 0 or fila == 9):                        # Las aristas con capacidad 3
                globals()['Celda_'+str(columna)+"_"+str(fila)].capacidad = 3
            if ((columna == fila == 0) or (columna == fila == 9) or 
                (columna == 0 and fila == 9) or (columna == 9 and fila == 0)):                  # Ls vértices con capacidad 2
                globals()['Celda_'+str(columna)+"_"+str(fila)].capacidad = 2
            
            globals()['CeldaG_'+str(columna)+"_"+str(fila)] = GraphCeldas(globals()['Celda_'+
                    str(columna)+"_"+str(fila)].coordenadas[0],globals()['Celda_'+
                    str(columna)+"_"+str(fila)].coordenadas[1],globals()['Celda_'+
                    str(columna)+"_"+str(fila)].cantidad,globals()['Celda_'+
                    str(columna)+"_"+str(fila)].fotograma,CeldasSprites,todos_los_sprites,globals()['Celda_'+str(columna)+"_"+str(fila)].MARGEN)                                      # Creamos una variable compuesta por la palabra "celda" y la columna y la fila

def LlamaCelda(a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda):                                                                      # Función que llama a la celda que se le pasa por parámetro
    
    cambio = globals()['Celda_'+str(a)+"_"+str(b)].IntroduceAtomo(a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)                             # Llamamos a la función IntroduceAtomo de la celda que se le pasa por parámetro
    return cambio
def LlamaCeldaJuega(a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,time,MarcaMaquina,ronda):

    if Jugadores[1].tipo == 1 and Jugadores[0].turno == False:
        
        a,b = InteligenciaArtificial()                                          # Llamamos a la función IntroduceAtomo de la celda que se le pasa por parámetro
        MarcaMaquina.NuevaPosicion(a,b)
        MarcaMaquina.update()
        
    cambio = globals()['Celda_'+str(a)+"_"+str(b)].Juega(a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)                             # Llamamos a la función IntroduceAtomo de la celda que se le pasa por parámetro
    if Jugadores[1].tipo == 1 and Jugadores[0].turno == True:
        time = pygame.time.get_ticks()
    return cambio,time

def InteligenciaArtificial():
    PuedeRegresar = False
        
    # 1 - Casillas de máxima capacidad 2 que estén vacías
    for columna in range (10):
        for fila in range (10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].capacidad == 2 and globals()['Celda_'+str(columna)+"_"+str(fila)].color == 0:
                return columna,fila
    
    # 2 - Casillas del color 2 con 1 átomo menos de su capacidad máxima y colindantes a casillas del color 1 con 1 átomo menos de su capacidad máxima
    for columna in range (10):
        for fila in range (10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 2 and globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad == globals()['Celda_'+str(columna)+"_"+str(fila)].capacidad-1:
                if columna > 0:
                    if globals()['Celda_'+str(columna-1)+"_"+str(fila)].color == 1 and globals()['Celda_'+str(columna-1)+"_"+str(fila)].cantidad == globals()['Celda_'+str(columna-1)+"_"+str(fila)].capacidad-1:
                        return columna,fila
                if columna < 9:
                    if globals()['Celda_'+str(columna+1)+"_"+str(fila)].color == 1 and globals()['Celda_'+str(columna+1)+"_"+str(fila)].cantidad == globals()['Celda_'+str(columna+1)+"_"+str(fila)].capacidad-1:
                        return columna,fila                
                if fila < 9:
                    if globals()['Celda_'+str(columna)+"_"+str(fila+1)].color == 1 and globals()['Celda_'+str(columna)+"_"+str(fila+1)].cantidad == globals()['Celda_'+str(columna)+"_"+str(fila+1)].capacidad-1:
                        return columna,fila                     
                if fila > 0:
                    if globals()['Celda_'+str(columna)+"_"+str(fila-1)].color == 1 and globals()['Celda_'+str(columna)+"_"+str(fila-1)].cantidad == globals()['Celda_'+str(columna)+"_"+str(fila-1)].capacidad-1:
                        return columna,fila   
    
    # 3 - Casilla del color 2 que alguna de sus casillas colindantes sean de color 1 y con menos átomos que la casilla de color 2 pero que no tenga ninguna casilla colindante de color 1 con más átomos que la casilla de color 2
    for columna in range (10):
        for fila in range(10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 2:
                posibilidades = 0
                if columna > 0:
                    if globals()['Celda_'+str(columna-1)+"_"+str(fila)].color == 1 and globals()['Celda_'+str(columna-1)+"_"+str(fila)].cantidad < globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:
                        posibilidades += 1
                    elif globals()['Celda_'+str(columna-1)+"_"+str(fila)].color == 1 and globals()['Celda_'+str(columna-1)+"_"+str(fila)].cantidad > globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:
                        posibilidades += 40
                if columna < 9:
                    if globals()['Celda_'+str(columna+1)+"_"+str(fila)].color == 1 and globals()['Celda_'+str(columna+1)+"_"+str(fila)].cantidad < globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:
                        posibilidades += 1
                    elif globals()['Celda_'+str(columna+1)+"_"+str(fila)].color == 1 and globals()['Celda_'+str(columna+1)+"_"+str(fila)].cantidad > globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:
                        posibilidades += 40
                if fila < 9:
                    if globals()['Celda_'+str(columna)+"_"+str(fila+1)].color == 1 and globals()['Celda_'+str(columna)+"_"+str(fila+1)].cantidad < globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:
                        posibilidades += 1
                    elif globals()['Celda_'+str(columna)+"_"+str(fila+1)].color == 1 and globals()['Celda_'+str(columna)+"_"+str(fila+1)].cantidad > globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:   
                        posibilidades += 40
                if fila > 0:
                    if globals()['Celda_'+str(columna)+"_"+str(fila-1)].color == 1 and globals()['Celda_'+str(columna)+"_"+str(fila-1)].cantidad < globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:
                        posibilidades += 1
                    elif globals()['Celda_'+str(columna)+"_"+str(fila-1)].color == 1 and globals()['Celda_'+str(columna)+"_"+str(fila-1)].cantidad > globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad:   
                        posibilidades += 40
                if 0 < posibilidades < 40:
                    return columna,fila
    # 4 - Casillas de color 2 que tengan menos átomos que su capacidad máxima menos 2
    for columna in range (10):
        for fila in range (10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 2 and globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad <= globals()['Celda_'+str(columna)+"_"+str(fila)].capacidad-3:
                return columna,fila
    # 5 - Casillas de color 2 que de color 0 y que alguna de las casillas colindantes sean de color 2 y con menos átomos que su capacidad máxima menos 2
    for columna in range (10):
        for fila in range (10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 0:
                if columna > 0:
                    if globals()['Celda_'+str(columna-1)+"_"+str(fila)].color == 2 and globals()['Celda_'+str(columna-1)+"_"+str(fila)].cantidad <= globals()['Celda_'+str(columna-1)+"_"+str(fila)].capacidad-3:
                        return columna,fila
                if columna < 9:
                    if globals()['Celda_'+str(columna+1)+"_"+str(fila)].color == 2 and globals()['Celda_'+str(columna+1)+"_"+str(fila)].cantidad <= globals()['Celda_'+str(columna+1)+"_"+str(fila)].capacidad-3:
                        return columna,fila                
                if fila < 9:
                    if globals()['Celda_'+str(columna)+"_"+str(fila+1)].color == 2 and globals()['Celda_'+str(columna)+"_"+str(fila+1)].cantidad <= globals()['Celda_'+str(columna)+"_"+str(fila+1)].capacidad-3:
                        return columna,fila                     
                if fila > 0:
                    if globals()['Celda_'+str(columna)+"_"+str(fila-1)].color == 2 and globals()['Celda_'+str(columna)+"_"+str(fila-1)].cantidad <= globals()['Celda_'+str(columna)+"_"+str(fila-1)].capacidad-3:
                        return columna,fila
    # 6 - Casilla de color 0 que sus casillas colindates sean de color 0
    for columna in range (10):
        for fila in range (10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 0:
                if columna > 0:
                    if globals()['Celda_'+str(columna-1)+"_"+str(fila)].color == 0:
                        break
                if columna < 9:
                    if globals()['Celda_'+str(columna+1)+"_"+str(fila)].color == 0:
                        break                
                if fila < 9:
                    if globals()['Celda_'+str(columna)+"_"+str(fila+1)].color == 0:
                        break                     
                if fila > 0:
                    if globals()['Celda_'+str(columna)+"_"+str(fila-1)].color == 0:
                        break
                return columna,fila   
            
    # 7 - Casillas de color 2 con menos átomos que su capacidad máxima menos 2
    for columna in range (10):
        for fila in range (10):
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 2 and globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad <= globals()['Celda_'+str(columna)+"_"+str(fila)].capacidad-3:
                return columna,fila
                                                   
    # 8 - Cualquier celda    
    while not PuedeRegresar:
        a = random.randint(0,9)
        b = random.randint(0,9)
        if globals()['Celda_'+str(a)+"_"+str(b)].color != 1:
            PuedeRegresar = True
    return a,b

def Animacion(Explosion,Pantalla,Fondo,Fondo_rect,Todos_los_sprites):        
        
    for columna in range (10):
        for fila in range (10):
                    
            extra = 0
            if globals()['Celda_'+str(columna)+"_"+str(fila)].color == 2:
                extra = 4*8
            
            a = pygame.time.get_ticks() - globals()['Celda_'+str(columna)+"_"+str(fila)].time
            b = globals()['Celda_'+str(columna)+"_"+str(fila)].cantidad
                    
            if ((a > 500 and b == 1) or (a > 250 and b == 2) or (a > 125 and b == 3) or (a > 50 and b == 0)) or (Explosion == True):
                        
                globals()['Celda_'+str(columna)+"_"+str(fila)].fotograma += 1
                globals()['CeldaG_'+str(columna)+"_"+str(fila)].fotograma += 1
                        
                if globals()['Celda_'+str(columna)+"_"+str(fila)].fotograma > 7:
                            
                    globals()['Celda_'+str(columna)+"_"+str(fila)].fotograma = 0  
                    globals()['CeldaG_'+str(columna)+"_"+str(fila)].fotograma = 0  
                globals()['CeldaG_'+str(columna)+"_"+str(fila)].image = globals()['Celda_'+str(columna)+"_"+str(fila)].CeldasSprites[(globals()['CeldaG_'+str(columna)+"_"+str(fila)].cantidad*8)+globals()['CeldaG_'+str(columna)+"_"+str(fila)].fotograma+extra]
                
                if ((a > 500 and b == 1) or (a > 250 and b == 2) or (a > 125 and b == 3) or (a > 50 and b == 0)):        
                    globals()['Celda_'+str(columna)+"_"+str(fila)].time = pygame.time.get_ticks()
                        
       
    Todos_los_sprites.update()
    Pantalla.pantalla.blit(Fondo, Fondo_rect)
    Todos_los_sprites.draw(Pantalla.pantalla)
class Celdas:                                                                                   # Clase celdas
    
    def __init__(self,x,y,capacidad,CeldasSprites):
        
        self.coordenadas    = [x,y]                                                             # Coordenadas de la celda
        self.capacidad      = capacidad                                                         # Capacidad de átomos la celda
        self.color          = 0                                                                 # Color de la celda entre amarillo y negro 0,1,2
        self.cantidad       = 0                                                                 # Cantidad de átomos que tiene -4 a 4 (negros,nada,amarillos)
        self.fotograma      = random.randint(0,7)                                               # Fotograma de los 8
        self.MARGEN         = 50                                                                # Margen a la hora de pintar
        self.CeldasSprites  = CeldasSprites
        self.time           =  pygame.time.get_ticks()
          
    def IntroduceAtomo(self,a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda):                                                         # Pone un átomo en la celda escogida
        
        if self.color == 0 or (self.color == Jugadores[0].color and Jugadores[0].turno == True) or (self.color != Jugadores[0].color and Jugadores[0].turno == False):                                              # Si coincide en color o está vacía
            
            if Jugadores[0].turno == False:
                self.color = 2
                Sounds[2][1].play()
            else:
                self.color = 1
                Sounds[2][0].play()
            extra = 0
            if self.color == 2:
                extra+= 4*8    
            self.cantidad   += 1                                                            # Añade
            globals()['CeldaG_'+str(a)+"_"+str(b)].cantidad =self.cantidad
            globals()['CeldaG_'+str(a)+"_"+str(b)].image = self.CeldasSprites[self.cantidad*8+self.fotograma+extra]

            if self.cantidad == self.capacidad and Jugadores[0].EnJuego == True and Jugadores[1].EnJuego == True:                                             # Si ya no caben más
                          
                # Actualizamos la pantalla
                globals()['Explosion_'+str(a)+"_"+str(b)] = CreaExplosion(self.coordenadas[0],self.coordenadas[1],Explosion,Todos_los_sprites)
                pygame.display.update()                                                    # Actualizamos la pantalla
                
                Animacion(True,Pantalla,Fondo,Fondo_rect,Todos_los_sprites)
                random.choice(Sounds[0]).play()
                globals()['CeldaG_'+str(a)+"_"+str(b)].cantidad =0
                globals()['CeldaG_'+str(a)+"_"+str(b)].image = self.CeldasSprites[0]
                self.Explota(a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)                                                         # Debe explotar
            
            cotejaGanador(PuedeRevisar,Jugadores,PackGanador,ronda)
            return True
        else:                                                                                   # Si está ocupada por el enemigo
            
            Sounds[1].play()
            return False                                                                             # Salimos de la función
        
    def Explota(self,a,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda):                                                                # Gestiona la explosión
        
        sleep(0.05)       

        self.cantidad   = 0                                                                     # Vaciamos la celda
        self.color      = 0                                                                     # la dejamos neutra de color  
                 
        actualizaExplosiones(Todos_los_sprites,Explosion)                                       # Actualizamos las explosiones
     
        if int(a) > 0:
            ax = int(a)-1
            globals()['Celda_'+str(ax)+"_"+str(b)].CambioColor(Jugadores)
            globals()['Celda_'+str(ax)+"_"+str(b)].IntroduceAtomo(ax,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)
        if int(a) < 9:
            ax = int(a)+1
            globals()['Celda_'+str(ax)+"_"+str(b)].CambioColor(Jugadores)
            globals()['Celda_'+str(ax)+"_"+str(b)].IntroduceAtomo(ax,b,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)
        if int(b) > 0:
            bx = int(b)-1
            globals()['Celda_'+str(a)+"_"+str(bx)].CambioColor(Jugadores)
            globals()['Celda_'+str(a)+"_"+str(bx)].IntroduceAtomo(a,bx,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)
        if int(b) < 9:
            bx = int(b)+1
            globals()['Celda_'+str(a)+"_"+str(bx)].CambioColor(Jugadores)
            globals()['Celda_'+str(a)+"_"+str(bx)].IntroduceAtomo(a,bx,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)

    def Juega(self,x,y,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda):
        
        cambio = LlamaCelda(x,y,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,ronda)
        return cambio
    def CambioColor(self,Jugadores):                                                                # Cambia el color de la celda
        
        if Jugadores[0].turno == True:                                                                  # Si es el turno del jugador 1
            self.color = 1                                                                      # Le damos el color que se le pasa por parámetro
        else:
            self.color = 2                                                                      # Si no, le damos el color del jugador 2
            
class jugador:
    
    def __init__(self,color,turno,playerType):                          # Constructor de la clase jugador
        
        self.color      = color                                         # Color del jugador
        self.cantidad   = 0                                             # Cantidad de átomos que tiene
        self.tipo       = playerType                                    # Tipo de jugador       
        self.EnJuego    = True                                          # Si está en juego o no
        self.turno      = turno                                         # Si es su turno o no
        self.atomos     = 0                                             # Cantidad de átomos que tiene            
