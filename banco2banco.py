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
# Consistencia Topologica de CT
##Alimentar banco com banco=name
##LF8) EDGV=group
##Banco_de_Dados_de_Origem=string
##Banco_de_Dados_de_Destino=string
##Usuario_PostGIS=string postgres
##Senha=string cgeo2017


from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

# Criar URI do banco de destino
uri = QgsDataSourceURI()

# Pegar SRC dos bancos de destinos
uri.setConnection("localhost","5432", Banco_de_Dados_de_Origem, Usuario_PostGIS, Senha)
uri.setDataSource("public","aux_moldura_a","geom","")
camada = QgsVectorLayer(uri.uri(), '', "postgres")
SRC_origem = camada.crs()

uri.setConnection("localhost","5432", Banco_de_Dados_de_Destino, Usuario_PostGIS, Senha)
uri.setDataSource("public","aux_moldura_a","geom","")
camada = QgsVectorLayer(uri.uri(), '', "postgres")
SRC_destino = camada.crs()

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
        else:
            pnt = geom.asPoint()
            newPnt = xform.transform(pnt)
            newGeom = QgsGeometry.fromPoint(newPnt)
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
        else:
            linha = geom.asPolyline()
            newLine =[]
            for pnt in linha:
                newLine += [xform.transform(pnt)]
            newGeom = QgsGeometry.fromPolyline(newLine)
    
    elif geom.type() == 2: #Poligono
        if geom.isMultipart():
            poligonos = geom.asMultiPolygon()
            newPolygons = []
            for aneis in poligonos:
                newAneis = []
                for anel in aneis:
                    newAnel = []
                    for pnt in anel:
                        newAnel += [xform.transform(pnt)]
                newAneis += [newAnel]
            newPolygons += [newAneis]
            newGeom = QgsGeometry.fromMultiPolygon(newPolygons)
        else:
            aneis = geom.asPolygon()
            newAneis = []
            for anel in aneis:
                newAnel = []
                for pnt in anel:
                    newAnel += [xform.transform(pnt)]
            newAneis += [newAnel]
            newGeom = QgsGeometry.fromPolygon(newAneis)
    return newGeom


# Colar feicoes do banco de origem para o banco de destino reprojetando as coordenadas, se necessario
if SRC_origem == SRC_destino:
    for layer in QgsMapLayerRegistry.instance().mapLayers().values():
        if layer.type()==0:
            try:
                lyr_source = (layer.source()).split("'")[1]
                if lyr_source == Banco_de_Dados_de_Origem:
                    layer_name = layer.name()
                    uri.setDataSource("public", layer_name, "geom","")
                    camada = QgsVectorLayer(uri.uri(), '', "postgres")
                    DP = camada.dataProvider()
                    newFeat = QgsFeature()
                    for feat in layer.getFeatures():
                        att = feat.attributes()
                        newFeat.setGeometry(feat.geometry())
                        newFeat.setAttributes([None]+att[1:])
                        ok = DP.addFeatures([newFeat])
            except:
                pass
else:
    for layer in QgsMapLayerRegistry.instance().mapLayers().values():
        if layer.type()==0:
            try:
                lyr_source = (layer.source()).split("'")[1]
                if lyr_source == Banco_de_Dados_de_Origem:
                    layer_name = layer.name()
                    uri.setDataSource("public", layer_name, "geom","")
                    camada = QgsVectorLayer(uri.uri(), '', "postgres")
                    DP = camada.dataProvider()
                    newFeat = QgsFeature()
                    for feat in layer.getFeatures():
                        att = feat.attributes()
                        newFeat.setGeometry(feat.geometry())
                        newFeat.setAttributes([None]+att[1:])
                        ok = DP.addFeatures([newFeat])
            except:
                pass
    
progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)