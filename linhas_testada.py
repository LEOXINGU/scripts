"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2019-08-16
        copyright            : (C) 2019 by Leandro Franca - Cartographic Engineer
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

# Gerar Linhas de Testada
##Linhas de Testada=name
##LF04) Vetor=group
##Camada_de_lotes=vector
##Linhas_de_Testada=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

# Abrir camada de linhas
pol = processing.getObject(Camada_de_lotes)
SRC = pol.crs()

# Validacao dos dados de entrada
if not(pol.geometryType() == QGis.Polygon):
    progress.setInfo('<b><font  color="#ff0000">Camada vetorial de entrada deve ser do tipo poligono!</b><br/>')
    iface.messageBar().pushMessage(u'Situacao', "Camada vetorial de entrada deve ser do tipo poligono!", level=QgsMessageBar.WARNING, duration=8)
else:
    
    # Criar camada de Linhas
    fields = pol.pendingFields()
    writer = QgsVectorFileWriter(Linhas_de_Testada, 'utf-8', fields, QGis.WKBLineString, SRC, 'ESRI Shapefile')

    # Colocar poligonos em lista
    feature = QgsFeature()
    tam = pol.featureCount()
    atributos, linhas = [],[]
    for feat in pol.getFeatures():
        geom = feat.geometry()
        atributos += [feat.attributes()]
        if geom:
            linhas += [geom.asPolygon()[0]]
            if not (geom.asPolygon()):
                linhas += [geom.asMultiPolygon()[0][0]]

    # Calculando a diferenca para cada linha
    for i in range(tam):
        geom1 = QgsGeometry.fromPolyline(linhas[i])
        for j in range(tam):
            if i != j:
                geom2 = QgsGeometry.fromPolyline(linhas[j])
                if geom1.intersects(geom2):
                    differ = geom1.difference(geom2)
                    geom1 = differ
        if geom1.length() > 0:
            feature.setAttributes(atributos[i])
            feature.setGeometry(geom1)
            writer.addFeature(feature)
        progress.setPercentage(int((i+1)/float(tam)*100))

    del writer
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
