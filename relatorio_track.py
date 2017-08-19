# -*- coding: utf-8 -*-
"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-05
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
# Relatorio GPX
##5. Relatorio GPX=name
##LF3) GPS, Fotos e Midias=group
##Arquivo_GPX=file
##Shapefile_da_moldura_WGS84_ou_SIRGAS2000=vector
##MI_da_moldura=string
##Reambulador=string
##Relatorio_FINAL_formato_csv=output file
##Track_points_formato_shp=output vector

sourceGPXPath = Arquivo_GPX
track_points = Track_points_formato_shp
frame = Shapefile_da_moldura_WGS84_ou_SIRGAS2000
CSV = Relatorio_FINAL_formato_csv + u'.csv'
MI = (MI_da_moldura).upper()

import xml.dom.minidom
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import os
from datetime import *
import re
import time

class TrackPoint( object ):
    def __init__(self, lat, lon, elev, time):
        self.lat = float( lat )
        self.lon = float( lon )
        self.time = time
        self.elev = float( elev )
        
def seg2hms(segundos):
    segundo = int(segundos%60)
    minutos = int(segundos/60)
    minuto = minutos%60
    hora = minutos/60
    hms = "%02d:%02d:%02d" %(hora, minuto, segundo)
    return hms
    
def file_path(caminho):
    quebrado = (caminho.replace('/','\\')).split('\\')
    tam = len(quebrado)-2
    filename = quebrado[-1]
    caminho = ''
    for i in range(tam):
        caminho+=quebrado[i]+'\\'
    caminho += quebrado[-2]
    return (caminho, filename)
    
# ABRIR MOLDURA
moldura = QgsVectorLayer(frame, None, "ogr")
moldura.setSubsetString('"MI" = '+'\'' + MI + '\'')
features = moldura.getFeatures()
feature = features.next()
moldura = feature.geometry()

# CRIAR SHAPEFILE
# Criar campos
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('track', QVariant.Int))
fields.append(QgsField('date_time', QVariant.String))
fields.append(QgsField('elev', QVariant.Double, "numeric", 14, 3))
fields.append(QgsField('vel', QVariant.Double, "numeric", 14, 1))
fields.append(QgsField('moldura', QVariant.Int))
# Criando o shapefile
encoding = 'utf-8'
formato = 'ESRI Shapefile'
crs_epsg =4326
crs = QgsCoordinateReferenceSystem()
crs.createFromSrid(crs_epsg)
writer = QgsVectorFileWriter(track_points, encoding, fields, QGis.WKBPoint, crs, formato)

# Criando arquivo CSV para relatorio
arquivo = open(CSV, "w")
arquivo.write("RELATORIO DE TRACKS GPX\n")
arquivo.write("MI: %s\n" %MI)
arquivo.write("Reambulador:; %s\n" %Reambulador)
arquivo.write("Data-Hora:; %s\n" %(datetime.now()).strftime("%d/%m/%Y - %H:%M:%S"))
arquivo.write("Arquivo:;%s\n\n" %file_path(sourceGPXPath)[1])


# LER ARQUIVO GPX
doc = xml.dom.minidom.parse( sourceGPXPath )

track_n=0
cont = 1
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
                    ptTime = datetime.strptime(ptTime, "%Y-%m-%dT%H:%M:%S.%fZ") - timedelta(hours=3) # correcao do fuso horario
            
            # add point to array
            points.append(TrackPoint(ptLat, ptLon, ptEle, ptTime))
            
        # CALCULAR VELOCIDADE
        if ptTime:
            # Data/hora inicial:
            inicial = points[0].time
            final = points[-1].time
            # Comprimento do track e velocidade media
            QgsPointList = []
            for ponto in points:
                QgsPointList += [QgsPoint(ponto.lon, ponto.lat)]
            geom = QgsGeometry.fromPolyline(QgsPointList)
            dist_total = geom.length()*111000
            tempo_total = (final - inicial).total_seconds()
            vel_media = dist_total/tempo_total
            # Velocidade em cada ponto
            velocidades = []
            p1p2 = [QgsPoint(points[0].lon, points[0].lat), QgsPoint(points[1].lon, points[1].lat)]
            tempo = (points[1].time-points[0].time).total_seconds()
            v_p1 = (QgsGeometry.fromPolyline(p1p2)).length()*111000/tempo*3.6
            velocidades += [v_p1]
            for i in range(1, len(points)-1):
                p1 = QgsPoint(points[i-1].lon, points[i-1].lat)
                p2 = QgsPoint(points[i].lon, points[i].lat)
                p3 = QgsPoint(points[i+1].lon, points[i+1].lat)
                tempo = (points[i+1].time-points[i-1].time).total_seconds()
                vel = (QgsGeometry.fromPolyline([p1, p2, p3])).length()*111000/tempo*3.6
                velocidades += [vel]
                
            p1p2 = [QgsPoint(points[-2].lon, points[-2].lat), QgsPoint(points[-1].lon, points[-1].lat)]
            tempo = (points[-1].time-points[-2].time).total_seconds()
            v_ult = (QgsGeometry.fromPolyline(p1p2)).length()*111000/tempo*3.6
            velocidades += [v_ult]
            # Determinando a velocidade maxima
            vel_max = -1e7
            for vel in velocidades:
                if vel > vel_max:
                    vel_max = vel
        else:
            # Comprimento do track
            QgsPointList = []
            for ponto in points:
                QgsPointList += [QgsPoint(ponto.lon, ponto.lat)]
            geom = QgsGeometry.fromPolyline(QgsPointList)
            dist_total = geom.length()*111000
            
        # Determinando os pontos dentro ou fora da moldura
        DentroFora = []
        for ponto in points:
            pnt = QgsGeometry.fromPoint(QgsPoint(ponto.lon, ponto.lat))
            if pnt.within(moldura):
                DentroFora +=[1]
            else:
                DentroFora +=[0]
                
        # Adicionando pontos ao shapefile
        fet = QgsFeature()
        for ind, ponto in enumerate(points):
            pnt = QgsGeometry.fromPoint(QgsPoint(ponto.lon, ponto.lat))
            fet.setGeometry(pnt)
            date_time = str(ponto.time)
            elev = ponto.elev
            dentroFora = DentroFora[ind]
            if ptTime:
                vel = velocidades[ind]
                fet.setAttributes([cont, track_n, date_time, elev, vel, dentroFora])
                cont +=1
            else:
                fet.setAttributes([cont, track_n, None, elev, None, dentroFora])
                cont +=1
            ok= writer.addFeature(fet)
            
        # INSERIR INFORMACOES NO ARQUIVO CSV
        # Track
        arquivo.write("Track: %02d\n" %int(track_n))
        if ptTime:
            # Data/hora inicial
            arquivo.write("Data/hora INICIAL:;%s\n" %inicial.strftime("%d/%m/%Y - %H:%M:%S"))
            # Data/hora final
            arquivo.write("Data/hora FINAL:;%s\n" %final.strftime("%d/%m/%Y - %H:%M:%S"))
            # Distancia percorrida (Km)
            arquivo.write("Distancia percorrida (Km):;%.1f\n" %(dist_total/1e3))
            # Velocidade Media (Km/h)
            arquivo.write("Velocidade Media (Km/h):;%.1f\n" %vel_media)
            # Velociade Maxima (Km/h)
            arquivo.write("Velociade Maxima (Km/h):;%.1f\n" %vel_max)
            
            # Tempo parado e tempo em movimento
            tp = 0
            tm = 0
            for i in range(1, len(velocidades)):
                if velocidades[i] < 1:
                    tp += (points[i].time - points[i-1].time).total_seconds()
                else:
                    tm +=(points[i].time - points[i-1].time).total_seconds()
            # Tempo em movimento (H, M, S)
            arquivo.write("Tempo em movimento (H, M, S):;%s\n" %seg2hms(tm))
            # Tempo parado (horas, minutos, segundos)
            arquivo.write("Tempo parado (H, M, S):;%s\n" %seg2hms(tp))
            
            # Tempo e distancia dentro da carta
            tdc = 0
            ddc =0
            for i in range(1, len(DentroFora)):
                if DentroFora[i] == 1:
                    tdc += (points[i].time - points[i-1].time).total_seconds()
                    p1 = QgsPoint(points[i-1].lon, points[i-1].lat)
                    p2 = QgsPoint(points[i].lon, points[i].lat)
                    geom = QgsGeometry.fromPolyline([p1, p2])
                    ddc += geom.length()*111
            # Tempo dentro da Carta
            arquivo.write("Tempo na Carta:;%s\n" %seg2hms(tdc))
            # Distancia percorrida dentro da Carta
            arquivo.write("Distancia (Km) na Carta:;%.1f\n\n" %ddc)
        else:
            # Data/hora inicial
            arquivo.write("Data/hora INICIAL:;Nao coletado pelo receptor GPS\n")
            # Data/hora final
            arquivo.write("Data/hora FINAL:;Nao coletado pelo receptor GPS\n")
            # Distancia percorrida (Km)
            arquivo.write("Distancia percorrida (Km):;%.1f\n" %(dist_total/1e3))
            # Velocidade Media (Km/h)
            arquivo.write("Velocidade Media:;Nao coletado pelo receptor GPS\n")
            # Velociade Maxima (Km/h)
            arquivo.write("Velocidade Media:;Nao coletado pelo receptor GPS\n")
                 
            # Distancia dentro da carta
            ddc =0
            for i in range(1, len(DentroFora)):
                if DentroFora[i] == 1:
                    p1 = QgsPoint(points[i-1].lon, points[i-1].lat)
                    p2 = QgsPoint(points[i].lon, points[i].lat)
                    geom = QgsGeometry.fromPolyline([p1, p2])
                    ddc += geom.length()*111
            # Distancia percorrida dentro da Carta
            arquivo.write("Distancia (Km) na Carta:;%.1f\n\n" %ddc)
        

del writer
arquivo.close()


progress.setInfo('<b>Relatorio gerado com sucesso!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Relatorio gerado com Sucesso!", level=QgsMessageBar.INFO, duration=10) 
time.sleep(4)

# Executar arquivo CSV
ok = os.system(CSV)