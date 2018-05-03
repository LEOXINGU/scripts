"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-04-30
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

# Rede de Drenagem
##Rede de Drenagem=name
##LF09) Validacao=group
##Camada_de_linhas=vector
##Moldura=vector
##Angulo_minimo=number 45.0
##Tolerancia=number 0.5
##Insconsistencias=output vector
##Pontos_de_drenagem=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from math import radians, cos, sqrt

# Abrir camada de linhas
linhas = processing.getObject(Camada_de_linhas)

# Validacao de dados de entrada
if linhas.geometryType() != QGis.Line:
    progress.setInfo('<br/><br/><b>As camadas devem ser do tipo linha!</b>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "As camadas devem ser do tipo linha!", level=QgsMessageBar.CRITICAL, duration=5)
elif Angulo_minimo<0 or Angulo_minimo>90:
    progress.setInfo('<br/><br/><b>Angulo minimo deve estar entre 0 e 90 graus!</b>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "Angulo minimo deve estar entre 0 e 90 graus!", level=QgsMessageBar.CRITICAL, duration=5)
elif Tolerancia<=0:
    progress.setInfo('<br/><br/><b>Tolerancia deve ser positiva!</b>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "Tolerancia deve ser positiva!", level=QgsMessageBar.CRITICAL, duration=5)
 else:
 
    COS_ALFA = cos(radians(Angulo_minimo))
    # Funcao Cosseno de Alfa
    def CosAlfa(v1, v2):
        return (v1[0]*v2[0]+v1[1]*v2[1])/(sqrt(v1[0]*v1[0]+v1[1]*v1[1])*sqrt(v2[0]*v2[0]+v2[1]*v2[1]))
        
    # pontos a montante e jusante
    lin_list = []
    PM, PJ, ATT = {},{},{}
    for feat in linhas.getFeatures():
            geom = feat.geometry()
            if geom:
                lin = geom.asPolyline()
                if not (lin):
                    lin = geom.asMultiPolyline()[0]
                lin_list +=[lin]
                ID = feat.id()
                att = [feat.attributes()[1:]]
                PM[ID] = {'coord':lin[0], 'M':[], 'J':[]}
                PJ[ID] = {'coord':lin[-1], 'M':[], 'J':[]}
                ATT[ID] = att

    # Abrir moldura
    moldura = processing.getObject(Moldura)
    SRC = moldura.crs()
    feat = moldura.getFeatures().next()
    pol = feat.geometry()
    coord = pol.asMultiPolygon()
    moldura_linha = QgsGeometry.fromMultiPolyline(coord[0])
    if SRC.geographicFlag():
        moldura_buffer = moldura_linha.buffer(Tolerancia/110000,5)
    else:
        moldura_buffer = moldura_linha.buffer(Tolerancia,5)

    # Criar camada de inconsistencias
    fields = QgsFields()
    fields.append(QgsField('problema', QVariant.String))
    writer1 = QgsVectorFileWriter(Insconsistencias, 'utf-8', fields, QGis.WKBPoint, SRC, 'ESRI Shapefile')

    # Criar camada de Pontos de Drenagem
    fields = QgsFields()
    fields.append(QgsField('tipo', QVariant.String))
    writer2 = QgsVectorFileWriter(Pontos_de_drenagem, 'utf-8', fields, QGis.WKBPoint, SRC, 'ESRI Shapefile')

    # Checar auto-intersecao
    progress.setInfo('<b>Verificando auto-intersecoes...</b><br/>')
    lista_pnts = []
    feature = QgsFeature()
    for coord in lin_list:
        tam = len(coord)
        if tam > 3:
            for i in range(0,tam-3):
                segA = [coord[i], coord[i+1]]
                geomA = QgsGeometry.fromPolyline(segA)
                for j in range(i+2,tam-1):
                    segB = [coord[j], coord[j+1]]
                    geomB = QgsGeometry.fromPolyline(segB)
                    if geomA.crosses(geomB):
                        point = geomA.intersection(geomB)
                        if not(point in lista_pnts or point.asPoint() == coord[0]):
                            lista_pnts += [point]
                            feature.setAttributes(['Auto-intersecao'])
                            feature.setGeometry(point)
                            writer1.addFeature(feature)

    # Checar se linhas se cruzam ou se sobrepoe
    progress.setInfo('<b>Verificando se as linhas se cruzam ou se sobrepoe...</b><br/>')
    tam = len(lin_list)
    feature = QgsFeature()
    for i in range(0,tam-1):
        for j in range(i+1,tam):
            linA = QgsGeometry.fromPolyline(lin_list[i])
            linB = QgsGeometry.fromPolyline(lin_list[j])
            if linA.crosses(linB):
                Intersecao = linA.intersection(linB)
                feature.setAttributes(['Cruzamento entre linhas'])
                if Intersecao.isMultipart():
                    for ponto in Intersecao.asMultiPoint():
                        feature.setGeometry(QgsGeometry.fromPoint(ponto))
                        writer1.addFeature(feature)
                else:
                    feature.setGeometry(Intersecao)
                    writer1.addFeature(feature)
            elif linA.intersects(linB):
                Intersecao = linA.intersection(linB)
                if Intersecao.type() == 1: # Tipo linha
                    feature.setAttributes(['Sobreposicao entre linhas'])
                    if Intersecao.isMultipart():
                        for linha in Intersecao.asMultiPolyline():
                            geom = QgsGeometry.fromPolyline(linha)
                            feature.setGeometry(geom.centroid())
                            writer1.addFeature(feature)
                    else:
                        feature.setGeometry(Intersecao.centroid())
                        writer1.addFeature(feature)

    # Verificar Angulos Fechados
    progress.setInfo('<b>Verificando angulos fechados...</b><br/>')
    feature = QgsFeature()
    for coord in lin_list:
        ind = 0
        while ind < len(coord)-2:
            p1 = coord[ind]
            p2 = coord[ind+1]
            p3 = coord[ind+2]
            v1 = [p1.x()-p2.x(), p1.y()-p2.y()]
            v2 = [p3.x()-p2.x(), p3.y()-p2.y()]
            if CosAlfa(v1, v2) > COS_ALFA:
                feature.setAttributes(['Angulo Fechado'])
                feature.setGeometry(QgsGeometry.fromPoint(p2))
                writer1.addFeature(feature)
            ind += 1

    # Gerar relacionamento entre PM e PJ
    progress.setInfo('<b>Gerando rede de drenagem...</b><br/>')
    ID = PM.keys()
    tam = len(ID)
    for i in range(0,tam-1):
        for j in range(i+1,tam):
            pntM_A = PM[ID[i]]['coord']
            pntJ_A  = PJ[ID[i]]['coord']
            att_A = ATT[ID[i]]
            pntM_B = PM[ID[j]]['coord']
            pntJ_B  = PJ[ID[j]]['coord']
            att_B = ATT[ID[j]]
            if pntM_A == pntM_B:
                PM[ID[i]]['M'] += [[ID[j], att_A == att_B]]
            elif pntM_A == pntJ_B:
                PM[ID[i]]['J'] += [[ID[j], att_A == att_B]]
            
            if pntJ_A == pntM_B:
                PJ[ID[i]]['M'] += [[ID[j], att_A == att_B]]
            elif pntJ_A == pntJ_B:
                PJ[ID[i]]['J'] += [[ID[j], att_A == att_B]]

    # Verificando problemas na rede
    progress.setInfo('<b>Verificando problema(s) de rede...</b><br/>')
    feat = QgsFeature()
    for id in ID:
        # ponto de jusante
        geom = QgsGeometry.fromPoint(PJ[id]['coord'])
        feat.setGeometry(geom)
        if len(PJ[id]['M'])>1 and len(PJ[id]['J'])==0: # ponto de ramificacao
            feat.setAttributes(['ramificacao'])
            writer2.addFeatures([feat])
            continue
        elif len(PJ[id]['M'])==1 and len(PJ[id]['J'])==0: # mudanca de atributos
            feat.setAttributes(['mudanca de atributo'])
            writer2.addFeatures([feat])
            continue
        elif len(PJ[id]['M'])==1 and len(PJ[id]['J'])>=1: # ponto de confluencia
            continue
        elif len(PJ[id]['M'])==0 and len(PJ[id]['J'])==0 and geom.disjoint(moldura_buffer): # sumidouro, foz, desembocadura
            feat.setAttributes(['sumidouro'])
            writer2.addFeatures([feat])
            continue
        else:
            feat.setAttributes(['problema de rede'])
            writer1.addFeatures([feat])
        # ponto de montante
        geom = QgsGeometry.fromPoint(PM[id]['coord'])
        feat.setGeometry(geom)
        if len(PM[id]['M'])>=1 and len(PM[id]['J'])==1: # ponto de ramificacao
            continue
        elif len(PM[id]['M'])==0 and len(PM[id]['J'])>1: # ponto de confluencia
            feat.setAttributes(['confluencia'])
            writer2.addFeatures([feat])
            continue
        elif len(PM[id]['M'])==0 and len(PM[id]['J'])==0 and geom.disjoint(moldura_buffer): # nascente, vertedouro
            feat.setAttributes(['vertedouro'])
            writer2.addFeatures([feat])
            continue
        elif len(PM[id]['M'])==0 and len(PM[id]['J'])==1: # mudanca de atributo
            continue
        else:
            att = ['problema de rede']
            feat.setAttributes(att)
            writer1.addFeatures([feat])


    del writer1, writer2
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(5)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
