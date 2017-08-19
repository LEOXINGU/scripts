"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-18
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
# Conserta Linhas invalidas (nos duplicados, filetes, e ziguezagues)
##Conserta Linhas=name
##LF4) Vetor=group
##Camada_de_entrada=vector
##Tolerancia_para_comprimento_minimo=number 0.001
##Tolerancia_para_distantica_minima=number 0
##Shapefile_de_saida=output vector

saida = Shapefile_de_saida
tol_compr = Tolerancia_para_comprimento_minimo
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
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBLineString, CRS, formato)
del writer
linhas = QgsVectorLayer(saida, 'linhas', 'ogr')
DataProvider = linhas.dataProvider()

# Copiar todas as feicoes do input para classe poligonos
for feature in input.getFeatures():
    ok = DataProvider.addFeatures([feature])

del input, fields

tam = linhas.featureCount()
deletar = []

if linhas.crs().geographicFlag():
    tol_area /= (111000)*(111000)
    tol_dist /= 111000

# Distancia unitaria
def DistUnit(p1, p2):
    return abs(p1.x() - p2.x())+abs(p1.y() - p2.y())

# Verificacao para cada feicao
for index, feature in enumerate(linhas.getFeatures()):
    geom = feature.geometry()
    # Deixar quieto geometrias NoType
    if geom == None:
        continue
    # Remocao de poligonos com area menor que a tolerancia
    if geom.length() <= tol_compr:
        deletar += [feature.id()]
        continue
    else:
        pointList = geom.asPolyline()
        if pointList == []:
            pointList = geom.asMultiPolyline()[0]
        
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
        
        # Adicionando nova geometria a feicao
        new_geom = QgsGeometry.fromPolyline(pointList)
        newGeomMap = {feature.id() : new_geom}
        ok = DataProvider.changeGeometryValues(newGeomMap)
        
    progress.setPercentage(int((index/float(tam))*100))
            
# Apagar feicoes com comprimento menor que a tolerancia
DataProvider.deleteFeatures(deletar)

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)