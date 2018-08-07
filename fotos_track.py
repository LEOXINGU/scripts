"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-06-14
        copyright            : (C) 2017 by Leandro Franca - Cartographic Engineer
        email                : geoleandro.franca@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation.                              *
 *                                                                         *
 ***************************************************************************/
"""
# Fotos Nao Geo para Geo

##3. Fotos com Track=name
##LF03) GPS, Fotos e Midias=group
##Pasta_com_fotos=folder
##Arquivo_GPX=file
##Shapefile_de_Fotos=output vector

import PIL.Image, PIL.ExifTags
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import os
import datetime
import xml.dom.minidom
from PyQt4.QtCore import *
import re
import numpy as np

pasta = Pasta_com_fotos
sourceGPXPath = Arquivo_GPX
saida = Shapefile_de_Fotos

os.chdir(str(pasta))
lista = os.listdir(pasta)
tam = len(lista)

# Funcao para gerar o padrao data-hora
def data_hora(texto):
    data_hora = texto.replace(' ',':')
    data_hora = data_hora.split(':')
    ano = int(data_hora[0])
    mes = int(data_hora[1])
    dia = int(data_hora[2])
    hora = int(data_hora[3])
    minuto = int(data_hora[4])
    segundo = int(data_hora[5])
    data_hora = datetime.datetime(ano, mes, dia, hora, minuto, segundo)
    return data_hora

# Verificando imangens
progress.setInfo('Verificando imagens...<br/>')
imagens = []
for arquivo in lista:
    if (arquivo[-3:]).lower() == 'jpg':
        img = PIL.Image.open(arquivo)
        if img._getexif():
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
        else:
            exif = {}
        date_time = None
        if 'DateTimeOriginal' in exif:
            date_time = data_hora(exif['DateTimeOriginal'])
            imagens += [[arquivo, date_time]]
        elif 'DateTime' in exif:
            date_time = data_hora(exif['DateTime'])
            imagens += [[arquivo, date_time]]


class TrackPoint( object ):
    def __init__(self, lat, lon, elev, time):
        self.lat = float(lat)
        self.lon = float(lon)
        self.time = time
        self.elev = float(elev)

# CRIAR SHAPEFILE
# Criar campos
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('nome', QVariant.String))
fields.append(QgsField('date_time', QVariant.String))
fields.append(QgsField('direcao', QVariant.Int))
# Criando o shapefile
encoding = 'utf-8'
formato = 'ESRI Shapefile'
crs_epsg =4326
crs = QgsCoordinateReferenceSystem()
crs.createFromSrid(crs_epsg)
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBPoint, crs, formato)

# LER ARQUIVO GPX
progress.setInfo('Lendo arquivo GPX...<br/>')
LISTA_TRACK = []
doc = xml.dom.minidom.parse( sourceGPXPath )
track_n=0
# reading GPX file
for trk_node in doc.getElementsByTagName( 'trk'):
    track_n = track_n+1
    
    # v1.0 
    trkname = 'noname'
    trknameNodeList = trk_node.getElementsByTagName( 'name' )
    if trknameNodeList.length != 0:
        trkname = trk_node.getElementsByTagName( 'name' )[0].firstChild.data
    
    trksegments = trk_node.getElementsByTagName( 'trkseg' )
    
    points = []
    
    # for each segment in GPX ...
    for trksegment in trksegments:
        trk_pts = trksegment.getElementsByTagName( 'trkpt' )
        
        # ... read each track point
        for tkr_pt in trk_pts:
        
            # get latitude and longitude
            ptLat =tkr_pt.getAttribute("lat")
            ptLon = tkr_pt.getAttribute("lon")
            ptEle = None
            ptTime = None
            
            # get elevation
            if len(tkr_pt.getElementsByTagName("ele")) != 0:
                if len(tkr_pt.getElementsByTagName("ele")[0].childNodes) != 0:
                    ptEle = tkr_pt.getElementsByTagName("ele")[0].childNodes[0].data
                    
            # get date and time
            if len(tkr_pt.getElementsByTagName("time")) != 0:
                if len(tkr_pt.getElementsByTagName("time")[0].childNodes) != 0:
                    ptTime = tkr_pt.getElementsByTagName("time")[0].childNodes[0].data
                    ptTime = re.sub(r"(\d{2}):(\d{2}):(\d{2})Z",r"\1:\2:\3.000Z",ptTime)
                    ptTime = datetime.datetime.strptime(ptTime, "%Y-%m-%dT%H:%M:%S.%fZ") -datetime.timedelta(hours=3)
            
            # add point to array
            points.append(TrackPoint(ptLat, ptLon, ptEle, ptTime))
            
        # Adicionando pontos a lista
        if ptTime:
            for ponto in points:
                pnt = QgsGeometry.fromPoint(QgsPoint(ponto.lon, ponto.lat))
                date_time = ponto.time
                LISTA_TRACK +=[[pnt, date_time]]

# Verificar pontos pela proximidade temporal
progress.setInfo('Relacionando data - hora...<br/>')
tam = len(LISTA_TRACK)
feat = QgsFeature()
cont = 0
for img in imagens:
    nome = img[0]
    DT_img = img[1]
    sentinela = False
    for ind in range(tam-2):
        DT1 = LISTA_TRACK[ind][1]
        DT2 = LISTA_TRACK[ind+1][1]
        difer1 = (DT_img - DT1).total_seconds()
        difer2 = (DT_img - DT2).total_seconds()
        if (difer1>=0 and difer2<0):
            sentinela = True
            if difer1 == 0:
                cont +=1
                geom = LISTA_TRACK[ind][0]
                feat.setGeometry(geom)
                att = [cont, pasta + '/' + nome, str(DT_img), None]
                feat.setAttributes(att)
                writer.addFeature(feat)
            else:
                cont +=1
                # Fazer interpolacao entre os dois pontos
                P1 = np.array([LISTA_TRACK[ind][0].asPoint()[0], LISTA_TRACK[ind][0].asPoint()[1]])
                P2 = np.array([LISTA_TRACK[ind+1][0].asPoint()[0], LISTA_TRACK[ind+1][0].asPoint()[1]])
                detaT = (DT2-DT1).total_seconds()
                Px = P1 + (difer1/detaT)*(P2-P1)
                geom = QgsGeometry.fromPoint(QgsPoint(Px[0], Px[1]))
                feat.setGeometry(geom)
                att = [cont, pasta + '/' + nome, str(DT_img), None]
                feat.setAttributes(att)
                ok = writer.addFeature(feat)
    if not sentinela:
        progress.setInfo('O arquivo %s nao esta dentro do track!<br/>' %nome)

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
time.sleep(3)
