import pygame

def EscribeTexto(pantalla,textos):
    
    font = textos[3]
    text_surface = font.render(textos[0], True, (100,255,0))
    text_shadow = font.render(textos[0], True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.center = (1180,443)
    text_shadow_pos = (text_rect[0]+2,text_rect[1]+2)
    pantalla.blit(text_shadow, text_shadow_pos)
    pantalla.blit(text_surface, text_rect)

    text_surface1 = font.render(textos[1], True, (0,100,255))
    text_shadow1 = font.render(textos[1], True, (0,0,0))
    text_rect1 = text_surface1.get_rect()
    text_rect1.center = (1180,540)
    text_shadow_pos1 = (text_rect1[0]+2,text_rect1[1]+2)
    pantalla.blit(text_shadow1, text_shadow_pos1)
    pantalla.blit(text_surface1, text_rect1)

    font = (textos[4])
    text_surface2 = font.render(textos[2]+" de 120", True, (255,100,0))
    text_shadow2 = font.render(textos[2]+" de 120", True, (0,0,0))
    text_rect2 = text_surface2.get_rect()
    text_rect2.center = (1180,608)
    text_shadow_pos2 = (text_rect2[0]+2,text_rect2[1]+2)
    pantalla.blit(text_shadow2, text_shadow_pos2)
    pantalla.blit(text_surface2, text_rect2)
                        
class pantallaJuego:
        
    def __init__(self):
       
        self.FPS = 160                                                   # Frames por segundo
        self.COLOR_FONDO = (0,0,0)                                      # Color de fondo de la pantalla
        self.ANCHO = 1300                                               # Ancho de la pantalla
        self.ALTO = 1100                                                # Alto de la pantalla
        self.MARGEN = 50
        pygame.mixer.pre_init(44100, -16, 2, 512)                  # Configuramos el mixer de pygame
        pygame.init()                                              # Inicializamos pygame 
        pygame.mixer.init()                                        # Inicializamos el mixer de pygame
        self.pantalla = pygame.display.set_mode((self.ANCHO,self.ALTO),pygame.NOFRAME)        # Creamos la pantalla
        
        self.reloj = pygame.time.Clock()                           # Creamos el reloj
        
    def ActualizaPantalla(self,Todos_los_sprites,Fondo,Fondo_rect,datosEscribe):
        
        Todos_los_sprites.update()                                                              # Actualizamos todos los sprites
        
        self.pantalla.blit(Fondo,Fondo_rect)                                                # Pintamos el fondo
        Todos_los_sprites.draw(self.pantalla)                                               # Pintamos todos los sprites
        EscribeTexto(self.pantalla,datosEscribe)                              # Escribimos el texto
        pygame.display.flip()                                                                   # Actualizamos la pantalla

class marcadorDeMaquina(pygame.sprite.Sprite):
    
    def __init__(self,Marcador,todos_los_sprites):
        
        pygame.sprite.Sprite.__init__(self)
        self.fotograma = 0
        self.image = Marcador[self.fotograma]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        todos_los_sprites.add(self)
    def NuevaPosicion(self,x,y):
        
        self.rect.x = x*100 + 50
        self.rect.y = y*100 + 50

class GraphCeldas(pygame.sprite.Sprite):
    
    def __init__(self,x,y,cantidad,fotograma,CeldasSprites,todos_los_sprites,margen):
                
        pygame.sprite.Sprite.__init__(self)
        self.cantidad = cantidad
        self.fotograma = fotograma
        self.image = CeldasSprites[self.cantidad+self.fotograma]
        self.rect = self.image.get_rect()
        self.rect.x = x*100 + margen
        self.rect.y = y*100 + margen
        
        todos_los_sprites.add(self)
    
class GraphTurno(pygame.sprite.Sprite):
    
    def __init__(self,Turno,todos_los_sprites):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = Turno[0]
        self.rect = self.image.get_rect()
        self.rect.x = 1030
        self.rect.y = 10
        todos_los_sprites.add(self)
        
class GraphGanador(pygame.sprite.Sprite):
    
    def __init__(self,Ganador,todos_los_sprites):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = Ganador[0]
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 421
        todos_los_sprites.add(self)
            
class CreaExplosion(pygame.sprite.Sprite):
    
    def __init__(self,x,y,Explosion,todos_los_sprites):
        
        pygame.sprite.Sprite.__init__(self)
        self.fotograma = 0
        self.image = Explosion[self.fotograma]
        self.rect = self.image.get_rect()
        self.rect.x = x*100+50
        self.rect.y = y*100+50
        todos_los_sprites.add(self)
        
