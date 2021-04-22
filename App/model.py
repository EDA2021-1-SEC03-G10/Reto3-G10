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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    

    Retorna el analizador inicializado.
    """
    analyzer = {'events': None,
                'artistIndex': None
                }

    analyzer['events'] = lt.newList('SINGLE_LINKED', compareEvents)
    analyzer['artistIndex'] = om.newMap(omaptype='BST',
                                       comparefunction=compareArtist)
    analyzer['tracksIndex'] = om.newMap(omaptype='BST',
                                       comparefunction=compareArtist)
    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
   
    lt.addLast(analyzer['events'], event)
    updateArtistIndex(analyzer['artistIndex'], event)
    updateTrackIndex(analyzer['tracksIndex'], event)
    return analyzer

def updateArtistIndex(map, event):
   
    artistId = event['artist_id']
    
    entry = om.get(map, artistId)
    if entry is None:
        datentry = newDataEntry(event)
        om.put(map, artistId, datentry)
    else:
        datentry = me.getValue(entry)
    addArtistIndex(datentry, event)
    return map

def updateTrackIndex(map, event):
       
    trackId = event["track_id"]
    
    entry = om.get(map, trackId)
    if entry is None:
        datentry = newDataEntry(event)
        om.put(map, trackId, datentry)
    else:
        datentry = me.getValue(entry)
    addTrackIndex(datentry, event)
    return map

def newDataEntry(event):

    entry = { 'lstevents': None}
    
    entry['lstevents'] = lt.newList('SINGLE_LINKED', compareArtist)
    return entry

def addArtistIndex (datentry, event):

    lst = datentry['lstevents']
    lt.addLast(lst, event)
    
    return datentry

def addTrackIndex (datentry, event):
    
    lst = datentry['lstevents']
    lt.addLast(lst, event)
    
    return datentry

# Funciones para creacion de datos

# Funciones de consulta

def eventsSize(analyzer):
    """
    Número de eventos
    """
    return lt.size(analyzer['events'])

def artistsSize (analyzer):
    return om.size(analyzer["artistIndex"])

def tracksSize (analyzer):
    return om.size(analyzer["tracksIndex"])

def indexHeight1(analyzer):
 
    return om.height(analyzer['artistIndex'])

def indexHeight2(analyzer):
     
    return om.height(analyzer['tracksIndex'])

def minKey1(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['artistIndex'])


def maxKey1(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['artistIndex'])

def minKey2(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['tracksIndex'])


def maxKey2(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['tracksIndex'])  

# Funciones utilizadas para comparar elementos dentro de una lista

def compareEvents (event1,event2):
    if event1 ["id"]== event2["id"]:
        return  0
    elif event1 ["id"] > event2["id"]:
        return  1
    elif event1 ["id"] < event2["id"]:
        return  -1

def compareArtist (artist1,artist2):
    if (artist1 == artist2):
        return 0
    elif (artist1 > artist2):
        return 1
    elif (artist1 < artist2):
        return -1


# Funciones de ordenamiento
