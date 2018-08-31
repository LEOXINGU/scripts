"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-05-02
        copyright            : (C) 2018 by Leandro Franca - Cartographic Engineer
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
# Alimentar Camada com outra Camada
##Alimentar camada=name
##LF08) EDGV=group
##Camada_de_Origem=vector
##Camada_de_Destino=vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing


# Pegar SRC da camada de destino
origem = processing.getObject(Camada_de_Origem)
SRC_origem = origem.crs()

destino = processing.getObject(Camada_de_Destino)
SRC_destino = destino.crs()
DP = destino.dataProvider()

# Transformacao entre diferentes SRC
xform = QgsCoordinateTransform(SRC_origem, SRC_destino)
def reprojetar(geom):
    if geom.type() == 0: #Ponto
        if geom.isMultipart():
            pnts = geom.asMultiPoint()
            newPnts = []
            for pnt in pnts:
                newPnts += [xform.transform(pnt)]
            newGeom = QgsGeometry.fromMultiPoint(newPnts)
            return newGeom
        else:
            pnt = geom.asPoint()
            newPnt = xform.transform(pnt)
            newGeom = QgsGeometry.fromPoint(newPnt)
            return newGeom
    elif geom.type() == 1: #Linha
        if geom.isMultipart():
            linhas = geom.asMultiPolyline()
            newLines = []
            for linha in linhas:
                newLine =[]
                for pnt in linha:
                    newLine += [xform.transform(pnt)]
                newLines += [newLine]
            newGeom = QgsGeometry.fromMultiPolyline(newLines)
            return newGeom
        else:
            linha = geom.asPolyline()
            newLine =[]
            for pnt in linha:
                newLine += [xform.transform(pnt)]
            newGeom = QgsGeometry.fromPolyline(newLine)
            return newGeom
    elif geom.type() == 2: #Poligono
        if geom.isMultipart():
            poligonos = geom.asMultiPolygon()
            newPolygons = []
            for pol in poligonos:
                newPol = []
                for anel in pol:
                    newAnel = []
                    for pnt in anel:
                        newAnel += [xform.transform(pnt)]
                    newPol += [newAnel]
                newPolygons += [newPol]
            newGeom = QgsGeometry.fromMultiPolygon(newPolygons)
            return newGeom
        else:
            pol = geom.asPolygon()
            newPol = []
            for anel in pol:
                newAnel = []
                for pnt in anel:
                    newAnel += [xform.transform(pnt)]
                newPol += [newAnel]
            newGeom = QgsGeometry.fromPolygon(newPol)
            return newGeom
    else:
        return None

# Mapeamento dos atributos
campos_origem = [field.name() for field in origem.pendingFields()]
campos_destino = [field.name() for field in destino.pendingFields()]
mapa_campo = []
for campo in campos_destino:
    if campo in campos_origem and campo!= 'id':
        mapa_campo += [campos_origem.index(campo)]
    else:
        mapa_campo += [None]

# Validar dados de entrada (deve ter mesma tipo de geometria e estrutura de atributos)
if origem.geometryType() != destino.geometryType():
    progress.setInfo('<br/><br/><b>As camadas devem ser do mesmo tipo de geometria.</b>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "As camadas devem ser do mesmo tipo de geometria!", level=QgsMessageBar.CRITICAL, duration=5)
else:
    # Colar feicoes da camada de origem para a camada de destino reprojetando as coordenadas, se necessario
    feature = QgsFeature()
    if SRC_origem == SRC_destino:
            for feat in origem.getFeatures():
                att = feat.attributes()
                new_att = []
                for k, item in enumerate(mapa_campo):
                    if item != None:
                        new_att += [att[item]]
                    else:
                        new_att += [DP.defaultValue(k)]
                geom = feat.geometry()
                feature.setAttributes(new_att)
                feature.setGeometry(geom)
                DP.addFeatures([feature])
    else:
        for feat in origem.getFeatures():
            att = feat.attributes()
            new_att = []
            for k, item in enumerate(mapa_campo):
                if item != None:
                    new_att += [att[item]]
                else:
                    new_att += [DP.defaultValue(k)]
            geom = feat.geometry()
            newGeom = reprojetar(geom)
            feature.setAttributes(new_att)
            feature.setGeometry(newGeom)
            DP.addFeatures([feature])

    progress.setInfo('<br/><br/><b>Operacao concluida com sucesso!</b>')
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)