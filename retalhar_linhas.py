# -*- coding: utf-8 -*-
"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-23
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
# Corta linhas nas intersecoes com os poligonos
##2. Retalhar Linhas=name
##LF4) Vetor=group
##Camada_de_Linhas=vector
##Camada_de_Poligonos=vector
##Saida=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

poligono = Camada_de_Poligonos
linha = Camada_de_Linhas
saida = Saida

# Camada de Poligonos
poligonos = processing.getObject(poligono)
# Camada de Linhas
linhas = processing.getObject(linha)

# Criar camada de Saida (linhas cortadas)
fields = linhas.pendingFields()
CRS = linhas.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBLineString, CRS, formato)
del writer
recortado = QgsVectorLayer(saida, 'poligonos', 'ogr')
DataProvider = recortado.dataProvider()

# Gerar camada do anel exterior dos poligonos
anel = processing.runalg('script:extrairanelexterior', poligonos, None)
recortante = processing.getObject(anel['Saida'])

# Funcao para recortar linhas
def SplitLine(geom, cortador):
    # split the line
    result, new_geoms, test_points = geom.splitGeometry(cortador, True)
    # Put pieces in the new list
    lista = []
    # part 1
    lista += [geom.asPolyline()]
    # part 2
    for new_geom in new_geoms:
         lista += [new_geom.asPolyline()]
    return lista

# Ober lista de linhas
lista_lin = []
for lin in linhas.getFeatures():
    geom = lin.geometry()
    coord = geom.asPolyline()
    if coord == []:
        coord = geom.asMultiPolyline()[0]
    lista_lin += [(coord, lin.attributes())]

# Ober lista de poligonos
lista_pol = []
for pol in recortante.getFeatures():
    geom = pol.geometry()
    coord = geom.asPolyline()
    if coord == []:
        coord = geom.asMultiPolyline()[0]
    lista_pol += [coord]


# Comecar o recorte
feature = QgsFeature(fields)
while len(lista_lin)>0:
    linha = QgsGeometry.fromPolyline(lista_lin[0][0])
    cruzou = False
    for pol in lista_pol:
        poligono = QgsGeometry.fromPolyline(pol)
        if linha.crosses(poligono):
            recortes = SplitLine(linha, pol)
            cruzou = True
            att = lista_lin[0][1]
            del lista_lin[0]
            for recorte in recortes:
                lista_lin = [(recorte, att)] + lista_lin
            break
    if cruzou == False:
        feature.setGeometry(linha)
        feature.setAttributes(lista_lin[0][1])
        DataProvider.addFeatures([feature])
        del lista_lin[0]
        
del DataProvider, recortado


progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)
