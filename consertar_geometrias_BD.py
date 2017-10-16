"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-16
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
# Consertar Geometrias na propria camada
##6. Conserta Geometrias no BD=name
##LF4) Vetor=group
##Camada_de_entrada=vector
##Comprimento_minimo=number 0.001
##Area_minima=number 0.001
##Tolerancia_entre_pontos=number 0
##Angulo_minimo=number 15.0

tol_compr = Comprimento_minimo
tol_area = Area_minima
tol_dist = Tolerancia_entre_pontos

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time
from math import radians, cos, sqrt

COS_ALFA = cos(radians(180-Angulo_minimo))
layer = processing.getObject(Camada_de_entrada)
DataProvider = layer.dataProvider()
tam = layer.featureCount()
deletar = []

if layer.crs().geographicFlag():
    tol_area /= (111000)*(111000)
    tol_dist /= 111000
    tol_compr/= 111000

# Distancia unitaria
def DistUnit(p1, p2):
    return abs(p1.x() - p2.x())+abs(p1.y() - p2.y())

# Cosseno de Alfa
def CosAlfa(v1, v2):
    return (v1[0]*v2[0]+v1[1]*v2[1])/(sqrt(v1[0]*v1[0]+v1[1]*v1[1])*sqrt(v2[0]*v2[0]+v2[1]*v2[1]))

# VERIFICACAO
if layer.geometryType() == QGis.Line:
    # LINHAS
    # Verificacao para cada feicao
    for index, feature in enumerate(layer.getFeatures()):
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
            
            # Remocao de Pontas
            while True:
                mudou = False
                ind = 0
                while ind < len(pointList)-2:
                    p1 = pointList[ind]
                    p2 = pointList[ind+1]
                    p3 = pointList[ind+2]
                    v1 = [p2.x()-p1.x(), p2.y()-p1.y()]
                    v2 = [p3.x()-p2.x(), p3.y()-p2.y()]
                    if CosAlfa(v1, v2) <=COS_ALFA:
                        mudou = True
                        del pointList[ind+1]
                    else:
                        ind+=1
                if not mudou:
                    break

            # Adicionando nova geometria a feicao
            new_geom = QgsGeometry.fromPolyline(pointList)
            newGeomMap = {feature.id() : new_geom}
            ok = DataProvider.changeGeometryValues(newGeomMap)
            
        progress.setPercentage(int((index/float(tam))*100))

    # Apagar feicoes com comprimento menor que a tolerancia
    DataProvider.deleteFeatures(deletar)

elif layer.geometryType() == QGis.Polygon:
    # POLIGONOS
    # Verificacao para cada feicao
    for index, feature in enumerate(layer.getFeatures()):
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
                            n+=1
                            if (ind+1+n) <= (len(pointList)-1):
                                pB = pointList[ind+1+n]
                            else:
                                break
                        if n>0:
                            for k in range(1, n+1):
                                del pointList[ind+1]
                        ind+=1
                        
                    # Remocao de Filetes
                    ind = 0
                    while ind < len(pointList)-2:
                        pA = pointList[ind]
                        pB = pointList[ind+1]
                        pC = pointList[ind+2]
                        n = 0
                        while DistUnit(pA, pC)<=tol_dist:
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
                        else:
                            ind+=1
                    
                    # Remocao de Pontas
                    while True:
                        mudou = False
                        ind = 0
                        while ind < len(pointList)-2:
                            p1 = pointList[ind]
                            p2 = pointList[ind+1]
                            p3 = pointList[ind+2]
                            v1 = [p2.x()-p1.x(), p2.y()-p1.y()]
                            v2 = [p3.x()-p2.x(), p3.y()-p2.y()]
                            if CosAlfa(v1, v2) <=COS_ALFA:
                                mudou = True
                                del pointList[ind+1]
                            else:
                                ind+=1
                        if not mudou:
                            break
                            
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