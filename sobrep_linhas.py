"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-05-31
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
# Verificar sobreposicao de todas as linhas da lista de camadas
##12. Sobrepos de Linhas=name
##LF02) Revisao=group
##Camada_de_sobreposicao=output vector

saida = Camada_de_sobreposicao

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
fet =QgsFeature()
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0 and layer.geometryType() == QGis.Line:
        for feature in layer.getFeatures():
            geom = feature.geometry()
            coord = geom.asPolyline()
            if coord == []:
                coord = geom.asMultiPolyline()[0]
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
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBLineString, CRS, formato)

# Verificando sobreposicoes
fet =QgsFeature()
cont = 0
tam = len(lista)
for i in range(tam-1):
    for j in range(i+1, tam):
        A = QgsGeometry.fromPolyline(lista[i][0])
        B = QgsGeometry.fromPolyline(lista[j][0])
        if A.intersects(B):
            C = A.intersection(B)
            D = C.asMultiPolyline()
            if D:
                E = QgsGeometry.fromPolyline(D[0])
                for k in range(1, len(D)):
                    E = E.combine(QgsGeometry.fromPolyline(D[k]))
                cont +=1
                att = [cont, lista[i][1], lista[j][1]]
                fet.setGeometry(E)
                fet.setAttributes(att)
                writer.addFeature(fet)
            elif C.asPolyline():
                E = QgsGeometry.fromPolyline(C.asPolyline())
                cont +=1
                att = [cont, lista[i][1], lista[j][1]]
                fet.setGeometry(E)
                fet.setAttributes(att)
                writer.addFeature(fet)
    progress.setPercentage(int((i/float(tam-1))*100))

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)