import pygame
from constantes import *
from funciones import ordenar_filas_desc

def renderizar_textos(fuente:str, tamaño:int,color,contenido:str):
    '''
    Se encarga de renderizar los textos
    Por parametro recibe la fuente el tamaño el color y el contenido a renderizar
    Devuelve el texto renderizado
    '''
    fuente_titulo = pygame.font.Font(fuente, tamaño)
    texto_titulo = fuente_titulo.render(contenido,True,color)
    return texto_titulo
def tranformar_imagen(imagen:str,ancho:int,alto:int):
     '''
     Carga y transforma una imagen
     Recibe por parametro la imagen el ancho y el alto
     Devuelve la imagen transformada
     '''
     imagen = pygame.image.load(imagen)
     imagen = pygame.transform.scale(imagen,(ancho,alto))
     return imagen

class Pantalla:
    def __init__(self,ancho:int,alto:int) -> None:
        '''
        Construye mi pantalla
        '''
        self.pantalla = pygame.display.set_mode((ancho,alto))
        pygame.display.set_caption("Super Bubble")
        self.fondo = tranformar_imagen("D:\Desktop\JUEGUILLO 2\imagenes\\fondo_2.jpg",ancho,alto)
        self.titulo = pygame.image.load("D:\Desktop\JUEGUILLO 2\imagenes\\titulo.png")
        self.fuente = "D:\Desktop\JUEGUILLO 2\\fuente\Retro Gaming.ttf"
        self.mostrar_scores = False
        self.flecha = tranformar_imagen("D:\Desktop\JUEGUILLO 2\imagenes\\flecha.png",50,40)
    def eventos(self, lista_eventos:list):
        '''
        Eventos del score
        '''
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_click = list(evento.pos)
                if (posicion_click[0] > 60 and posicion_click[0] < 283) and (posicion_click[1] > 352 and posicion_click[1] < 410):
                    self.mostrar_scores = True
                if (posicion_click[0] > 62 and posicion_click[0] < 107) and (posicion_click[1] > 434 and posicion_click[1] < 460):
                    if self.mostrar_scores:
                        self.mostrar_scores = False

    def dibujar(self):
        self.pantalla.blit(self.fondo,self.fondo.get_rect())
        if self.mostrar_scores:
            txt_titulos = renderizar_textos(self.fuente,40,COLOR_AZUL,"NUMERO   NOMBRE     PUNTOS")
            self.pantalla.blit(txt_titulos,(50,105))
            cursor = ordenar_filas_desc()
            for i,fila in enumerate(cursor):
                fila = list(fila)
                txt_id = renderizar_textos(self.fuente,30,COLOR_AMARILLO,str(fila[0]))
                self.pantalla.blit(txt_id,(40*3,170+(i*50)))
                txt_nombre = renderizar_textos(self.fuente,30,COLOR_AMARILLO,fila[1])
                self.pantalla.blit(txt_nombre,(40*8,170+(i*50)))
                txt_puntos = renderizar_textos(self.fuente,30,COLOR_AMARILLO,str(fila[2]))
                self.pantalla.blit(txt_puntos,(40*15.5,170+(i*50)))
            txt_top = renderizar_textos(self.fuente,50,COLOR_AZUL,"TOP 5  ")
            self.pantalla.blit(txt_top,(305,30))
            self.pantalla.blit(self.flecha,(60,430))
        else:
            self.pantalla.blit(self.titulo,(85,110))
            texto_jugar = renderizar_textos(self.fuente,50,COLOR_ESMERALDA, "Jugar")
            self.pantalla.blit(texto_jugar,(290,300))
            texto_scores = renderizar_textos(self.fuente,50,COLOR_ESMERALDA, "Scores")
            self.pantalla.blit(texto_scores,(56,350))
            texto_salir = renderizar_textos(self.fuente,50,COLOR_ESMERALDA, "Salir")
            self.pantalla.blit(texto_salir,(530,350))
        pygame.display.flip()

def dibujar_vida(pantalla, x:int, y:int):
    '''
    Dibuja las vidas en mi pantalla
    Por parametro recibe el x y el y y la pantalla
    '''
    vida = tranformar_imagen("D:\Desktop\JUEGUILLO 2\imagenes\corazon.png",60,60)
    pantalla.blit(vida,(x,y))

class PantallaNiveles(Pantalla):
    def __init__(self, ancho, alto) -> None:
        '''
        Constructor de mi pantalla niveles
        '''
        super().__init__(ancho, alto)
        self.fondo_juego = pygame.image.load("D:\Desktop\JUEGUILLO 2\imagenes\\5.jpg")
        self.piso = pygame.image.load("D:\Desktop\JUEGUILLO 2\imagenes\\02.jpg")
        self.time_imagen = tranformar_imagen("D:\Desktop\JUEGUILLO 2\imagenes\\time.png",60,30)
        self.score_imagen = tranformar_imagen("D:\Desktop\JUEGUILLO 2\imagenes\score.png",60,30)
    
    def dibujar(self,nivel:int,num_vidas:int,personaje,burbuja,segundos:int,score:int):
        '''
        Se encarga de mostrarlos en pantalla
        '''
        self.pantalla.fill((0,0,0))

        personaje.dibujar_personaje(self.pantalla,DIRECCION_R)
        self.pantalla.blit(self.piso,(0,478))
        burbuja.actualizar_pantalla(self.pantalla)
        txt_nivel = renderizar_textos(self.fuente,30,COLOR_AMARILLO, f"Nivel {nivel}")
        self.pantalla.blit(txt_nivel,(345,23))
        for i in range(num_vidas):
            dibujar_vida(self.pantalla,(i*60+15),10)
        self.pantalla.blit(self.time_imagen,(650,23))
        self.pantalla.blit(self.score_imagen,(650,63))
        txt_segundos = renderizar_textos(self.fuente,30,COLOR_AMARILLO, str(segundos)+"s")
        self.pantalla.blit(txt_segundos,(720,20))
        txt_score = renderizar_textos(self.fuente,25,COLOR_AMARILLO, str(score))
        self.pantalla.blit(txt_score,(720,62))
        pygame.display.flip()      
    
class PantallaFinal(Pantalla):
    def __init__(self, ancho, alto) -> None:
        super().__init__(ancho, alto)
      
    def dibujar(self,ganando, fin_tiempo,ingreso,guardado):
        '''
        Se encarga de mostrar los elementos en pantalla
        '''
        self.pantalla.fill((0,0,0))
        if ganando:
            txt = renderizar_textos(self.fuente,60,COLOR_VERDE,"GANASTE!")
        elif fin_tiempo == True:
            txt = renderizar_textos(self.fuente,60,COLOR_VERDE,"TIEMPO!!")
        else:
            txt = renderizar_textos(self.fuente,60,COLOR_ROJO,"PERDISTE")
            guardado = False
        self.pantalla.blit(txt,(240,140))
        txt_salir = renderizar_textos(self.fuente,35,COLOR_AMARILLO,"Salir")
        txt_menu = renderizar_textos(self.fuente,35,COLOR_AMARILLO,"Menu")
        self.pantalla.blit(txt_salir,(360,400))
        self.pantalla.blit(txt_menu,(360,350))
        if guardado:
            ingreso_rect = pygame.Rect(270,260,300,44)
            pygame.draw.rect(self.pantalla,COLOR_AMARILLO,ingreso_rect,2)
            txt_nombre = renderizar_textos(self.fuente,30,COLOR_BLANCO, ingreso)
            txt_ingreso = renderizar_textos(self.fuente,20,COLOR_BLANCO, "Ingrese su nombre:")
            self.pantalla.blit(txt_ingreso,(285,220))
            txt_guardar_puntaje = renderizar_textos(self.fuente, 20,COLOR_ESMERALDA, "GUARDAR PUNTAJE")
            self.pantalla.blit(txt_guardar_puntaje,(300,320))
            self.pantalla.blit(txt_nombre, (ingreso_rect.x + 5, ingreso_rect.y + 2))
        pygame.display.flip()
    
