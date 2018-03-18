"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-02-20
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
##Consistencia Topologica de CT=name
##LF09) Validacao=group
##Camada_de_linhas=vector
##Moldura=vector
##Tolerancia=number 0.5
##Insconsistencias=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

# Abrir camada de linhas
linhas = processing.getObject(Camada_de_linhas)
lin_list = []
for feat in linhas.getFeatures():
        geom = feat.geometry()
        if geom:
            lin = geom.asPolyline()
            if not (lin):
                lin = geom.asMultiPolyline()[0]
            lin_list +=[lin]

# Abrir moldura
moldura = processing.getObject(Moldura)
SRC = moldura.crs()
feat = moldura.getFeatures().next()
pol = feat.geometry()
coord = pol.asMultiPolygon()
moldura_linha = QgsGeometry.fromMultiPolyline(coord[0])
moldura_buffer = moldura_linha.buffer(Tolerancia/110000,5)

# Criar camada de inconsistencias
fields = QgsFields()
fields.append(QgsField('problema', QVariant.String))
writer = QgsVectorFileWriter(Insconsistencias, 'utf-8', fields, QGis.WKBPoint, SRC, 'ESRI Shapefile')

# Checar se linhas se cruzam
progress.setInfo('<b>Verificando se as linhas se cruzam...</b><br/>')
tam = len(lin_list)
feature = QgsFeature()
for i in range(0,tam-1):
    for j in range(i+1,tam):
        linA = QgsGeometry.fromPolyline(lin_list[i])
        linB = QgsGeometry.fromPolyline(lin_list[j])
        if linA.crosses(linB):
            Intersecao = linA.intersection(linB)
            feature.setAttributes(['Instersecao entre linhas'])
            feature.setGeometry(Intersecao)
            writer.addFeature(feature)

# Checar se uma feicao nao toca outra feicao ou moldura
progress.setInfo('<b>Verificando se as linhas toca outra feicao ou a moldura...</b><br/>')
for i in range(tam):
    tocaIni = False
    tocaFim = False
    pnt_Ini_A = QgsGeometry.fromPoint(lin_list[i][0])
    pnt_Fim_A = QgsGeometry.fromPoint(lin_list[i][-1])
    for j in range(tam):
        if i != j:
            lin_B = QgsGeometry.fromPolyline(lin_list[j])
            # Ponto inicial
            if pnt_Ini_A.intersects(lin_B) or pnt_Ini_A.intersects(moldura_buffer):
                tocaIni = True
            # Ponto final
            if pnt_Fim_A.intersects(lin_B) or  pnt_Fim_A.intersects(moldura_buffer):
                tocaFim = True
    # Gerar Ponto de Inconsistencia
    if not(tocaIni and tocaFim):
        if not (pnt_Ini_A.intersects(pnt_Fim_A)):
            if not tocaIni:
                feature.setAttributes(['Ponta Solta'])
                feature.setGeometry(pnt_Ini_A)
                writer.addFeature(feature)
            if not tocaFim:
                feature.setAttributes(['Ponta Solta'])
                feature.setGeometry(pnt_Fim_A)
                writer.addFeature(feature)
    progress.setPercentage(int((i+1)/float(tam)*100))

del writer
progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)