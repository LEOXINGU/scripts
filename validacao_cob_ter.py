"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-07-21
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
# Validacao de cobertura terrestre
##Checar Cobertura Terrestre=name
##LF09) Validacao=group
##Cobertura_Terrestre=vector
##Moldura=vector
##Tolerancia_area_minima=number 10
##Inconsistencias=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Criar camada de Inconsistencias
moldura = processing.getObject(Moldura)
fields = QgsFields()
fields.append(QgsField('problema', QVariant.String))
CRS = moldura.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(Inconsistencias, encoding, fields, QGis.WKBPolygon, CRS, formato)

if CRS.geographicFlag():
    tol = Tolerancia_area_minima/(110000.0*110000.0)
else:
    tol = Tolerancia_area_minima

# LACUNAS

DIFER = processing.runalg('saga:symmetricaldifference', Cobertura_Terrestre, Moldura, True, None)
diferenca = processing.getObject(DIFER['RESULT'])
tam = diferenca.featureCount()
if tam>0:
    # Quebrando as partes
    feat = QgsFeature()
    for pol in diferenca.getFeatures():
        geom = pol.geometry()
        if geom.area() > tol:
            feat.setGeometry(geom)
            feat.setAttributes(['lacuna'])
            writer.addFeature(feat)

# SOBREPOSICAO

# Varrer camadas e pegar as geometrias que compoe a cobertura terrestre
layer = processing.getObject(Cobertura_Terrestre)
lista = []
for feature in layer.getFeatures():
    geom = feature.geometry()
    if geom:
        coord = geom.asPolygon()
        if coord == []:
            COORD = geom.asMultiPolygon()
            for coord in COORD:
                if coord != []:
                    lista += [(coord, layer.name())]
        else:
            if coord != []:
                lista += [(coord, layer.name())]

# Verificar Sobreposicao
fet =QgsFeature()
tam = len(lista)
cont = 0
for i in range(tam-1):
    for j in range(i+1, tam):
        A = QgsGeometry.fromPolygon(lista[i][0])
        B = QgsGeometry.fromPolygon(lista[j][0])
        if A.intersects(B) or A.equals(B):
            C = A.intersection(B)
            if C.asPolygon() != []:
                if C.area() > tol:
                    fet.setGeometry(C)
                    fet.setAttributes(['sobreposicao'])
                    writer.addFeature(fet)
            elif C.asMultiPolygon() != []:
                for pol in C.asMultiPolygon():
                    geom = QgsGeometry.fromPolygon(pol)
                    if geom.area()>tol:
                        fet.setGeometry(geom)
                        fet.setAttributes(['sobreposicao'])
                        writer.addFeature(fet)
    progress.setPercentage(int(((i+1)/float(tam))*100))

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)