"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-05-05
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
##1. Track Points=name
##LF3) GPS, Fotos e Midias=group
##arquivo_GPX=file
##Shapefile_de_saida=output vector

import xml.dom.minidom
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import os
from datetime import *
import re
import time

track_points = Shapefile_de_saida
sourceGPXPath = arquivo_GPX

class TrackPoint( object ):
    def __init__(self, lat, lon, elev, time):
        self.lat = float( lat )
        self.lon = float( lon )
        self.time = time
        self.elev = float( elev )

# CRIAR SHAPEFILE
# Criar campos
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('track', QVariant.Int))
fields.append(QgsField('date_time', QVariant.String))
fields.append(QgsField('elev', QVariant.Double, "numeric", 14, 3))
fields.append(QgsField('vel', QVariant.Double, "numeric", 14, 1))
# Criando o shapefile
encoding = 'utf-8'
formato = 'ESRI Shapefile'
crs_epsg =4326
crs = QgsCoordinateReferenceSystem()
crs.createFromSrid(crs_epsg)
writer = QgsVectorFileWriter(track_points, encoding, fields, QGis.WKBPoint, crs, formato)

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
                    ptTime = datetime.strptime(ptTime, "%Y-%m-%dT%H:%M:%S.%fZ") -timedelta(hours=3)
            
            # add point to array
            points.append(TrackPoint(ptLat, ptLon, ptEle, ptTime))
            
        # CALCULAR VELOCIDADE
        if ptTime:
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
        # Adicionando pontos ao shapefile
        fet = QgsFeature()
        for ind, ponto in enumerate(points):
            pnt = QgsGeometry.fromPoint(QgsPoint(ponto.lon, ponto.lat))
            fet.setGeometry(pnt)
            date_time = str(ponto.time)
            elev = ponto.elev
            if ptTime:
                vel = velocidades[ind]
                fet.setAttributes([cont, track_n, date_time, elev, vel])
                cont +=1
            else:
                fet.setAttributes([cont, track_n, None, elev, None])
                cont +=1
            ok= writer.addFeature(fet)
        
del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
time.sleep(3)