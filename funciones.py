import sqlite3

def crear_tabla(nombre:str):
    '''
    Esta funcion crea la tabla de puntajes para el ranking.
    Recibe por parametro el nombre del archivo a crear.
    '''
    with sqlite3.connect(nombre) as conexion:
        try:
            sentencia = ''' create table puntajes
            (
            id integer primary key autoincrement,
            nombre text,
            puntaje integer
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla puntajes")
        except sqlite3.OperationalError:
            print("La tabla puntajes ya existe")

def insertar_fila(ingreso,score):
    '''
    Esta funcion se encarga de insertar una nueva fila.
    Recibe por parametro el nombre ingresado y el score final.
    '''
    with sqlite3.connect("puntajes.db") as conexion:
        try:
            conexion.execute("insert into puntajes(nombre,puntaje) values (?,?)",(ingreso,score))
            conexion.commit()
        except:
            print("Error")
def ordenar_filas_desc():
    '''
    Esta funcion se encarga de realizar el ordenamiento de las filas de manera descendente
    '''
    with sqlite3.connect("puntajes.db") as conexion:
        try:
            cursor = conexion.execute("SELECT * FROM puntajes ORDER BY puntaje DESC LIMIT 5")
        except:
                print("Error")
    return cursor
