import pygame, sys, random

def dibujar_suelo():
    pantalla.blit(suelo_superficie,(suelo_pos_x,suelo_pos_y))
    pantalla.blit(suelo_superficie,(suelo_pos_x + 576,suelo_pos_y))

def crear_tuberia():
    random_posicion_tuberia = random.choice(tuberia_altura)
    tuberia_inferior = tuberia_superficie.get_rect(midtop = (700,random_posicion_tuberia))
    tuberia_superior = tuberia_superficie.get_rect(midbottom = (700,random_posicion_tuberia - 300))
    return tuberia_inferior, tuberia_superior

def movimiento_tuberias(tuberias):
    for tuberia in tuberias:
        tuberia.centerx -= 5
    return tuberias

def dibujar_tuberias(tuberias):
    for tuberia in tuberias:
        if tuberia.bottom >= 1024:
            pantalla.blit(tuberia_superficie,tuberia)
        else:
            voltear_tuberia = pygame.transform.flip(tuberia_superficie,False,True)
            pantalla.blit(voltear_tuberia,tuberia)

def comprobar_colision(tuberias):
    for tuberia in tuberias:
        if pajaro_rectangulo.colliderect(tuberia):
            sonido_muerte.play()
            return False
    
    if pajaro_rectangulo.top <= 0: 
        sonido_muerte.play()
        return False
    
    if pajaro_rectangulo.bottom >=900:
        sonido_muerte.play()
        return False

    return True

def rotar_pajaro(pajaro):
    nuevo_pajaro = pygame.transform.rotozoom(pajaro,-pajaro_movimiento * 3,1)
    return nuevo_pajaro

def animacion_pajaro():
    nuevo_pajaro = pajaro_frames[indice_pajaro]
    nuevo_pajaro_rectangulo = nuevo_pajaro.get_rect(center = (100,pajaro_rectangulo.centery))
    return nuevo_pajaro, nuevo_pajaro_rectangulo    

def mostrar_puntuacion(estado_juego):
    if estado_juego == 'Juego_Principal':
        puntuacion_superficie = fuente_juego.render(str(int(puntuacion)),True,(255,255,255))
        puntuacion_rectangulo = puntuacion_superficie.get_rect(center = (288,100))
        pantalla.blit(puntuacion_superficie,puntuacion_rectangulo)
    if estado_juego == 'Fin_Juego':
        puntuacion_superficie = fuente_juego.render(f'Score: {int(puntuacion)}',True,(255,255,255))
        puntuacion_rectangulo = puntuacion_superficie.get_rect(center = (288,100))
        pantalla.blit(puntuacion_superficie,puntuacion_rectangulo)

        alta_puntuacion_superficie = fuente_juego.render(f'High Score: {int(alta_puntuacion)}',True,(255,255,255))
        alta_puntuacion_rectangulo = alta_puntuacion_superficie.get_rect(center = (288,850))
        pantalla.blit(alta_puntuacion_superficie,alta_puntuacion_rectangulo)

def actualizar_puntuacion(puntuacion, alta_puntuacion):
    if puntuacion > alta_puntuacion:
        alta_puntuacion = puntuacion
    return alta_puntuacion

def comprobar_puntuacion_tuberia():
    global puntuacion, puntuacion_recipiente

    if tuberia_lista:
        for tuberia in tuberia_lista:
            if 95 < tuberia.centerx < 105 and puntuacion_recipiente:
                puntuacion = puntuacion + 1
                sonido_puntuacion.play()
                puntuacion_recipiente = False
            if tuberia.centerx < 0:
                puntuacion_recipiente = True

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 512, devicename= None)
pygame.init()
pantalla = pygame.display.set_mode((576,1024))
pygame.display.set_caption('FlappyBird by Alberto Moreno',)
reloj = pygame.time.Clock()
fuente_juego = pygame.font.Font('04B_19__.ttf',60)

#icono ventana
icono = pygame.image.load('favicon.ico').convert()
pygame.display.set_icon(icono)

#Variables del juego
gravedad = 0.25
pajaro_movimiento = 0
juego_activo = True
puntuacion = 0
alta_puntuacion = 0
puntuacion_recipiente = True

fondo_superficie = pygame.image.load('sprites/background-day.png').convert()
fondo_superficie = pygame.transform.scale2x(fondo_superficie) #Escalamos la imagen a la pantalla

suelo_superficie = pygame.image.load('sprites/base.png').convert()
suelo_superficie = pygame.transform.scale2x(suelo_superficie)
suelo_pos_x = 0
suelo_pos_y = 900

pajaro_volarAbajo = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
pajaro_volarMedio = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
pajaro_volarArriba = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
pajaro_frames = [pajaro_volarAbajo, pajaro_volarMedio, pajaro_volarArriba]
indice_pajaro = 0
pajaro_superficie = pajaro_frames[indice_pajaro]
pajaro_rectangulo = pajaro_superficie.get_rect(center =(100,512))

PAJAROALETEO = pygame.USEREVENT + 1
pygame.time.set_timer(PAJAROALETEO,200)

#pajaro_superficie = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
#pajaro_superficie = pygame.transform.scale2x(pajaro_superficie)
#pajaro_rectangulo = pajaro_superficie.get_rect(center =(100,512))

tuberia_superficie = pygame.image.load('sprites/pipe-green.png')
tuberia_superficie = pygame.transform.scale2x(tuberia_superficie)
tuberia_lista = []
SPAWNTUBERIA = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUBERIA, 1300)
tuberia_altura = [400,500,600,700,800]

fin_juego_superficie = pygame.transform.scale2x(pygame.image.load('sprites/gameover.png').convert_alpha())
fin_juego_rectangulo = fin_juego_superficie.get_rect(center = (288,512))

nuevo_juego_superficie = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())
nuevo_juego_rectangulo = nuevo_juego_superficie.get_rect(center = (288,512))

#Importamos los sonidos del juego
sonido_ala = pygame.mixer.Sound('audio/wing.wav')
sonido_muerte = pygame.mixer.Sound('audio/hit.wav')
sonido_alto = pygame.mixer.Sound('audio/die.wav')
sonido_puntuacion = pygame.mixer.Sound('audio/point.wav')
sonido_puntuacion_contador = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and juego_activo:
                pajaro_movimiento = 0
                pajaro_movimiento -= 10
                sonido_ala.play()
            if event.key == pygame.K_SPACE and  juego_activo == False:
                juego_activo = True
                tuberia_lista.clear()
                pajaro_rectangulo.center = (100,512)
                pajaro_movimiento = 0
                puntuacion = 0
                sonido_alto.play()

        if event.type == SPAWNTUBERIA:
            tuberia_lista.extend(crear_tuberia())

        if event.type == PAJAROALETEO:
            if indice_pajaro < 2:
                indice_pajaro += 1
            else:
                indice_pajaro = 0  
    
            pajaro_superficie, pajaro_rectangulo = animacion_pajaro()

    pantalla.blit(fondo_superficie,(0,0))

    if juego_activo:
        # Pajaro
        pajaro_movimiento += gravedad
        pajaro_rotado = rotar_pajaro(pajaro_superficie)
        pajaro_rectangulo.centery += pajaro_movimiento
        pantalla.blit(pajaro_rotado,pajaro_rectangulo)
        juego_activo = comprobar_colision(tuberia_lista)

        # Tuberias
        tuberia_lista = movimiento_tuberias(tuberia_lista) 
        dibujar_tuberias(tuberia_lista)
                
        comprobar_puntuacion_tuberia()
        mostrar_puntuacion('Juego_Principal')
    else:
        pantalla.blit(nuevo_juego_superficie,nuevo_juego_rectangulo)
        alta_puntuacion = actualizar_puntuacion(puntuacion,alta_puntuacion)
        mostrar_puntuacion('Fin_Juego')
          

    # Suelo
    suelo_pos_x = suelo_pos_x - 1
    dibujar_suelo()
    if suelo_pos_x <= -576:
        suelo_pos_x = 0
    

    pygame.display.update()
    reloj.tick(100) # Limitamos el juego a 100 FPS