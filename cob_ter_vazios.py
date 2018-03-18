"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-05-24
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
# Verificacao de cobertura terrestre (VAZIOS)
##09. Cob Ter Vazios=name
##LF02) Revisao=group
##Moldura=vector
##Tolerancia_area_minima=number 10
##Todas_os_poligonos_de_Cob_Ter=output vector
##Camada_de_Vazios=output vector

path_name = Todas_os_poligonos_de_Cob_Ter
tol = Tolerancia_area_minima

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

CT = processing.runalg('script:cobter', Moldura, Todas_os_poligonos_de_Cob_Ter)
DIFER = processing.runalg('saga:symmetricaldifference', CT['Todas_os_poligonos_de_Cob_Ter'], Moldura, False, None)
diferenca = processing.getObject(DIFER['RESULT'])
tam = diferenca.featureCount()
features = diferenca.getFeatures( QgsFeatureRequest(tam-1))
feature = features.next()
poligonos = feature.geometry().asMultiPolygon()

# Moldura
moldura = processing.getObject(Moldura)

# Criar camada de Vazios
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
CRS = moldura.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(Camada_de_Vazios, encoding, fields, QGis.WKBPolygon, CRS, formato)

# Quebrando as partes
cont = 0
feat = QgsFeature()
for pol in poligonos:
    geom = QgsGeometry.fromPolygon(pol)
    if geom.area() > tol:
        cont +=1
        feat.setGeometry(geom)
        feat.setAttributes([cont])
        writer.addFeature(feat)

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)