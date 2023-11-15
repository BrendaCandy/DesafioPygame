import pygame
from constantes import *

def armar_lista_paso (imagen:str,num:int,left:int,top:int)->list:
    '''
    Crea la lista de pasos del personaje
    Recibe por parametro la imagen del personaje, el numero de imagenes, la pos x y pos y
    Devuelve la lista de pasos 
    '''
    lista_pasos = []
    i = 0
    for i in range(num):
        path = imagen + str(i) + ".png"
        imagen_personaje = pygame.image.load(path)
        imagen_personaje = pygame.transform.scale(imagen_personaje,(45,70))
        rect_imagen = imagen_personaje.get_rect()
        rect_imagen.x = left
        rect_imagen.y = top
        dict_personaje = {}
        dict_personaje["imagen"] = imagen_personaje
        dict_personaje["rect_imagen"] = rect_imagen
        lista_pasos.append(dict_personaje)
    return lista_pasos

def armar_disparo (imagen:str)->dict:
    '''
    Arma el diccionario del disparador
    Recibe por parametro la imagen 
    Devuelve el diccionario completo
    '''
    imagen_disparo = pygame.image.load(imagen)
    imagen_disparo = pygame.transform.scale(imagen_disparo,(25,450))
    imagen_disparo_personaje = pygame.image.load("D:\Desktop\JUEGUILLO 2\imagenes\player-dispara.png")
    imagen_disparo_personaje = pygame.transform.scale(imagen_disparo_personaje,(45,70))
    rect_disparo = imagen_disparo.get_rect()
    dict_disparo = {}
    dict_disparo["imagen"] = imagen_disparo
    dict_disparo["rect_pos"] = rect_disparo
    dict_disparo["rect"] = pygame.Rect(0,0,8,500)
    dict_disparo["imagen_personaje"] = imagen_disparo_personaje
    return dict_disparo

class Personaje:
    def __init__(self, path_L:str,path_D:str,cantidad:int,left:int,top:int,direccion:str,imagen_disparo:str) -> None:
        '''
        Contruye mi personaje
        '''
        self.lista_pasos_d = armar_lista_paso(path_D,cantidad,left,top)
        self.lista_pasos_i = armar_lista_paso(path_L,cantidad,left,top)
        self.disparo = armar_disparo(imagen_disparo)
        self.dirrecion_actual = direccion
        self.pos_actual = left
        self.disparo_activo = False
        self.pos_fotograma = 0
        pygame.mixer.init()
        self.sonido_disparo = pygame.mixer.Sound("D:\Desktop\JUEGUILLO 2\\audio\\audio_disparo.mp3")

    def girar(self, direccion:str,lista_pasos:list):
        '''
        Permite a mi personaje girar
        Por parametro paso la dirrecion a la que deseo girar y la lista de pasos correspondiente
        '''
        for i in range(4):
            lista_pasos[i]["rect_imagen"].x = self.pos_actual
        self.dirrecion_actual = direccion
        if self.pos_fotograma < len(lista_pasos) - 1:
            self.pos_fotograma += 1
        else:
            self.pos_fotograma = 0

    def caminar(self,lista_pasos:list,dirreccion:int):
        '''
        Permite desplazarse a mi personae
        Recibe lista de pasos y dirrecion a tomar
        '''
        if dirreccion == DIRECCION_L:
            if lista_pasos[self.pos_fotograma]["rect_imagen"].x < 32:
                lista_pasos[self.pos_fotograma]["rect_imagen"].x = lista_pasos[self.pos_fotograma]["rect_imagen"].x
            else:
                lista_pasos[self.pos_fotograma]["rect_imagen"].x = lista_pasos[self.pos_fotograma]["rect_imagen"].x - 25
        else:
            if lista_pasos[self.pos_fotograma]["rect_imagen"].x < 720:
                lista_pasos[self.pos_fotograma]["rect_imagen"].x = lista_pasos[self.pos_fotograma]["rect_imagen"].x + 25
            else:
                lista_pasos[self.pos_fotograma]["rect_imagen"].x = lista_pasos[self.pos_fotograma]["rect_imagen"].x

        self.pos_actual = lista_pasos[self.pos_fotograma]["rect_imagen"].x
        if self.pos_fotograma < len(lista_pasos) - 1:
            self.pos_fotograma += 1
        else:
            self.pos_fotograma = 0
   

    def disparar_juego (self):  
        '''
        Permite disparar a mi personaje
        '''
        if not (self.disparo_activo):
            self.disparo["rect_pos"].x = self.pos_actual + 9
            self.disparo["rect_pos"].y = 500
            self.disparo["rect"].x = self.pos_actual + 16
            self.disparo["rect"].y = 500
        else:
            self.disparo["rect_pos"].y -= 25
            self.disparo["rect"].y -= 25
        if self.disparo["rect_pos"].y < 0:
            self.disparo_activo = False

    def update_personaje(self,lista_eventos:list):
        '''
        Actualizo los eventos de mi personaje
        Recibo la lista de eventos
        '''
        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.disparo_activo = True
                    self.sonido_disparo.play()   
        self.disparar_juego()
        lista_teclas = pygame.key.get_pressed()
        if True in lista_teclas:
            if lista_teclas[pygame.K_RIGHT]:
                if self.dirrecion_actual == DIRECCION_L:
                    self.girar(DIRECCION_R,self.lista_pasos_d)
                else:
                    self.caminar(self.lista_pasos_d,DIRECCION_R)
            if lista_teclas[pygame.K_LEFT]:
                if self.dirrecion_actual == DIRECCION_R:
                    self.girar(DIRECCION_L,self.lista_pasos_i)
                else:
                    self.caminar(self.lista_pasos_i,DIRECCION_L)

    def dibujar_personaje(self, pantalla,direccion:str):
        '''
        Actualiza el personaje
        Recibe la pantalla y la direccion
        '''
        if self.disparo_activo:
            # pygame.draw.rect(pantalla,COLOR_VERDE, self.disparo["rect"])
            pantalla.blit(self.disparo["imagen"],self.disparo["rect_pos"])
            pantalla.blit(self.disparo["imagen_personaje"],(self.pos_actual,411))
        else:
            if self.dirrecion_actual == direccion:
                # pygame.draw.rect(pantalla,COLOR_VERDE, self.lista_pasos_d[self.pos_fotograma]["rect_imagen"])
                pantalla.blit(self.lista_pasos_d[self.pos_fotograma]["imagen"],self.lista_pasos_d[self.pos_fotograma]["rect_imagen"])
            else:
                # pygame.draw.rect(pantalla,COLOR_VERDE, self.lista_pasos_i[self.pos_fotograma]["rect_imagen"])
                pantalla.blit(self.lista_pasos_i[self.pos_fotograma]["imagen"],self.lista_pasos_i[self.pos_fotograma]["rect_imagen"])
                


