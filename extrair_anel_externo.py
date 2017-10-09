"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-22
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
# Extrair anel externo de poligonos
##Extrair anel exterior=name
##LF4) Vetor=group
##Camada_de_poligonos=vector
##Saida=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

poligono = Camada_de_poligonos
saida = Saida

# Camada de Poligono
poligonos = processing.getObject(poligono)

# Camada para o anel externo do poligono
fields = poligonos.pendingFields()
CRS = poligonos.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBLineString, CRS, formato)
del writer
anel = QgsVectorLayer(saida, 'poligonos', 'ogr')
DataProvider = anel.dataProvider()

# Extrair aneis externos
feat = QgsFeature(fields)
for feature in poligonos.getFeatures():
    geom = feature.geometry()
    att = feature.attributes()
    coord = geom.asPolygon()
    if coord == []:
        coord = geom.asMultiPolygon()
        for item in coord:
            new_geom = QgsGeometry.fromPolyline(item[0])
            feat.setGeometry(new_geom)
            feat.setAttributes(att)
            DataProvider.addFeatures([feat])
    else:
        new_geom = QgsGeometry.fromPolyline(coord[0])
        feat.setGeometry(new_geom)
        feat.setAttributes(att)
        DataProvider.addFeatures([feat])

del anel, DataProvider

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Franca- Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 