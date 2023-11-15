import pygame
from constantes import *
from personaje import Personaje
from burbujas import *
from pantalla import *
from funciones import *

crear_tabla("puntajes.db")
pygame.init()
pantalla = Pantalla(ANCHO_VENTANA,ALTO_VENTANA)
pantalla_final = PantallaFinal(ANCHO_VENTANA,ALTO_VENTANA)
pantalla_niveles = PantallaNiveles(ANCHO_VENTANA,ALTO_VENTANA)

timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos, 1000)

pygame.mixer.init()
sonido_victoria = pygame.mixer.Sound("D:\Desktop\JUEGUILLO 2\\audio\\audio_victoria.mp3")
sonido_derrota = pygame.mixer.Sound("D:\Desktop\JUEGUILLO 2\\audio\\audio_gameover.mp3")

reloj = pygame.time.Clock()
flag_correr = True
fin_tiempo = False 
while flag_correr:
    guardado = True
    ingreso = ''
    segundos = "40"
    score = 0 
    num_vidas = 3
    nivel = 1
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            posicion_click = list(evento.pos)
            # print(posicion_click)
            if (posicion_click[0] > 534 and posicion_click[0] < 676) and (posicion_click[1] > 362 and posicion_click[1] < 396):
                flag_correr = False
            if (posicion_click[0] > 289 and posicion_click[0] < 488) and (posicion_click[1] > 305 and posicion_click[1] < 365):
                flag_partida = True
                while flag_partida:
                    en_final = False
                    ganando = False
                    personaje = Personaje("D:\Desktop\JUEGUILLO 2\imagenes\player-L-","D:\Desktop\JUEGUILLO 2\imagenes\player-",4,400,411,DIRECCION_L,"D:\Desktop\JUEGUILLO 2\imagenes\lazo.png")
                    burbujas = Bubujas(nivel)
                    flag_inicio = True
                    while flag_inicio:
                        milis = reloj.tick(60)
                        lista_eventos = pygame.event.get()
                        for evento in lista_eventos:
                            if evento.type == pygame.QUIT:
                                flag_correr = False
                                flag_partida = False
                                flag_inicio = False
                            if evento.type == pygame.USEREVENT:
                                if evento.type == timer_segundos:
                                    if fin_tiempo == False:
                                        segundos = int(segundos) - 1
                                        if int(segundos) <= 0:
                                            fin_tiempo = True
                                            en_final = True
                                            sonido_derrota.play()
                        personaje.update_personaje(lista_eventos)
                        burbujas.mover()
                        for bola in burbujas.lista_burbujas:
                            if personaje.dirrecion_actual == DIRECCION_L:
                                if personaje.lista_pasos_i[personaje.pos_fotograma]["rect_imagen"].colliderect(bola["rect"]):
                                    flag_inicio = False
                                    num_vidas -= 1
                                    score = 0
                            else:
                                if personaje.lista_pasos_d[personaje.pos_fotograma]["rect_imagen"].colliderect(bola["rect"]):
                                    flag_inicio = False
                                    num_vidas -= 1
                                    score = 0
                        score = burbujas.detectar__disparo(personaje,score)
                        if len(burbujas.lista_burbujas) <= 0:
                            nivel += 1
                            flag_inicio = False
                        if num_vidas == 0:
                            ganando = False
                            en_final = True
                            sonido_derrota.play()
                        if nivel > 3:
                            ganando = True
                            en_final = True
                            sonido_victoria.play()
                        while en_final:
                            lista_eventos = pygame.event.get()
                            for evento in lista_eventos:
                                if evento.type == pygame.QUIT:
                                    flag_correr = False
                                    flag_partida = False
                                    flag_inicio = False
                                    en_final = False
                                if evento.type == pygame.KEYDOWN:
                                    if evento.key == pygame.K_BACKSPACE:
                                        ingreso = ingreso[0:-1]
                                    else:
                                        ingreso += evento.unicode
                                if evento.type == pygame.MOUSEBUTTONDOWN:
                                    posicion_click = list(evento.pos)
                                    if (posicion_click[0] > 300 and posicion_click[0] < 528) and (posicion_click[1] > 324 and posicion_click[1] < 336):
                                            if guardado:
                                                insertar_fila(ingreso,score)
                                                guardado = False
                                    if (posicion_click[0] > 362 and posicion_click[0] < 465) and (posicion_click[1] > 358 and posicion_click[1] < 383):
                                        en_final = False
                                        flag_inicio = False
                                        flag_partida = False
                                        sonido_derrota.stop()
                                        sonido_victoria.stop()
                                    if (posicion_click[0] > 363 and posicion_click[0] < 460) and (posicion_click[1] > 409 and posicion_click[1] < 430):
                                        en_final = False
                                        flag_inicio = False
                                        flag_partida = False
                                        flag_correr = False
                            pantalla_final.dibujar(ganando,fin_tiempo,ingreso,guardado)
                        pantalla_niveles.dibujar(nivel,num_vidas,personaje,burbujas,segundos,score)    
                    pygame.display.flip()
    pantalla.eventos(lista_eventos)
    pantalla.dibujar() 
pygame.quit() 