"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-24
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
# Verificacao de sobreposicao em uma camada
##Verifica Sobreposicao=name
##LF4) Vetor=group
##Entrada=vector
##Saida=output vector

entrada = Entrada
saida = Saida

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Poligono de entrada
input = processing.getObject(entrada)

if input.geometryType() == QGis.Polygon:
    # Pegar coordenadas dos poligonos
    lista = []
    for feat in input.getFeatures():
        geom = feat.geometry()
        coord = geom.asPolygon()
        if coord == []:
            coord = geom.asMultiPolygon()[0]
        if coord != []:
            lista += [coord]

    # Cirando camada de sobreposicao
    fields = QgsFields()
    fields.append(QgsField('id', QVariant.Int))
    fields.append(QgsField('Feat1', QVariant.Int))
    fields.append(QgsField('Feat2', QVariant.Int))
    CRS = input.crs()
    encoding = 'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBPolygon, CRS, formato)
    del writer
    sobrep = QgsVectorLayer(saida, 'sobreposicao', 'ogr')
    DataProvider = sobrep.dataProvider()

    # Verificar Sobreposicao
    fet =QgsFeature()
    tam = input.featureCount()
    cont = 0
    for i in range(tam-1):
        for j in range(i+1, tam):
            A = QgsGeometry.fromPolygon(lista[i])
            B = QgsGeometry.fromPolygon(lista[j])
            if A.overlaps(B):
                C = A.intersection(B)
                if C.asPolygon() != []:
                    cont +=1
                    att = [cont, i, j]
                    fet.setGeometry(C)
                    fet.setAttributes(att)
                    DataProvider.addFeatures([fet])
        progress.setPercentage(int(((i+1)/float(tam))*100))
        
elif input.geometryType() == QGis.Line:
    # Colocar todas as geometrias em uma lista
    lista = []
    for linha in input.getFeatures():
        geom = linha.geometry()
        coord = geom.asPolyline()
        if coord == []:
            coord = geom.asMultiPolyline()[0]
        lista += [coord]
    tam = len(lista)

    # Cirando camada de sobreposicao
    fields = QgsFields()
    fields.append(QgsField('id', QVariant.Int))
    fields.append(QgsField('Feat1', QVariant.Int))
    fields.append(QgsField('Feat2', QVariant.Int))
    CRS = input.crs()
    encoding = 'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBLineString, CRS, formato)
    del writer
    sobrep = processing.getObject(saida)
    DataProvider = sobrep.dataProvider()

    # Verificando sobreposicoes
    fet =QgsFeature()
    cont = 0
    for index, i in enumerate(range(tam-1)):
        for j in range(i+1, tam):
            A = QgsGeometry.fromPolyline(lista[i])
            B = QgsGeometry.fromPolyline(lista[j])
            if A.intersects(B):
                C = A.intersection(B)
                D = C.asMultiPolyline()
                if D:
                    E = QgsGeometry.fromPolyline(D[0])
                    for k in range(1, len(D)):
                        E = E.combine(QgsGeometry.fromPolyline(D[k]))
                    cont +=1
                    att = [cont, i, j]
                    fet.setGeometry(E)
                    fet.setAttributes(att)
                    DataProvider.addFeatures([fet])
                elif C.asPolyline():
                    E = QgsGeometry.fromPolyline(C.asPolyline())
                    cont +=1
                    att = [cont, i, j]
                    fet.setGeometry(E)
                    fet.setAttributes(att)
                    DataProvider.addFeatures([fet])
                elif C.asMultiPoint():
                    E = QgsGeometry.fromPolyline(C.asMultiPoint())
                    cont +=1
                    att = [cont, i, j]
                    fet.setGeometry(E)
                    fet.setAttributes(att)
                    DataProvider.addFeatures([fet])
        progress.setPercentage(int((index/float(tam-1))*100))


progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>3 CGEO</b><br/>')
progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
time.sleep(3)