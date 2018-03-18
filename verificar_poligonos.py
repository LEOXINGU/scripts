# -*- coding: utf-8 -*-
"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-09
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
# Verificar Poligonos invalidos (nos duplicados, filetes, e ziguezague)
##Verifica Poligonos=name
##LF04) Vetor=group
##Classe_EDGV_PostGIS=vector
##Pontos_com_problemas=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

poligonos =  QgsVectorLayer(Classe_EDGV_PostGIS, "poligono", "postgres")
DataProvider = poligonos.dataProvider()
tam = poligonos.featureCount()

# Criar shapefile
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('problema', QVariant.String))
path_name = Pontos_com_problemas
encoding = 'utf-8'
formato = 'ESRI Shapefile'
canvas = iface.mapCanvas()
crs_epsg =int((canvas.mapRenderer().destinationCrs().authid()).split(':')[1])
crs = QgsCoordinateReferenceSystem()
crs.createFromSrid(crs_epsg)
writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBPoint, crs, formato)

# Verificacao para cada feicao
for index, feature in enumerate(poligonos.getFeatures()):
    id = feature.id()
    geom = feature.geometry()
    if geom == None:
        continue
    pol = geom.asPolygon()
    if pol == []:
        pol = geom.asMultiPolygon()[0]
    new_pol =[]
    for pointList in pol:
        
        # Identificacao de Nos Duplicados
        ind = 0
        while ind < len(pointList)-1:
            p1 = pointList[ind]
            p2 = pointList[ind+1]
            if p1 == p2:
                # Criar ponto com a classe, id e problema
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(p2))
                feature.setAttributes([ id, u'No duplicado'])
                writer.addFeature(feature)
            ind+=1

        # Identificacao de Filetes
        ind = 0
        while ind < len(pointList)-2:
            p1 = pointList[ind]
            p2 = pointList[ind+1]
            p3 = pointList[ind+2]
            if p1==p3:
                # Criar ponto com a classe, id e problema
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(p2))
                feature.setAttributes([ id, u'Filete'])
                writer.addFeature(feature)
            ind+=1
            
        # Identificacao de Ziguezague
        newPointList = []
        for point in pointList[:-1]:
            if not (point in newPointList):
                newPointList +=[point]
            else:
                # Criar ponto com a classe, id e problema
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(point))
                feature.setAttributes([ id, u'Ziguezague'])
                writer.addFeature(feature)
                
    progress.setPercentage(int((index/float(tam))*100))
    
progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>3 CGEO</b><br/>')
progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)
