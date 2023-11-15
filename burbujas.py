import pygame
from constantes import *

def crear_obstaculo(imagen:str,x:int,y:int,mov_x:int,mov_y:int,ancho:int,alto:int)->dict:
    '''
    Se encarga de crear un diccionario para un obstaculo.
    Recibe una imagen, pos x, pos y, movimiento en x, movimiento en y, ancho y alto de la imagen.
    Devuelve diccionario.
    '''
    dic_circulo = {}
    dic_circulo["superficie"] = pygame.image.load(imagen)
    dic_circulo["superficie"] = pygame.transform.scale(dic_circulo["superficie"],(ancho,alto))
    dic_circulo["rect"] = dic_circulo["superficie"].get_rect()
    dic_circulo["rect"].x = x
    dic_circulo["rect"].y = y
    dic_circulo["mov_x"] = mov_x
    dic_circulo["mov_y"] = mov_y
    dic_circulo["ancho"] = ancho
    dic_circulo["alto"] = alto
    return dic_circulo

def crear_obstaculos(num:int)->list:
    '''
    Se encarga de crear la lista de los obstaculos
    Recibe por parametro el numero del nivel
    Devuelve la lista
    '''
    burbujas = []
    for i in range(num+4):
        burbuja = crear_obstaculo("D:\Desktop\JUEGUILLO 2\imagenes\BOLA_L_ROJA.png",10+(i*110),50,3+num,-3-num,60-(num*10),60-(num*10))
        burbujas.append(burbuja)
    return burbujas

class Bubujas:
    def __init__(self,num:int) -> None:
        '''
        Contruye mi clase
        '''
        self.lista_burbujas = crear_obstaculos(num)
        pygame.mixer.init()
        self.sonido_burbuja = pygame.mixer.Sound("D:\Desktop\JUEGUILLO 2\\audio\\audio_burbuja_pop.mp3")

    def mover(self):
        '''
        Se encarga de mover las burbujas y determinar sus limites.
        '''
        for bola in self.lista_burbujas:
            alto_piso = 30
            if bola["rect"].y >= ALTO_VENTANA - bola["alto"] - 30:
                bola["mov_y"] = -17
            else: 
                bola["mov_y"] += 0.5

            if bola["rect"].x < 0 or bola["rect"].x > ANCHO_VENTANA - bola["ancho"]:
                bola["mov_x"] *= -1
            bola["rect"].x += bola["mov_x"]
            bola["rect"].y += bola["mov_y"]

    def detectar__disparo(self,personaje,score:int):
        '''
        Detecta la colision del arma con la burbuja.
        Recibe por parametro la clase personaje y el score
        Devuelve el score que va acumulando
        '''
        burbujas_a_eliminar = []
        for bola in self.lista_burbujas:
            if personaje.disparo["rect"].colliderect(bola["rect"]):
                score += 10
                personaje.disparo_activo = False
                self.sonido_burbuja.play()
                burbujas_a_eliminar.append(bola)
        self.eliminar_burbuja(burbujas_a_eliminar)
        return score
    
    def eliminar_burbuja(self,lista:list):
        '''
        Elimina las burbujas que fueron colisionadas con el arma.
        Recibe por parametro la lista a eliminar
        '''
        for bola in lista:
            self.lista_burbujas.remove(bola)

    def actualizar_pantalla(self,pantalla):
        '''
        Actualiza a las burbujas en pantalla
        Recibe la pantalla del juego a blittear
        '''
        for burbuja in self.lista_burbujas: 
            # pygame.draw.rect(pantalla,COLOR_VERDE, burbuja["rect"])
            pantalla.blit(burbuja["superficie"],burbuja["rect"])

        
