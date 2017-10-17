"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-09-21
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
# Verificar Auto-Intersecao
##LF2) Revisao=group
##08. Verificar Auto Intersecoes=name
##Shapefile_de_Loops=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Pegando o SRC da camada trecho de drenagem
layerList = QgsMapLayerRegistry.instance().mapLayersByName('hid_trecho_drenagem_l')
if layerList:
 layer = layerList[0]
 SRC = layer.crs()
# Criar arquivo de pontos para armazenar as informacoes
fields = QgsFields()
fields.append(QgsField('classe', QVariant.String))
fields.append(QgsField('id', QVariant.Int))
writer = QgsVectorFileWriter(Shapefile_de_Loops, 'utf-8', fields, QGis.WKBPoint, SRC, 'ESRI Shapefile')

# Camada para nao verificar
nao_verif = ['rel_curva_nivel_l',
                    'hid_trecho_drenagem_l']

# Varrer camadas
cont = 0
lista_pnts = []
feature = QgsFeature()
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    nome = layer.name()
    # Linhas
    if layer.geometryType() == QGis.Line and not(nome in nao_verif) :
        progress.setInfo('Verificando classe: %s<br/>' %nome)
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPolyline()[0]
            if coord:
                tam = len(coord)
                if tam > 3:
                    for i in range(0,tam-3):
                        segA = [coord[i], coord[i+1]]
                        geomA = QgsGeometry.fromPolyline(segA)
                        for j in range(i+2,tam-1):
                            segB = [coord[j], coord[j+1]]
                            geomB = QgsGeometry.fromPolyline(segB)
                            if geomA.crosses(geomB):
                                point = geomA.intersection(geomB)
                                if not(point in lista_pnts):
                                    lista_pnts += [point]
                                    feature.setAttributes([nome, feat.id()])
                                    feature.setGeometry(point)
                                    writer.addFeature(feature)
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPolyline()[0]
            if coord:
                tam = len(coord)
                if tam > 5:
                    for i in range(0,tam-3):
                        PntA = coord[i]
                        for j in range(i+3,tam):
                            PntB = coord[j]
                            if PntA == PntB:
                                point = QgsGeometry.fromPoint(PntA)
                                if not(point in lista_pnts):
                                    lista_pnts += [point]
                                    feature.setAttributes([nome, feat.id()])
                                    feature.setGeometry(point)
                                    writer.addFeature(feature)
    # Poligonos
    if layer.geometryType() == QGis.Polygon and not(nome in nao_verif) :
        progress.setInfo('Verificando classe: %s<br/>' %nome)
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPolygon()[0][0]
            if coord:
                tam = len(coord)
                if tam > 3:
                    for i in range(0,tam-3):
                        segA = [coord[i], coord[i+1]]
                        geomA = QgsGeometry.fromPolyline(segA)
                        for j in range(i+2,tam-1):
                            segB = [coord[j], coord[j+1]]
                            geomB = QgsGeometry.fromPolyline(segB)
                            if geomA.crosses(geomB):
                                point = geomA.intersection(geomB)
                                if not(point in lista_pnts):
                                    lista_pnts += [point]
                                    feature.setAttributes([nome, feat.id()])
                                    feature.setGeometry(point)
                                    writer.addFeature(feature)
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPolygon()[0][0]
            if coord:
                tam = len(coord)
                if tam > 5:
                    for i in range(0,tam-3):
                        PntA = coord[i]
                        for j in range(i+3,tam-1):
                            PntB = coord[j]
                            if PntA == PntB:
                                point = QgsGeometry.fromPoint(PntA)
                                if not(point in lista_pnts):
                                    lista_pnts += [point]
                                    feature.setAttributes([nome, feat.id()])
                                    feature.setGeometry(point)
                                    writer.addFeature(feature)
                                    
del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)