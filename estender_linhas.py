"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-08-14
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

# Estender linhas
##Estender Linhas=name
##LF04) Vetor=group
##Camada_de_linhas=vector
##Moldura=vector
##Distancia=number 0.5
##Linhas_Estendidas=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from numpy import array
from numpy.linalg import norm

# Abrir camada de linhas
linhas = processing.getObject(Camada_de_linhas)
SRC_linhas = linhas.crs()

# Abrir moldura
moldura = processing.getObject(Moldura)
SRC = moldura.crs()

# Validacao dos dados de entrada
if not(SRC_linhas == SRC and linhas.geometryType() == QGis.Line and moldura.geometryType() == QGis.Polygon):
    progress.setInfo('<b><font  color="#ff0000">Erro nos parametros de entrada. Possiveis erros:</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. As camadas devem ter o mesmo SRC.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. A camada de linhas deve ser do tipo linha.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. A camada da moldura deve ser do tipo poligono.</b><br/>')
    iface.messageBar().pushMessage(u'Situacao', "Problema com os dados de entrada!", level=QgsMessageBar.WARNING, duration=8)
else:
    # Pegar poligono da moldura
    feat = moldura.getFeatures().next()
    pol = feat.geometry()
    coord = pol.asMultiPolygon()
    if coord:
        moldura_linha = QgsGeometry.fromMultiPolyline(coord[0])
    else:
        coord = pol.asPolygon()
        moldura_linha = QgsGeometry.fromMultiPolyline(coord)

    if SRC.geographicFlag():
        Distancia = Distancia/110000.0
        moldura_buffer = moldura_linha.buffer(Distancia,5)
    else:
        moldura_buffer = moldura_linha.buffer(Distancia,5)

    # Criar camada de Linhas Estendidas
    fields = linhas.pendingFields()
    writer = QgsVectorFileWriter(Linhas_Estendidas, 'utf-8', fields, QGis.WKBLineString, SRC, 'ESRI Shapefile')

    # Varrer linhas
    feature = QgsFeature()
    tam = linhas.featureCount()
    for index, feat in enumerate(linhas.getFeatures()):
        geom = feat.geometry()
        att = feat.attributes()
        if geom:
            line = geom.asPolyline()
            if not (line):
                lines = geom.asMultiPolyline()
                for line in lines:                        
                    P1 = line[0]
                    P2 = line[1]
                    Pn = line[-1]
                    Pn_1 = line[-2]
                    P_ini =  QgsGeometry.fromPoint(P1)
                    P_fim =  QgsGeometry.fromPoint(Pn)
                    if not P_ini.intersects(moldura_buffer):
                        vetor = array(P1) - array(P2)
                        P = array(P1) + vetor/norm(vetor)*Distancia
                        P1 = QgsPoint(P[0], P[1])
                    if not P_fim.intersects(moldura_buffer):
                        vetor = array(Pn) - array(Pn_1)
                        P = array(Pn) + vetor/norm(vetor)*Distancia
                        Pn = QgsPoint(P[0], P[1])
                    line = [P1] + line[1:-1] + [Pn]
                    new_geom = QgsGeometry.fromPolyline(line)
                    feature.setAttributes(att)
                    feature.setGeometry(new_geom)
                    writer.addFeature(feature)
            else:
                P1 = line[0]
                P2 = line[1]
                Pn = line[-1]
                Pn_1 = line[-2]
                P_ini =  QgsGeometry.fromPoint(P1)
                P_fim =  QgsGeometry.fromPoint(Pn)
                if not P_ini.intersects(moldura_buffer):
                    vetor = array(P1) - array(P2)
                    P = array(P1) + vetor/norm(vetor)*Distancia
                    P1 = QgsPoint(P[0], P[1])
                if not P_fim.intersects(moldura_buffer):
                    vetor = array(Pn) - array(Pn_1)
                    P = array(Pn) + vetor/norm(vetor)*Distancia
                    Pn = QgsPoint(P[0], P[1])
                line = [P1] + line[1:-1] + [Pn]
                new_geom = QgsGeometry.fromPolyline(line)
                feature.setAttributes(att)
                feature.setGeometry(new_geom)
                writer.addFeature(feature)
                
        progress.setPercentage(int((index+1)/float(tam)*100))

    del writer
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
