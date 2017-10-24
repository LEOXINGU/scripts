"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-20
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
# Fechar Anel Linear
##Fechar Anel Linear=name
##LF4) Vetor=group
##Camada_de_entrada=vector
##Tolerancia=number 10.0
##Tipo_de_conexao=selection Ponto Medio;Ligar ultimo ao primeiro;Deslocar ultimo ao primeiro;Deslocar primeiro ao ultimo

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
from processing.tools.vector import VectorWriter
import time

layer = processing.getObject(Camada_de_entrada)

def Conectar(Tipo_de_conexao, coord_list):
    if Tipo_de_conexao == 0:
        P_ini=coord_list[0]
        P_fim=coord_list[-1]
        P_medio = QgsPoint(0.5*(P_ini.x()+P_fim.x()),0.5*(P_ini.y()+P_fim.y()))
        coord_list[0] = P_medio
        coord_list[-1] = P_medio
    elif Tipo_de_conexao == 1:
        coord_list += [coord_list[0]]
    elif Tipo_de_conexao == 2:
        P_ini=coord_list[0]
        coord_list[-1] = P_ini
    elif Tipo_de_conexao == 3:
        P_fim=coord_list[-1]
        coord_list[0] = P_fim
    return coord_list

if layer.crs().geographicFlag():
    Tolerancia/= float(111000)
    
if layer.type()==0 and layer.geometryType() == QGis.Line:
    DP = layer.dataProvider()
    # Quebrar multipartes
    for feat in layer.getFeatures():
        geom = feat.geometry()
        if geom:
            coord = geom.asMultiPolyline()
            if len(coord)>1:
                # Atualizar a geometria da feicao com a geometria com apenas uma parte
                new_geom = QgsGeometry.fromMultiPolyline([coord[0]])
                newGeomMap = {feat.id() : new_geom}
                ok = DP.changeGeometryValues(newGeomMap)
                # Criar novas feicoes com as outras partes
                att = feat.attributes()
                new_att = [None] + att[1:]
                new_feat = QgsFeature()
                for i in range(1, len(coord)):
                    new_geom = QgsGeometry.fromMultiPolyline([coord[i]])
                    new_feat.setGeometry(new_geom)
                    new_feat.setAttributes(new_att)
                    ok = DP.addFeatures([new_feat])
    
    # Fechar anel
    for feat in layer.getFeatures():
        geom = feat.geometry()
        coord = geom.asPolyline()
        if coord:
            P_ini = coord[0]
            P_fim = coord[-1]
            Multiparte = False
        else:
            Multiparte = True
            coord = geom.asMultiPolyline()
            P_ini = coord[0][0]
            P_fim = coord[0][-1]
        # Verificar se o ponto inicial e final estao na tolerancia
        Pnt_ini = QgsGeometry.fromPoint(P_ini)
        Pnt_fim = QgsGeometry.fromPoint(P_fim)
        if Pnt_ini.intersects(Pnt_fim.buffer(Tolerancia, 5)):
            if not(P_ini == P_fim):
                # Atualizar a geometria da feicao com a geometria com apenas uma parte
                if Multiparte:
                    coord = coord[0]
                    coord = Conectar(Tipo_de_conexao, coord)
                    new_geom = QgsGeometry.fromMultiPolyline([coord])
                else:
                    coord = Conectar(Tipo_de_conexao, coord)
                    new_geom = QgsGeometry.fromPolyline(coord)
                newGeomMap = {feat.id() : new_geom}
                ok = DP.changeGeometryValues(newGeomMap)

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)