import sys
from celdas import *                                                                            # Importamos la clase celdas                                    
from grafismo import *                                                                          # Importamos la clase pantallaJuego
from cargas import *                                                                            # Importamos la función CargaSprites

def main():                                                                                     # Empieza el juego
    
    global PuedeRevisar
    global partida
    
    sys.setrecursionlimit(10000)                                                                # Aumentamos el límite de recursividad

    partida = True
    salida = False
    PuedeRevisar = 0
    
    Pantalla = pantallaJuego()                                                                  # Creamos la pantalla
    CeldasSprites = CargaSprites()                                                              # Cargamos los sprites
    Menu,Instrucciones = CargaMenu()                                                            # Cargamos el fondo
    Menu_rect = Menu.get_rect()                                                                 # Obtenemos el rectángulo del fondo
    Instrucciones_rect = Instrucciones.get_rect()                                               # Obtenemos el rectángulo del fondo
    
    Turno = CargaTurno()                                                                        # Cargamos el turno
    Ganador = CargaGanador()                                                                    # Cargamos el ganador
    Explosion = CargaExplosion()                                                                # Cargamos la explosión
    
    Todos_los_sprites = pygame.sprite.Group()                                                   # Creamos el grupo de sprites
    CreaCeldas(CeldasSprites,Todos_los_sprites)                                                 # Creamos las celdas
    TurnoReal = GraphTurno(Turno,Todos_los_sprites)                                             # Creamos el turno 
    GanadorReal = GraphGanador(Ganador,Todos_los_sprites)                                       # Creamos el ganador
    PackGanador= [GanadorReal,Ganador]                                                          # Creamos una lista con el ganador
    
    FxExplosion,Fallo,Pone = CargaFx()                                                          # Cargamos el sonido de explosión
    Sounds = [FxExplosion,Fallo,Pone]                                                           # Creamos una lista con los sonidos
    pygame.mixer.music.load("AUDIOS/BANDA_SONORA.wav")                                          # Cargamos la música
    pygame.mixer.music.set_volume(1.05)                                                         # Ajustamos el volumen
    pygame.mixer.music.play(loops = -1)                                                         # Reproducimos la música
    
    menu = True
    estado = 0
    segundoJugador = 0
    rondas = 0
    escarolitropicos = 0
    gmnesicos = 0
    
    while menu:
        Pantalla.reloj.tick(Pantalla.FPS)                                                       # Limitamos la velocidad de la pantalla a 60 fps

        # Eventos
        for evento in pygame.event.get():
            # Si se pulsa la tecla esc
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                partida = False
                salida = True
                menu = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:                    # Mientras no pulse el ratón
                
                if estado == 0: 
                    # Obtenemos la posición del ratón
                    pos = pygame.mouse.get_pos()                                                # Obtenemos la posición del ratón
                    if pos[0] > 63 and pos[0] < 274 and pos[1] > 22 and pos[1] < 325:            # Si se pulsa instrucciones
                        estado = 1
                    elif pos[0] > 96 and pos[0] < 769 and pos[1] > 514 and pos[1] < 703:       # Si se pulsa player versus player
                        segundoJugador = 0                        
                        menu = False
                    elif pos[0] > 96 and pos[0] < 744 and pos[1] > 829 and pos[1] < 1020:       # Si se pulsa player versus machine
                        segundoJugador = 1                        
                        menu = False    
                        
                else: estado = 0
                
        if estado == 0:
            Pantalla.pantalla.blit(Menu,Menu_rect)                                                # Pintamos el fondo                
        else:
            Pantalla.pantalla.blit(Instrucciones,Instrucciones_rect)                                                # Pintamos el fondo
            
        pygame.display.flip()                                                                   # Actualizamos la pantalla
        
    Fondo = CargaFondo()                                                                        # Cargamos el fondo
    Fondo_rect = Fondo.get_rect()                                                               # Obtenemos el rectángulo del fondo    
    Jug1 = jugador(1,True,0)                                                                    # Creamos el jugador 1
    Jug2 = jugador(2,False,segundoJugador)                                                      # Creamos el jugador 2
    Jugadores = [Jug1,Jug2]                                                                     # Creamos una lista con los jugadores
    time = pygame.time.get_ticks()                                                              # Obtenemos el tiempo actual
    MarcaMaquina = None
    
    fuente = pygame.font.Font('FONTS/SF Toontime Bold.ttf',50)                                   # Cargamos la fuente
    fuente2 = pygame.font.Font('FONTS/SF Toontime Bold.ttf',30)                                  # Cargamos la fuente
    
    if Jugadores[1].tipo == 1:                                                                  # Si el jugador 2 es de tipo 1
        Marcador = []                                                                           # Creamos una lista vacía
        for i in range(1,10):                                                                   # Creamos 9 marcadores
            Marcador.append(pygame.image.load("SPRITES/MARCADOR_"+str(i)+".png").convert_alpha())          # Cargamos el sprite marcador
        MarcaMaquina = marcadorDeMaquina(Marcador,Todos_los_sprites)                            # Creamos el marcador de la máquina
            
    while partida:
        
        Pantalla.reloj.tick(Pantalla.FPS)                                                       # Limitamos la velocidad de la pantalla a 60 fps
        
        if pygame.time.get_ticks() - time < 1000:
            pass
        
        else:        
            if Jugadores[0].EnJuego == False or Jugadores[1].EnJuego == False:
                for evento in pygame.event.get():
                    # Elimina todos los sprites Explosión de la pantalla
                    for columna in range(10):
                        for fila in range(10):
                            try:
                                globals()['Explosion_'+str(columna)+'_'+str(fila)].kill()
                            except:
                                pass
                            
                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:                    # Mientras no pulse el ratón

                        partida = False 
        
            if Jugadores[0].turno == False and Jugadores[1].tipo == 1 and Jugadores[0].EnJuego == True and Jugadores[1].EnJuego == True :                                        # Si el turno es del jugador 2 y es de tipo 1
                
    
                cambio,time = LlamaCeldaJuega(xCelda,yCelda,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,time,MarcaMaquina,rondas)# Llamamos a la función Juega de la celda en la que se ha pulsado
                rondas += 1
                Jugadores[0].turno = True
                Jugadores[1].turno = False
                TurnoReal.image = Turno[0]

            # Eventos
            for evento in pygame.event.get():
                # Si se pulsa la tecla esc
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    partida = False
                    salida = True
                
                # Si el evento es boton izquierdo del ratón pulsado
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        
                        pos = pygame.mouse.get_pos()                                                # Obtenemos la posición del ratón

                        xCelda = int((pos[0]-50)/100)                                               # Obtenemos la celda en la que se ha pulsado
                        yCelda = int((pos[1]-50)/100)                                               # Obtenemos la celda en la que se ha pulsado
                        if yCelda < 0 or yCelda > 9 or xCelda < 0 or xCelda > 9:
                            break
                        cambio = True
                        cambio,time = LlamaCeldaJuega(xCelda,yCelda,Jugadores,Pantalla,Fondo,Fondo_rect,Todos_los_sprites,PuedeRevisar,Sounds,PackGanador,Explosion,time,MarcaMaquina,rondas)                                         # Llamamos a la función Juega de la celda en la que se ha pulsado
                        if cambio == True:
                        
                            PuedeRevisar += 1
                            if Jugadores[0].turno == True:
                                Jugadores[0].turno = False
                                Jugadores[1].turno = True
                                TurnoReal.image = Turno[1]
                            else:
                                Jugadores[0].turno = True
                                Jugadores[1].turno = False
                                TurnoReal.image = Turno[0]
                                rondas += 1
                            
        actualizaExplosiones(Todos_los_sprites,Explosion)
        escarolitropicos,gmnesicos = CuentaAtomos()
                
        if Jugadores[1].tipo == 1:
            MarcaMaquina.fotograma += 1
            if MarcaMaquina.fotograma > 8:
                MarcaMaquina.fotograma = 0
            MarcaMaquina.image = Marcador[MarcaMaquina.fotograma]    
            MarcaMaquina.update()   
        Animacion(False,Pantalla,Fondo,Fondo_rect,Todos_los_sprites)           
        datosEscribe = [str(escarolitropicos),str(gmnesicos),str(rondas),fuente,fuente2]
        Pantalla.ActualizaPantalla(Todos_los_sprites,Fondo,Fondo_rect,datosEscribe)                          # Actualizamos la pantalla
        
    pygame.quit()                                                                               # Salimos de pygame
    
    if salida == True:
        sys.exit(0)                                                                              # Salimos del programa
    main()
    
if __name__ == '__main__':                                                                      # Si se ejecuta este archivo, se ejecuta la función main()
        
     main()                                                                                      # Llamada a la función main()                                 
