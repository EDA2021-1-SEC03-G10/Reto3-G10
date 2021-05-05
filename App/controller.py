"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def loadData(analyzer, eventsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    eventsfile = cf.data_dir + eventsfile
    input_file = csv.DictReader(open(eventsfile, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        model.addEvent(analyzer, event)

    return analyzer

def eventsSize (analyzer):
  
    return model.eventsSize(analyzer)


def artistsSize (analyzer):

    return model.artistsSize(analyzer)

def tracksSize (analyzer):
    
    return model.tracksSize(analyzer)

def indexHeight1(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight1(analyzer)

def minKey1(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey1(analyzer)


def maxKey1(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey1(analyzer)

def getFirstLastEvents (analyzer):

    return model.getFirstLastEvents (analyzer)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def characterizeReproductions(analyzer, characteristic, minval, maxval):

    return model.characterizeReproductions(analyzer, characteristic, minval, maxval) 

def getPartyMusic (analyzer, energyMin, energyMax, danceMin, danceMax):

    return model.getPartyMusic (analyzer, energyMin, energyMax, danceMin, danceMax) 

def newGenre(analyzer, genre, tempoMin, tempoMax):
    return model.newGenre(analyzer, genre.lower().strip(), tempoMin, tempoMax)

def studyGenres(analyzer, txtGenres):
    genres = txtGenres.split(',')
    result = []
    for genre in genres:
        result.append(genre.strip())
    return model.studyGenres(analyzer, result)