"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-03-31
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
# Mesclar linhas na direcao
##1. Mesclar na Direcao=name
##arquivo=vector
##tolerancia=number 10
##atributos=selection Mesclar com mesmos atributos;Manter atributos da maior feicao
##saida=output vector
##LF04) Vetor=group
# inputs
filename = arquivo
output_name = saida
tol = tolerancia
from math import atan2, degrees, fabs
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

# Abrir layer de linhas
linhas = processing.getObject(filename)

# Funcao que pega ponto incial e final e os seus angulos
def pontos_ang(feature):
    att = feature.attributes()
    geom = feature.geometry()
    coord = geom.asPolyline()
    if coord != []:
            # Tangente entre o primeiro e segundo ponto
            Xa = coord[0].x()
            Xb = coord[1].x()
            Ya = coord[0].y()
            Yb = coord[1].y()
            ang_ini = degrees(atan2(Yb-Ya,Xb-Xa))
            Xa = coord[-2].x()
            Xb = coord[-1].x()
            Ya = coord[-2].y()
            Yb = coord[-1].y()
            ang_fim = degrees(atan2(Yb-Ya,Xb-Xa))
            return [[coord, coord[0], coord[-1], ang_ini, ang_fim, att]]
    elif geom.asMultiPolyline():
        coord = geom.asMultiPolyline()
        itens = []
        for item in coord:
            Xa = item[0].x()
            Xb = item[1].x()
            Ya = item[0].y()
            Yb = item[1].y()
            ang_ini = degrees(atan2(Yb-Ya,Xb-Xa))
            Xa = item[-2].x()
            Xb = item[-1].x()
            Ya = item[-2].y()
            Yb = item[-1].y()
            ang_fim = degrees(atan2(Yb-Ya,Xb-Xa))
            itens += [[item, item[0], item[-1], ang_ini, ang_fim, att]]
        return itens

# Funcao para dar a direcao oposta
def contraAz(x):
    if x<=0:
        return x+180
    else:
        return x-180

# Validacao dos dados de entrada
validacao = True
if tol >90 or tol <0:
    validacao = False
    progress.setInfo('<b>O valor da tolerancia deve estar entre 0 e 90 graus!</b><br/>')
if linhas.geometryType() != QGis.Line:
    validacao = False
    progress.setInfo('<b>A camada de entrada deve ser do tipo "Linha"!</b><br/>')
if not validacao:
    time.sleep(6)
    iface.messageBar().pushMessage(u'Situacao', "Problema nos parametros de entrada!", level=QgsMessageBar.WARNING, duration=5)

if validacao:
    progress.setInfo('<b>Iniciando processamento...</b><br/>')

    # Criar lista com informacoes das feicoes
    lista = []
    for feature in linhas.getFeatures():
            lista += pontos_ang(feature)

    # Criar uma nova lista com as feicoes finais mescladas
    nova_lista = []
    # Remover os aneis lineares da lista e acrescentar na nova lista
    ind = 0
    while ind < len(lista)-1:
        P_ini = lista[ind][1]
        P_fim = lista[ind][2]
        if P_ini==P_fim:
            nova_lista+= [lista[ind][0]]
            del  lista[ind]
        else:
            ind +=1

    # Mesclar linhas que se tocam e tem a mesma direcao (com mesmo atributo)
    if atributos == 0:
        while len(lista)>1:
            tam = len(lista)
            for i in range(0,tam-1):
                mergeou = False
                # Ponto inicial e final da feicao A
                coord_A = lista[i][0]
                P_ini_A = lista[i][1]
                P_fim_A = lista[i][2]
                ang_ini_A = lista[i][3]
                ang_fim_A = lista[i][4]
                att_A = lista[i][5]
                for j in range(i+1,tam):
                    # Ponto inicial e final da feicao B
                    coord_B = lista[j][0]
                    P_ini_B = lista[j][1]
                    P_fim_B = lista[j][2]
                    ang_ini_B = lista[j][3]
                    ang_fim_B = lista[j][4]
                    att_B = lista[j][5]
                    if att_A == att_B:
                        # 4 possibilidades
                        # 1 - Ponto final de A igual ao ponto inicial de B
                        if (P_fim_A == P_ini_B) and (fabs(ang_fim_A-ang_ini_B)<tol or fabs(360-fabs(ang_fim_A-ang_ini_B))<tol):
                            mergeou = True
                            break
                        # 2 - Ponto inicial de A igual ao ponto final de B
                        elif (P_ini_A == P_fim_B) and (fabs(ang_ini_A-ang_fim_B)<tol or fabs(360-fabs(ang_ini_A-ang_fim_B))<tol):
                            mergeou = True
                            break
                        # 3 - Ponto incial de A igual ao ponto inicial de B
                        elif (P_ini_A == P_ini_B) and (fabs(ang_ini_A-contraAz(ang_ini_B))<tol or fabs(360-fabs(ang_ini_A-contraAz(ang_ini_B)))<tol):
                            mergeou = True
                            break
                        # 4 - Ponto final de A igual ao ponto final de B
                        elif (P_fim_A == P_fim_B) and (fabs(ang_fim_A-contraAz(ang_fim_B))<tol or fabs(360-fabs(ang_fim_A-contraAz(ang_fim_B)))<tol):
                            mergeou = True
                            break
                if mergeou:
                    geom_A = QgsGeometry.fromPolyline(coord_A)
                    geom_B = QgsGeometry.fromPolyline(coord_B)
                    new_geom = geom_A.combine(geom_B)
                    
                    new_feat = QgsFeature()
                    new_feat.setAttributes(att_A)
                    new_feat.setGeometry(new_geom)
                    
                    if new_geom.isMultipart():
                        nova_lista += [[coord_A, att_A], [coord_B, att_B]]
                        del lista[i], lista[j-1]
                        break
                    else:
                        del lista[i], lista[j-1]
                        lista = pontos_ang(new_feat)+lista
                        break
                if not(mergeou):
                    # Tirar a geometria que nao se conecta com nada da lista
                    nova_lista += [[coord_A, att_A]]
                    del lista[i]
                    break
            if len(lista)==1:
                nova_lista += [[lista[0][0], lista[0][5]]]
            
    # Mesclar os que se tocam e tem mesma direcao (preservar atributos da linha maior)
    if atributos == 1:
        while len(lista)>1:
            tam = len(lista)
            for i in range(0,tam-1):
                mergeou = False
                # Ponto inicial e final da feicao A
                coord_A = lista[i][0]
                P_ini_A = lista[i][1]
                P_fim_A = lista[i][2]
                ang_ini_A = lista[i][3]
                ang_fim_A = lista[i][4]
                att_A = lista[i][5]
                for j in range(i+1,tam):
                    # Ponto inicial e final da feicao B
                    coord_B = lista[j][0]
                    P_ini_B = lista[j][1]
                    P_fim_B = lista[j][2]
                    ang_ini_B = lista[j][3]
                    ang_fim_B = lista[j][4]
                    att_B = lista[j][5]
                    # 4 possibilidades
                    # 1 - Ponto final de A igual ao ponto inicial de B
                    if (P_fim_A == P_ini_B) and (fabs(ang_fim_A-ang_ini_B)<tol or fabs(360-fabs(ang_fim_A-ang_ini_B))<tol):
                        mergeou = True
                        break
                    # 2 - Ponto inicial de A igual ao ponto final de B
                    elif (P_ini_A == P_fim_B) and (fabs(ang_ini_A-ang_fim_B)<tol or fabs(360-fabs(ang_ini_A-ang_fim_B))<tol):
                        mergeou = True
                        break
                    # 3 - Ponto incial de A igual ao ponto inicial de B
                    elif (P_ini_A == P_ini_B) and (fabs(ang_ini_A-contraAz(ang_ini_B))<tol or fabs(360-fabs(ang_ini_A-contraAz(ang_ini_B)))<tol):
                        mergeou = True
                        break
                    # 4 - Ponto final de A igual ao ponto final de B
                    elif (P_fim_A == P_fim_B) and (fabs(ang_fim_A-contraAz(ang_fim_B))<tol or fabs(360-fabs(ang_fim_A-contraAz(ang_fim_B)))<tol):
                        mergeou = True
                        break
                if mergeou:
                    geom_A = QgsGeometry.fromPolyline(coord_A)
                    geom_B = QgsGeometry.fromPolyline(coord_B)
                    new_geom = geom_A.combine(geom_B)
                    
                    length_A = geom_A.length()
                    length_B = geom_B.length()
                    if length_A > length_B:
                        att = att_A
                    else:
                        att = att_B
                    new_feat = QgsFeature()
                    new_feat.setAttributes(att)
                    new_feat.setGeometry(new_geom)
                    
                    if new_geom.isMultipart():
                        nova_lista += [[coord_A, att_A], [coord_B, att_B]]
                        del lista[i], lista[j-1]
                        break
                    else:
                        del lista[i], lista[j-1]
                        lista = pontos_ang(new_feat)+lista
                        break
                if not(mergeou):
                    # Tirar a geometria que nao se conecta com nada da lista
                    nova_lista += [[coord_A, att_A]]
                    del lista[i]
                    break
            if len(lista)==1:
                nova_lista += [[lista[0][0], lista[0][5]]]
    
    # Criando o shapefile de saida
    progress.setInfo('<b>Criando shapefile de saida...</b><br/>')
    path_name = output_name
    encoding = 'utf-8'
    formato = 'ESRI Shapefile'
    crs = linhas.crs()
    # Criar campos
    fields = linhas.pendingFields()

    writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBLineString, crs, formato)

    for item in nova_lista:
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolyline(item[0]))
        feature.setAttributes(item[1])
        writer.addFeature(feature)

    del writer
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(3)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)