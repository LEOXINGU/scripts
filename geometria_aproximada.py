"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-09-13
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
# Atualizacao de Geometria Aproximada

##LF2) Revisao=group
##17. Geometria Aproximada=name
##Banco_de_Dados_da_Reambulacao=string
##Banco_de_Dados_da_Vetorizacao=string
##Tolerancia_do_Buffer_em_metros=number 5.0
##Percentual_de_Buffer_para_Linhas_e_Poligonos=number 90
##Usuario_PostGIS=string postgres
##Senha=string postgres

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

BD_Vetor = Banco_de_Dados_da_Vetorizacao
BD_Reamb = Banco_de_Dados_da_Reambulacao
tol = Tolerancia_do_Buffer_em_metros
percentual = Percentual_de_Buffer_para_Linhas_e_Poligonos/100.0

uriA = QgsDataSourceURI()
uriA.setConnection("localhost","5432", BD_Vetor, Usuario_PostGIS, Senha)

# Abrir as camadas
    # Objeto Desconhecido Ponto
uriA.setDataSource("public","aux_objeto_desconhecido_p","geom","")
obj_desc_pnt = QgsVectorLayer(uriA.uri(), '', "postgres")
    # Objeto Desconhecido Linha
uriA.setDataSource("public","aux_objeto_desconhecido_l","geom","")
obj_desc_lin = QgsVectorLayer(uriA.uri(), '', "postgres")
    # Objeto Desconhecido Area
uriA.setDataSource("public","aux_objeto_desconhecido_a","geom","")
obj_desc_pol = QgsVectorLayer(uriA.uri(), '', "postgres")
    # Massa Dagua e Trecho de Massa Dagua
uriA.setDataSource("cb","hid_massa_dagua_a","geom","")
MassaDagua = QgsVectorLayer(uriA.uri(), '', "postgres")
uriA.setDataSource("cb","hid_trecho_massa_dagua_a","geom","")
TrechoMassaDagua = QgsVectorLayer(uriA.uri(), '', "postgres")
    # Trecho Rodoviario
uriA.setDataSource("cb","tra_trecho_rodoviario_l","geom","")
TrechoRodoviario = QgsVectorLayer(uriA.uri(), '', "postgres")

# Criar lista de Pontos com geometria Aproximada "NAO"
PONTOS = []
for feat in obj_desc_pnt.getFeatures():
    geom = feat.geometry()
    if geom:
        geomBuffer = geom.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            PONTOS += [coord]

# Criar lista de Linhas com geometria Aproximada "NAO"
LINHAS = []
for feat in obj_desc_lin.getFeatures():
    geom = feat.geometry()
    if geom:
        geomBuffer = geom.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            LINHAS += [coord]

# Criar lista de Poligonos com geometria Aproximada "NAO"
POLIGONOS = []
for feat in obj_desc_pol.getFeatures():
    pol = feat.geometry()
    if pol:
        coord = pol.asMultiPolygon()
        lin = QgsGeometry.fromMultiPolyline(coord[0])
        geomBuffer = lin.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            POLIGONOS += [coord]

# Criar lista de Trecho de Drenagem com geometria Aproximada "NAO"
DRENAGEM = []
for feat in drenagem.getFeatures():
    geom = feat.geometry()
    if geom:
        geomBuffer = geom.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            DRENAGEM += [coord]

# Criar lista de Massa Dagua com geometria Aproximada "NAO"
MASSADAGUA = []
for feat in MassaDagua.getFeatures():
    pol = feat.geometry()
    if pol:
        coord = pol.asMultiPolygon()
        lin = QgsGeometry.fromMultiPolyline(coord[0])
        geomBuffer = lin.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            MASSADAGUA += [coord]
for feat in TrechoMassaDagua.getFeatures():
    pol = feat.geometry()
    if pol:
        coord = pol.asMultiPolygon()
        lin = QgsGeometry.fromMultiPolyline(coord[0])
        geomBuffer = lin.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            MASSADAGUA += [coord]

# Criar lista de Trecho Rodoviario com geometria Aproximada "NAO"
RODOVIAS = []
for feat in TrechoRodoviario.getFeatures():
    geom = feat.geometry()
    if geom:
        geomBuffer = geom.buffer(tol, 5)
        coord = geomBuffer.asPolygon()
        if coord:
            RODOVIAS += [coord]

Outras = ['hid_trecho_drenagem_l',
                'hid_massa_dagua_a',
                'hid_trecho_massa_dagua_a',
                'rel_ponto_cotado_altimetrico_p',
                'rel_curva_nivel_l',
                'rel_elemento_fisiog_natural_l']


for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0 and (layer.source()).split("'")[1]==BD_Reamb:
        # Pontos
        if layer.geometryType() == QGis.Point and not(layer.name() in Outras):
            att_column = layer.pendingFields().fieldNameIndex('geometriaaproximada')
            if att_column !=-1:
                DP = layer.dataProvider()
                for feat in layer.getFeatures():
                    geom = feat.geometry()
                    if geom:
                        for item in PONTOS:
                            geomBuffer = QgsGeometry.fromPolygon(item)
                            if geom.intersects(geomBuffer):
                                newColumnValueMap = {att_column : 2} # Geometria aproximada nao
                                newAttributesValuesMap = {feat.id() : newColumnValueMap}
                                DP.changeAttributeValues(newAttributesValuesMap)
        # Linhas
        if layer.geometryType() == QGis.Line and not(layer.name() in Outras):
            att_column = layer.pendingFields().fieldNameIndex('geometriaaproximada')
            if att_column !=-1:
                DP = layer.dataProvider()
                for feat in layer.getFeatures():
                    geom = feat.geometry()
                    if geom:
                        comp = geom.length()
                        for item in LINHAS:
                            geomBuffer = QgsGeometry.fromPolygon(item)
                            if geom.intersects(geomBuffer):
                                intersecao = geom.intersection(geomBuffer)
                                comp_inter = intersecao.length()
                                if (comp_inter/comp) >= percentual:
                                    newColumnValueMap = {att_column : 2} # Geometria aproximada nao
                                    newAttributesValuesMap = {feat.id() : newColumnValueMap}
                                    DP.changeAttributeValues(newAttributesValuesMap)
        # Poligonos
        if layer.geometryType() == QGis.Polygon and not(layer.name() in Outras):
            att_column = layer.pendingFields().fieldNameIndex('geometriaaproximada')
            if att_column !=-1:
                DP = layer.dataProvider()
                for feat in layer.getFeatures():
                    pol = feat.geometry()
                    if pol:
                        coord = pol.asMultiPolygon()
                        lin = QgsGeometry.fromPolyline(coord[0][0])
                        comp = lin.length()
                        for item in POLIGONOS:
                            geomBuffer = QgsGeometry.fromPolygon(item)
                            if lin.intersects(geomBuffer):
                                intersecao = lin.intersection(geomBuffer)
                                comp_inter = intersecao.length()
                                if (comp_inter/comp) >= percentual:
                                    newColumnValueMap = {att_column : 2} # Geometria aproximada nao
                                    newAttributesValuesMap = {feat.id() : newColumnValueMap}
                                    DP.changeAttributeValues(newAttributesValuesMap)
                                    
        # Rodovias
        if layer.name() == 'tra_trecho_rodoviario_l':
            att_column = layer.pendingFields().fieldNameIndex('geometriaaproximada')
            if att_column !=-1:
                DP = layer.dataProvider()
                for feat in layer.getFeatures():
                    geom = feat.geometry()
                    if geom:
                        comp = geom.length()
                        for item in RODOVIAS:
                            geomBuffer = QgsGeometry.fromPolygon(item)
                            if geom.intersects(geomBuffer):
                                intersecao = geom.intersection(geomBuffer)
                                comp_inter = intersecao.length()
                                if (comp_inter/comp) >= percentual:
                                    newColumnValueMap = {att_column : 2} # Geometria aproximada nao
                                    newAttributesValuesMap = {feat.id() : newColumnValueMap}
                                    DP.changeAttributeValues(newAttributesValuesMap)
                                    
        # Corpo Dagua
        if layer.name()  == 'hid_massa_dagua_a' or layer.name()  == 'hid_trecho_massa_dagua_a':
            att_column = layer.pendingFields().fieldNameIndex('geometriaaproximada')
            if att_column !=-1:
                DP = layer.dataProvider()
                for feat in layer.getFeatures():
                    pol = feat.geometry()
                    if pol:
                        coord = pol.asMultiPolygon()
                        lin = QgsGeometry.fromPolyline(coord[0][0])
                        comp = lin.length()
                        for item in MASSADAGUA:
                            geomBuffer = QgsGeometry.fromPolygon(item)
                            if lin.intersects(geomBuffer):
                                intersecao = lin.intersection(geomBuffer)
                                comp_inter = intersecao.length()
                                if (comp_inter/comp) >= percentual:
                                    newColumnValueMap = {att_column : 2} # Geometria aproximada nao
                                    newAttributesValuesMap = {feat.id() : newColumnValueMap}
                                    DP.changeAttributeValues(newAttributesValuesMap)


progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)