from grafismo import *

def CargaSprites():
    
    global CeldasSprites
    CeldasSprites = []
    for i in range(0,9):
        
        for a in range(1,9):
                            
            CeldasSprites.append(pygame.image.load("SPRITES/ATOMO_"+str(i)+"_"+str(a)+".png"))
                
    return CeldasSprites

def CargaFondo():
    
    global Fondo
    Fondo = pygame.image.load("SPRITES/FONDO.png").convert_alpha()
    return Fondo

def CargaMenu():
    
    global Menu,Instrucciones
    Menu=pygame.image.load("SPRITES/MENU.png").convert_alpha()
    Instrucciones = pygame.image.load("SPRITES/INSTRUCCIONES.png").convert_alpha()
    return Menu,Instrucciones

def CargaTurno():
    
    global Turno
    Turno = []
    for i in range(1,3):
        
        Turno.append(pygame.transform.scale(pygame.image.load("SPRITES/TURNO_" + str(i) + ".png").convert_alpha(), (300, 300)))
    return Turno

def CargaGanador():
    
    global Ganador
    Ganador = []
    for i in range(0,5):
        
        Ganador.append(pygame.transform.scale(pygame.image.load("SPRITES/GANADOR_" + str(i) + ".png").convert_alpha(), (300, 300)))
    return Ganador
def CargaExplosion():
    
    global Explosion
    Explosion = []
    for i in range(1,9):
        
        Explosion.append(pygame.transform.scale(pygame.image.load("SPRITES/EXPLOSION_" + str(i) + ".png").convert_alpha(), (100, 100)))
    return Explosion

def CargaFx():
    FxExplosion = []
    Explosiones = ['Explosion1.wav','Explosion2.wav','Explosion3.wav','Explosion4.wav','Explosion5.wav','Explosion6.wav','Explosion7.wav']
    for Explosion in Explosiones:
        snd = pygame.mixer.Sound("AUDIOS/"+Explosion)
        FxExplosion.append(snd)
    
    Fallo = pygame.mixer.Sound("AUDIOS/Blip_Select1.wav")
    
    FxPone = []
    Pone = ['Jump1.wav','Jump2.wav']
    for Sonido in Pone:
        snd = pygame.mixer.Sound("AUDIOS/"+Sonido)
        FxPone.append(snd)
            
    return FxExplosion,Fallo,FxPone