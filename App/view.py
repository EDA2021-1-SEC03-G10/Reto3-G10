"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


eventsfile = 'context_content_features-small.csv'

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Caracterizar las reproducciones")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")
    print("7- Indicar el género musical más escuchado en el tiempo")
    

catalog = None
cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando analizador....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont, eventsfile)
        print('Eventos cargados: ' + str(controller.eventsSize(cont)))

        print('Artistas cargados: ' + str(controller.artistsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight1(cont))) 
        print('Menor Llave: ' + str(controller.minKey1(cont)))
        print('Mayor Llave: ' + str(controller.maxKey1(cont)))

        print('Pistas de audio cargados: ' + str(controller.tracksSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight2(cont))) 
        print('Menor Llave: ' + str(controller.minKey2(cont)))
        print('Mayor Llave: ' + str(controller.maxKey2(cont)))

    elif int(inputs[0]) == 2:
        characteristic = input("Ingrese la característica a evaluar: ")
        minval = input("ingrese el mínimo valor: ")
        maxval = input("Ingrese el maximo valor: ")
        answer = controller.firstreq(catalog, characteristic, minval, maxval)
        print(answer)

        pass

    else:
        sys.exit(0)
sys.exit(0)
