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
import random

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
                'artistIndex': None,
                'tracksIndex': None,
                'energyIndex': None,
                'danceability': None,
                'tempo': None,
                'genreIndex': None
                }

    analyzer['events'] = lt.newList('SINGLE_LINKED', compareEvents)
    analyzer['artistIndex'] = om.newMap(omaptype='RBT', comparefunction=compareArtist)

    analyzer['tracksIndex'] = mp.newMap(numelements=30631, maptype='PROBING',
                                        comparefunction=compareStrings)
    analyzer['energy'] = om.newMap(omaptype='RBT',
                                        comparefunction=compareCharacteristic)
    analyzer['danceability'] = om.newMap(omaptype='RBT',
                                        comparefunction=compareCharacteristic)
    analyzer['tempo'] = om.newMap(omaptype='RBT',
                                        comparefunction=compareCharacteristic)
    analyzer['genreIndex'] = mp.newMap(numelements=29, maptype='PROBING',
                                        comparefunction=compareStrings)
   
    genres = [{'name':'reggae', 'min':60, 'max':90},
                {'name':'down-tempo', 'min':70, 'max':100},
                {'name':'chill-out', 'min':90, 'max':120},
                {'name':'hip-hop', 'min':85, 'max':115},
                {'name':'jazz and funk', 'min':120, 'max':125},
                {'name':'pop', 'min':100, 'max':130},
                {'name':'r&b', 'min':60, 'max':80},
                {'name':'rock', 'min':110, 'max':140},
                {'name':'metal', 'min':100, 'max':160}]

    for genre in genres:
        updateGenreIndex(analyzer['genreIndex'], genre)

    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
   
    lt.addLast(analyzer['events'], event)
    updateArtistIndex(analyzer['artistIndex'], event)
    updateTrackIndex(analyzer['tracksIndex'], event)
    updateCharacteristicIndex(analyzer['danceability'], 'danceability', event)
    updateCharacteristicIndex(analyzer['energy'], 'energy', event)
    updateCharacteristicIndex(analyzer['tempo'], 'tempo', event)
    
    return analyzer

def updateArtistIndex(map, event):
   
    artistId = event['artist_id']
    
    entry = om.get(map, artistId)
    if entry is None:
        datentry = newDataEntry()
        om.put(map, artistId, datentry)
    else:
        datentry = me.getValue(entry)
    addCharacteristicIndex(datentry, event)
    return map

def updateTrackIndex(map, event):
       
    trackId = event["track_id"]
    
    entry = mp.get(map, trackId)
    if entry is None:
        mp.put(map, trackId, trackId)
    return map

def updateCharacteristicIndex(map, characteristic, event):
       
    value = event[characteristic]
   
    entry = om.get(map, value)
    if entry is None:
        datentry = newDataEntry2()
        om.put(map, value, datentry)
    else:
        datentry = me.getValue(entry)
    addCharacteristicIndex2(datentry, event)
    return map

def updateGenreIndex(map, genre):
   
    genreName = genre['name']
    
    entry = mp.get(map, genreName)
    if entry is None:
        mp.put(map, genreName, genre)
    
    return map

def newDataEntry():

    entry = { 'lstevents': None, 'instrumentalness': None, 'liveness': None, 'speechiness': None,
                'danceability': None, 'valence': None, 'loudness': None, 'tempo': None, 'acousticness': None,
                 'energy': None }
    
    entry['lstevents'] = lt.newList('SINGLE_LINKED', compareEvents)

    entry['instrumentalness'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['liveness'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['speechiness'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['danceability'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['valence'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['loudness'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['tempo'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['acousticness'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)
    entry['energy'] = om.newMap(omaptype='RBT',
                                       comparefunction=compareCharacteristic)

    return entry

def newDataEntry2():

    entry = { 'lstevents': None, 'trackIndex': None}
    
    entry['lstevents'] = lt.newList('SINGLE_LINKED', compareEvents)
    entry['trackIndex'] = mp.newMap(numelements=307, maptype='PROBING', comparefunction=compareTracks)

    return entry

def addCharacteristicIndex (datentry, event):
   
    characteristics = ['instrumentalness', 'liveness', 'speechiness',
                'danceability', 'valence', 'loudness', 'tempo', 'acousticness',
                 'energy']

    for characteristic in characteristics:

        lst = datentry['lstevents']
        lt.addLast(lst, event)

        charIndex = datentry[characteristic ]

        charEntry = om.get(charIndex, event[characteristic ])
        if (charEntry is None):
            entry = newCharEntry(event)
            lt.addLast(entry['lstevents'], event)
            om.put(charIndex, event[characteristic ], entry)
        else:
            entry = me.getValue(charEntry)
            lt.addLast(entry['lstevents'], event)

    return datentry

def addCharacteristicIndex2 (datentry, event):
    
    lst = datentry['lstevents']
    lt.addLast(lst, event)
    
    trackIndex = datentry['trackIndex']
    trackEntry = mp.get(trackIndex, event['track_id'])
    if (trackEntry is None):
        mp.put(trackIndex, event['track_id'], event)
    return datentry

def newCharEntry (event):
    
    charentry = {'lstevents': None}
    
    charentry['lstevents'] = lt.newList('SINGLELINKED', compareEvents)
    return charentry

def addTrackIndex (datentry, event):
    
    lst = datentry['lstevents']
    lt.addLast(lst, event)
    
    return datentry

def newGenre(analyzer, genreName, tempoMin, tempoMax):
    genreIndex = analyzer['genreIndex']
    if not mp.contains(genreIndex, genreName):
        genre = {'name': genreName, 'min': tempoMin, 'max': tempoMax}
        updateGenreIndex(genreIndex, genre)
        return True
    return False


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
    return mp.size(analyzer["tracksIndex"])

def indexHeight1(analyzer):
 
    return om.height(analyzer['artistIndex'])

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

def getFirstLastEvents(analyzer):
    result = lt.newList('SINGLE_LINKED', None,"id")

    i = 1
    j = lt.size(analyzer["events"])

    while i <= lt.size(analyzer["events"]):
        if i <= 5:
            lt.addLast(result, lt.getElement(analyzer["events"],i))

        if (i > j-5):
            lt.addLast(result, lt.getElement(analyzer["events"],i))
    
        i += 1

    return result

def characterizeReproductions(analyzer, characteristic, minval, maxval):

    totevents = 0
    artists = 0
    for key in lt.iterator(om.keySet(analyzer['artistIndex'])):
        charMap = me.getValue(om.get(analyzer['artistIndex'],key))
        lst = om.values(charMap[characteristic], minval, maxval)
        eventsArtist = 0
        for lstevent in lt.iterator(lst):
            eventsArtist += lt.size(lstevent['lstevents'])
        totevents += eventsArtist
        if eventsArtist != 0:
            artists += 1
        
    return [totevents,artists]

def getPartyMusic (analyzer, energyMin, energyMax, danceMin, danceMax):
    
    tracks = lt.newList('SINGLE_LINKED', compareTracks)

    lstEnergy = om.values(analyzer["energy"], energyMin, energyMax)
    lstDance = om.values(analyzer["danceability"], danceMin, danceMax)
    lstResult = lt.newList('SINGLE_LINKED', compareTracks)

    for energyValue in lt.iterator(lstEnergy):
        trackIndex1 = energyValue["trackIndex"]

        for track in lt.iterator(mp.keySet(trackIndex1)):

            for danceValue in lt.iterator(lstDance):
                trackIndex2 = danceValue["trackIndex"]

                if mp.contains(trackIndex2, track):
                    lt.addLast(lstResult, me.getValue(mp.get(trackIndex1, track)))
                    break

    tottracks = lt.size(lstResult)
    
    for i in range(5):
        pos = random.randint(1,lt.size(lstResult))
        lt.addLast(tracks,lt.getElement(lstResult, pos))
        lt.deleteElement(lstResult, pos)

    return [tottracks, tracks]

def studyGenres(analyzer, genres):
    result = []

    for genreName in genres:
        genreEntry = mp.get(analyzer['genreIndex'], genreName)
        genre = me.getValue(genreEntry)

        lstGenre = om.values(analyzer["tempo"], genre['min'], genre['max'])
        genreCount = 0
        artists = []
        for lstItem in lt.iterator(lstGenre):
            genreCount += lt.size(lstItem['lstevents'])

            # for event in lt.iterator(lstItem['lstevents']):
            #     if len(artists) < 10:
            #         artists.append(event['artist_id'])
            #     else:
            #         break

        for event in lt.iterator(analyzer['events']):
            if float(event['tempo']) >= genre['min'] and float(event['tempo']) <= genre['max'] and event['artist_id'] not in artists:
                artists.append(event['artist_id'])
            if len(artists) >= 10:
                break

        result.append({'genre':genreName, 'count': genreCount, 'min':genre['min'], 'max':genre['max'], 'artists':artists})
    return result

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

def compareCharacteristic (characteristic1,characteristic2):
    if (float(characteristic1) == float(characteristic2)):
            return 0
    elif (float(characteristic1) > float(characteristic2)):
        return 1
    elif (float(characteristic1) < float(characteristic2)):
        return -1

def compareStrings (string1, string):
    string2 = string["key"]
    if (string1 == string2):
        return 0
    elif (string1 > string2):
        return 1
    elif (string1 < string2):
        return -1

def compareTracks (track1, track):
    track2 = track["key"]
    if (track1 == track2):
        return 0
    elif (track1 > track2):
        return 1
    elif (track1 < track2):
        return -1

# Funciones de ordenamiento
