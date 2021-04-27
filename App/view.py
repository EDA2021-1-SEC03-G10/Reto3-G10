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

def printEvents(analyzer):
    events = controller.getFirstLastEvents(analyzer)    
    
    print('Estos son los 5 primeros y 5 últimos eventos de escucha: ')
    for event in lt.iterator(events):
        print('Instrumentalidad: ' + event['instrumentalness'] + 
            ' Viveza: ' + event['liveness'] + ' Habla: ' + event['speechiness'] +
            ' Capacidad de baile: ' + event['danceability'] +
            ' Valencia: ' + event['valence'] + ' Sonoridad: ' + event['loudness'] +
            ' Tempo: ' + event['tempo'] + ' Acústica: ' + event['acousticness'] + 
            ' Energía: ' + event['energy'] + ' Modo: ' + event['mode'] +
            ' Clave: ' + event['key'] + ' Id del artista: ' + event['artist_id'] +
            ' Idioma del tweet: ' + event['tweet_lang'] + ' Fecha de creación del registro: ' + event['created_at'] +
            ' Idioma: ' + event['lang'] + ' Zona Horaria: ' + event['time_zone'] +
            ' Id del usuario: ' + event['user_id'] + ' Id: ' + event['id'])

    print("\n")

def printTracks(lstTracks):
  
    
    print('Estos son 5 tracks aleatorios: ')
    i = 1
    for event in lt.iterator(lstTracks):
        print('Track ' + str(i) + ': ' + event['track_id'] + "con energía = " + event['energy'] +
            ' y capacidad de baile = ' + event['danceability'])
        i += 1

    print("")


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
        print('Altura del árbol: ' + str(controller.indexHeight1(cont))) 
        print('Menor Llave: ' + str(controller.minKey1(cont)))
        print('Mayor Llave: ' + str(controller.maxKey1(cont)))

        print('Pistas de audio cargados: ' + str(controller.tracksSize(cont)))

        printEvents(cont)


    elif int(inputs[0]) == 3:
        characteristic = input("Ingrese la característica a evaluar (en inglés): ")
        minval = float(input("Ingrese el mínimo valor: "))
        maxval = float(input("Ingrese el máximo valor: "))

        answer = controller.characterizeReproductions(cont, characteristic, minval, maxval)


        print ("===============================================================================")
        print ("++++++ Req No. 1 resultados... ++++++")
        print (characteristic + " está entre " + str(minval) + " y " + str(maxval))
        print ("Total de reproducciones: " + str(answer[0]) + "  Total de artistas únicos:  " +  str(answer[1]) )
        print ("===============================================================================")

    elif int(inputs[0]) == 4:
        energyMin = float(input( "Ingrese el Valor mínimo de la característica Energy: "))
        energyMax = float(input( "Ingrese el Valor máximo de la característica Energy: "))
        danceMin = float(input( "Ingrese el Valor mínimo de la característica Danceability: "))
        danceMax = float(input( "Ingrese el Valor máximo de la característica Danceability: "))

        answer = controller.getPartyMusic(cont, energyMin, energyMax, danceMin, danceMax)

        print ("=========================================================================================")
        print ("++++++ Req No. 2 (Estudiante A: Lindsay Pinto Morato) resultados... ++++++")
        print ("")
        print("Energy está entre " + str(energyMin) + " y " + str(energyMax))
        print("Danceability está entre " + str(danceMin) + " y " + str(danceMax))
        print ("")
        print("Total de tracks únicos en eventos: " + str(answer[0]))
        

        printTracks(answer[1])

        print ("=========================================================================================")

    elif int(inputs[0]) == 5:
        pass


    elif int(inputs[0]) == 6:
        print("1- Ingresar un nuevo género musical")
        print("2- Estudiar géneros musicales")
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs[0]) == 1:
            genre = input("Ingrese el nombre único para el nuevo género musical: ")
            tempoMin = int(input( "Valor mínimo del Tempo del nuevo género musical: "))
            tempoMax = int(input( "Valor máximo del Tempo del nuevo género musical: "))

            answer = controller.newGenre(cont, genre, tempoMin, tempoMax)

            if answer:
                print("El género se creó correctamente")
            else:
                print("Ya existe un género con ese nombre")
        elif int(inputs[0]) == 2:
            genres = input("Ingrese los nombres de los géneros, separados por coma: ")

            answer = controller.studyGenres(cont, genres)

            total = 0

            for genre in answer:
                total += genre['count']
            print ("=========================================================")   
            print ("++++++ Req No. 4  resultados... ++++++")
            print ("Total de reproducciones: " + str(total))
            print ("")

            for genre in answer:
                
                print ("")
                print("======== " + genre['genre'].upper() + " ========")
                print("Para " + genre['genre'] + " el tempo está entre " + str(genre['min']) + " y " + str(genre['max']) + "BPM")
                print("Reproducciones de " + genre['genre'] + ": " + str(genre['count']))
                print("----- Algunos artistas de " + genre['genre'] + " -----")

                i = 1
                for artist in genre['artists']:
                    print("Artista " + str(i) + ": " + artist)
                    i += 1
                print("")

            print ("=========================================================")   
    else:
        sys.exit(0)
sys.exit(0)
