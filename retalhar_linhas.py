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
##LF04) Vetor=group
##Camada_de_Linhas=vector
##Camada_Recortante_Tipo_Linha_ou_Poligono=vector
##Saida=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

poligono = Camada_Recortante_Tipo_Linha_ou_Poligono
linha = Camada_de_Linhas
saida = Saida

# Camada de Poligonos
poligonos = processing.getObject(poligono)
# Camada de Linhas
linhas = processing.getObject(linha)
# Validacao dos parametros de entrada
validacao = True
if linhas.geometryType() != QGis.Line:
    validacao = False
    progress.setInfo('<b>A camada a ser recortada deve ser do tipo "Linha" !</b><br/>')
if not (poligonos.geometryType() == QGis.Line or poligonos.geometryType() == QGis.Polygon):
    validacao = False
    progress.setInfo('<b>A camada recortante deve ser do tipo "Linha" ou "Poligono"!</b><br/>')
if not validacao:
    time.sleep(6)
    iface.messageBar().pushMessage(u'Situacao', "Problema nos parametros de entrada!", level=QgsMessageBar.WARNING, duration=5)

# Criar camada de Saida (linhas cortadas)
fields = linhas.pendingFields()
CRS = linhas.crs()
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBLineString, CRS, formato)

if poligonos.geometryType() == QGis.Polygon:
    # Gerar camada do anel exterior dos poligonos
    anel = processing.runalg('script:extrairanelexterior', poligonos, None)
    recortante = processing.getObject(anel['Saida'])
else:
    recortante = processing.getObject(poligono)

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
    att = lin.attributes()
    coord = geom.asPolyline()
    if coord == []:
        coord = geom.asMultiPolyline()
        for item in coord:
            lista_lin += [(item, att)]
    else:
        lista_lin += [(coord, att)]

# Ober lista de poligonos
lista_pol = []
for pol in recortante.getFeatures():
    geom = pol.geometry()
    coord = geom.asPolyline()
    if coord == []:
        coord = geom.asMultiPolyline()
        for item in coord:
            lista_pol += [item]
    else:
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
        writer.addFeature(feature)
        del lista_lin[0]

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)
