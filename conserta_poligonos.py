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
# Conserta Poligonos invalidos (nos duplicados, filetes, e ziguezagues)
##Conserta Poligonos=name
##LF4) Vetor=group
##Camada_de_entrada=vector
##Tolerancia_para_area_minima=number 0.001
##Tolerancia_para_distantica_minima=number 0.001
##Shapefile_de_saida=output vector

saida = Shapefile_de_saida
tol_area = Tolerancia_para_area_minima
tol_dist = Tolerancia_para_distantica_minima

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

input = processing.getObject(Camada_de_entrada)
fields = input.pendingFields()
CRS = input.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBPolygon, CRS, formato)
del writer
poligonos = QgsVectorLayer(saida, 'poligonos', 'ogr')
DataProvider = poligonos.dataProvider()

# Copiar todas as feicoes do input para classe poligonos
for feature in input.getFeatures():
    ok = DataProvider.addFeatures([feature])

del input, fields
tam = poligonos.featureCount()
deletar = []

if poligonos.crs().geographicFlag():
    tol_area /= (111000)*(111000)
    tol_dist /= 111000

# Distancia unitaria
def DistUnit(p1, p2):
    return abs(p1.x() - p2.x())+abs(p1.y() - p2.y())

# Verificacao para cada feicao
for index, feature in enumerate(poligonos.getFeatures()):
    geom = feature.geometry()
    # Deixar quieto geometrias NoType
    if geom == None:
        continue
    # Remocao de poligonos com area menor que a tolerancia
    if geom.area() <= tol_area:
        deletar += [feature.id()]
        continue
    else:
        pol = geom.asPolygon()
        if pol == []:
            pol = geom.asMultiPolygon()[0]
        new_pol =[]
        for pointList in pol:
            # Remocao de buracos com area menor que a tolerancia
            simples = QgsGeometry.fromPolygon([pointList])
            if simples.area() <= tol_area:
                continue
            else:
                # Remocao de Nos  N-plicados
                ind = 0
                while ind < len(pointList)-1:
                    pA = pointList[ind]
                    pB = pointList[ind+1]
                    n = 0
                    while DistUnit(pA, pB) <=tol_dist:
                        print 'no duplicado'
                        n+=1
                        if (ind+1+n) <= (len(pointList)-1):
                            pB = pointList[ind+1+n]
                        else:
                            break
                    if n>0:
                        for k in range(1, n+1):
                            del pointList[ind+1]
                        print 'nos deletados'
                    ind+=1
                    
                # Remocao de Filetes
                ind = 0
                while ind < len(pointList)-2:
                    pA = pointList[ind]
                    pB = pointList[ind+1]
                    pC = pointList[ind+2]
                    n = 0
                    while DistUnit(pA, pC)<=tol_dist:
                        print 'filete'
                        n +=1
                        if ((ind+2+n) <= (len(pointList)-1)) and ((ind - n) >= 0):
                            pA = pointList[ind - n]
                            pC = pointList[ind +2 +n]
                        else:
                            break
                    if n>0:
                        for k in range(1, 2*n+1):
                            del pointList[ind+1]
                        ind -= n-1
                        print 'filete deletado'
                    else:
                        ind+=1
                    
                new_pol += [pointList]
            # Adicionando nova geometria a feicao
            new_geom = QgsGeometry.fromPolygon(new_pol)
            newGeomMap = {feature.id() : new_geom}
            ok = DataProvider.changeGeometryValues(newGeomMap)
            
    progress.setPercentage(int((index/float(tam))*100))
            
# Apagar feicoes com area menor que a tolerancia
DataProvider.deleteFeatures(deletar)
    
progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)
