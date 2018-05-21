"""

/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-02-22
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
# Alimentar BD com outro BD
##Alimentar banco=name
##LF08) EDGV=group
##Banco_de_Dados_de_Origem=string
##Banco_de_Dados_de_Destino=string

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

# Transformacao entre diferentes SRC
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

# Colar feicoes das camadas de origem para as camadas de destino reprojetando as coordenadas, se necessario
feature = QgsFeature()
for origem in QgsMapLayerRegistry.instance().mapLayers().values():
    try:
        BD1 = (origem.source()).split("'")[1]
        if BD1 == Banco_de_Dados_de_Origem:
            nome_origem = origem.name()
            campos_origem = [field.name() for field in origem.pendingFields()]
            for destino in QgsMapLayerRegistry.instance().mapLayers().values():
                try:
                    BD2 = (destino.source()).split("'")[1]
                    nome_destino = destino.name()
                    if BD2 == Banco_de_Dados_de_Destino and nome_origem == nome_destino:
                        DP = destino.dataProvider()
                        campos_destino = [field.name() for field in destino.pendingFields()]
                        mapa_campo = []
                        for campo in campos_destino:
                            if campo in campos_origem and campo!= 'id':
                                mapa_campo += [campos_origem.index(campo)]
                            else:
                                mapa_campo += [None]
                        progress.setInfo('<br/>Copiando dados da camada %s...' %nome_origem)
                        SRC_origem = origem.crs()
                        SRC_destino = destino.crs()
                        if SRC_origem == SRC_destino:
                                for feat in origem.getFeatures():
                                    att = feat.attributes()
                                    new_att = []
                                    for item in mapa_campo:
                                        if item != None:
                                            new_att += [att[item]]
                                        else:
                                            new_att += [None]
                                    geom = feat.geometry()
                                    feature.setAttributes(new_att)
                                    feature.setGeometry(geom)
                                    DP.addFeatures([feature])
                        else:
                            xform = QgsCoordinateTransform(SRC_origem, SRC_destino)
                            for feat in origem.getFeatures():
                                att = feat.attributes()
                                new_att = []
                                for item in mapa_campo:
                                    if item != None:
                                        new_att += [att[item]]
                                    else:
                                        new_att += [None]
                                geom = feat.geometry()
                                newGeom = reprojetar(geom)
                                feature.setAttributes(new_att)
                                feature.setGeometry(newGeom)
                                DP.addFeatures([feature])
                except:
                    pass
    except:
        pass

progress.setInfo('<br/><br/><b>Operacao concluida com sucesso!</b>')
progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)