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
# Verificar sobreposicao de todos os Pontos da lista de camadas
##10. Sobrepos de Pontos=name
##LF2) Revisao=group
##Tolerancia=number 0.5
##Camada_de_sobreposicao=output vector

saida = Camada_de_sobreposicao
tol = Tolerancia

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Varrer camadas e pegar as geometrias
# Carregar cada feicao na camada temporaria
lista = []
cont = 1
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0 and layer.geometryType() == QGis.Point and layer.name()!=u'rel_ponto_cotado_altimetrico_p':
        for feature in layer.getFeatures():
            geom = feature.geometry()
            if geom:
                coord = geom.asPoint()
                if coord == []:
                    COORD = geom.asMultiPoint()
                    for coord in COORD:
                        if coord != []:
                            lista += [(coord, layer.name())]
                            cont +=1
                else:
                    if coord != []:
                        lista += [(coord, layer.name())]
                        cont +=1

# Criando camada de sobreposicao
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('camada1', QVariant.String))
fields.append(QgsField('camada2', QVariant.String))
CRS = layer.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBPoint, CRS, formato)

# Distancia unitaria
def DistUnit(p1, p2):
    return abs(p1.x() - p2.x())+abs(p1.y() - p2.y())

# Verificando sobreposicoes
fet =QgsFeature()
cont = 0
tam = len(lista)
for i in range(tam-1):
    for j in range(i+1, tam):
        pA = lista[i][0]
        pB = lista[j][0]
        if DistUnit(pA, pB)<=tol:
            P = QgsGeometry.fromPoint(pA)
            cont +=1
            att = [cont, lista[i][1], lista[j][1]]
            fet.setGeometry(P)
            fet.setAttributes(att)
            writer.addFeature(fet)
    progress.setPercentage(int((i/float(tam-1))*100))
del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)