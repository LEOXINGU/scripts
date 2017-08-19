"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-06-15
        copyright            : (C) 2017 by Leandro Franca - Cartographic Engineer @ Brazilian Army
        email                : franca.leandro@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation.                              *
 *                                                                         *
 ***************************************************************************/
"""
# Gerreferenciar Midia pelo Track

##4. Midias com Track=name
##LF3) GPS, Fotos e Midias=group
##Pasta_com_Video_ou_Audio=folder
##Padrao_da_DataHora=string YYYY_MM_DD_hh_mm_ss
##Arquivo_GPX=file
##Shapefile_de_Midia=output vector


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

pasta = Pasta_com_Video_ou_Audio
sourceGPXPath = Arquivo_GPX
saida = Shapefile_de_Midia
formatos = ['mp3', 'mp4', 'avi', 'wmv', 'wma', 'wav']
os.chdir(str(pasta))
lista = os.listdir(pasta)
tam = len(lista)

# Padrao: Y - ano, M - mes, D - dia, h - hora, m - minutos, s - segundos
modelo = 'YYYY_MM_DD_hh_mm_ss'
ind_Y = modelo.index('Y')
ind_M = modelo.index('M')
ind_D = modelo.index('D')
ind_h = modelo.index('h')
ind_m = modelo.index('m')
ind_s = modelo.index('s')

# Funcao para gerar o padrao data-hora
def data_hora(texto):
    ano = int(texto[ind_Y:ind_Y+4])
    mes = int(texto[ind_M:ind_M+2])
    dia = int(texto[ind_D:ind_D+2])
    hora = int(texto[ind_h:ind_h+2])
    minuto = int(texto[ind_m:ind_m+2])
    segundo = int(texto[ind_s:ind_s+2])
    data_hora = datetime.datetime(ano, mes, dia, hora, minuto, segundo)
    return data_hora

# Verificando imangens
progress.setInfo('Verificando midias...<br/>')
midias = []
for arquivo in lista:
    if (arquivo[-3:]).lower() in formatos:
        date_time = data_hora(arquivo)
        midias += [[arquivo, date_time]]


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
for midia in midias:
    nome = midia[0]
    DT_img = midia[1]
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
                att = [cont, nome, str(DT_img)]
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
                att = [cont, nome, str(DT_img)]
                feat.setAttributes(att)
                ok = writer.addFeature(feat)
    if not sentinela:
        progress.setInfo('O arquivo %s nao esta dentro do track!<br/>' %nome)

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
time.sleep(3)