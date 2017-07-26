"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-03-31
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
# Consertar Linhas
##1. Mergear na Direcao=name
##arquivo=vector
##tolerancia=number 10
##saida=output vector
##LF4) Vetor=group
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
progress.setInfo('<b>Iniciando processamento...</b><br/>')
# Funcao que pega ponto incial e final e os seus angulos
def pontos_ang(geom):
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
    else:
        print 'Feicao nao prevista!'
    return [[coord, coord[0], coord[-1], ang_ini, ang_fim]]

# Criar lista com as geometrias
lista = []
for feature in linhas.getFeatures():
        id = feature.id()
        geom = feature.geometry()
        lista += pontos_ang(geom)

# Funcao para dar a direcao oposta
def contraAz(x):
    if x<=0:
        return x+180
    else:
        return x-180

# Criar uma nova lista com as feicoes finais mergeadas
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

# Mergear os que se tocam e tem mesma direcao
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
        for j in range(i+1,tam):
            # Ponto inicial e final da feicao B
            coord_B = lista[j][0]
            P_ini_B = lista[j][1]
            P_fim_B = lista[j][2]
            ang_ini_B = lista[j][3]
            ang_fim_B = lista[j][4]
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
            if new_geom.isMultipart():
                nova_lista += [coord_A, coord_B]
                del lista[i], lista[j-1]
                break
            else:
                del lista[i], lista[j-1]
                lista = pontos_ang(new_geom)+lista
                break
        if not(mergeou):
            # Tirar a geometria que nao se conecta com nada da lista
            nova_lista += [lista[i][0]]
            del lista[i]
            break
    if len(lista)==1:
        nova_lista += [lista[0][0]]
        
# Criando o shapefile de saida
progress.setInfo('<b>Criando shapefile de saida...</b><br/>')
path_name = output_name
encoding = 'utf-8'
formato = 'ESRI Shapefile'
crs = linhas.crs()
# Criar campos
fields = QgsFields()
fields.append(QgsField('ID', QVariant.Int))

writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBLineString, crs, formato)

for index, coord in enumerate(nova_lista):
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPolyline(coord))
    feature.setAttributes([index])
    writer.addFeature(feature)

del writer
progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>3 CGEO</b><br/>')
progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
time.sleep(3)