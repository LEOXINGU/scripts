"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-06-13
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
# Separar feicoes multipartes de todas as camadas
##05. Separar Multipartes=name
##LF2) Revisao=group

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
from processing.tools.vector import VectorWriter
import time

for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0 and layer.geometryType() == QGis.Point:
        DP = layer.dataProvider()
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPoint()
                if len(coord)>1:
                    # Atualizar a geometria da feicao com a geometria com apenas uma parte
                    new_geom = QgsGeometry.fromMultiPoint([coord[0]])
                    newGeomMap = {feat.id() : new_geom}
                    ok = DP.changeGeometryValues(newGeomMap)
                    # Criar novas feicoes com as outras partes
                    att = feat.attributes()
                    new_att = [None] + att[1:]
                    new_feat = QgsFeature()
                    for i in range(1, len(coord)):
                        new_geom = QgsGeometry.fromMultiPoint([coord[i]])
                        new_feat.setGeometry(new_geom)
                        new_feat.setAttributes(new_att)
                        ok = DP.addFeatures([new_feat])
    if layer.type()==0 and layer.geometryType() == QGis.Line:
        DP = layer.dataProvider()
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPolyline()
                if len(coord)>1:
                    # Atualizar a geometria da feicao com a geometria com apenas uma parte
                    new_geom = QgsGeometry.fromMultiPolyline([coord[0]])
                    newGeomMap = {feat.id() : new_geom}
                    ok = DP.changeGeometryValues(newGeomMap)
                    # Criar novas feicoes com as outras partes
                    att = feat.attributes()
                    new_att = [None] + att[1:]
                    new_feat = QgsFeature()
                    for i in range(1, len(coord)):
                        new_geom = QgsGeometry.fromMultiPolyline([coord[i]])
                        new_feat.setGeometry(new_geom)
                        new_feat.setAttributes(new_att)
                        ok = DP.addFeatures([new_feat])
    if layer.type()==0 and layer.geometryType() == QGis.Polygon:
        DP = layer.dataProvider()
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom:
                coord = geom.asMultiPolygon()
                if len(coord)>1:
                    # Atualizar a geometria da feicao com a geometria com apenas uma parte
                    new_geom = QgsGeometry.fromMultiPolygon([coord[0]])
                    newGeomMap = {feat.id() : new_geom}
                    ok = DP.changeGeometryValues(newGeomMap)
                    # Criar novas feicoes com as outras partes
                    att = feat.attributes()
                    new_att = [None] + att[1:]
                    new_feat = QgsFeature()
                    for i in range(1, len(coord)):
                        new_geom = QgsGeometry.fromMultiPolygon([coord[i]])
                        new_feat.setGeometry(new_geom)
                        new_feat.setAttributes(new_att)
                        ok = DP.addFeatures([new_feat])

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)