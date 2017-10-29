"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-25
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

# Fazer linha de talvegue
##1. Linha de Talvegue=name
##LF6) Terreno=group
##MDE=raster
##Linha_de_Referencia=vector
##Distancia_entre_Secoes=number 20.0
##Tamanho_das_Secoes=number 300.0
##Distancia_entre_Pontos_nas_Secoes=number 30.0
##Tipo_de_Interpolacao=selection Bicubica;Bilinear;Vizinho Mais Proximo
##Cotas_Minimas=output vector
##Linha_de_Talvegue=output vector

linha = Linha_de_Referencia
saida_ponto = Cotas_Minimas
saida_linha = Linha_de_Talvegue
distSec = Distancia_entre_Secoes
tamSec = Tamanho_das_Secoes
distPnts = Distancia_entre_Pontos_nas_Secoes
interpolacao = ['bicubic', 'bilinear', 'nearest']
metodo = interpolacao[Tipo_de_Interpolacao]

from qgis.core import *
from PyQt4.QtCore import *
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from math import floor, ceil, pow
from numpy import array, arange, mat
from numpy.linalg import norm
import processing
import time

# Funcao de Interpolacao
def Interpolar(X, Y, MDE, origem, resol_X, resol_Y, metodo):
    if metodo == 'nearest':
        linha = round((origem[1]-Y)/resol_Y - 0.5)
        coluna = round((X - origem[0])/resol_X - 0.5)
        return float(MDE[linha][coluna])
    elif metodo == 'bilinear':
        nlin = len(MDE)
        ncol = len(MDE[0])
        I = (origem[1]-Y)/resol_Y - 0.5
        J = (X - origem[0])/resol_X - 0.5
        di = I - floor(I)
        dj = J - floor(J)
        if I<0:
            I=0
        if I>nlin-1:
            I=nlin-1
        if J<0:
            J=0
        if J>ncol-1:
            J=ncol-1
        Z = (1-di)*(1-dj)*MDE[floor(I)][floor(J)] + (1-dj)*di*MDE[ceil(I)][floor(J)] + (1-di)*dj*MDE[floor(I)][ceil(J)] + di*dj*MDE[ceil(I)][ceil(J)]
        return float(Z)
    elif metodo == 'bicubic':
        nlin = len(MDE)
        ncol = len(MDE[0])
        I = (origem[1]-Y)/resol_Y - 0.5
        J = (X - origem[0])/resol_X - 0.5
        di = I - floor(I)
        dj = J - floor(J)
        I=floor(I)
        J=floor(J)
        if I<2:
            I=2
        if I>nlin-3:
            I=nlin-3
        if J<2:
            J=2
        if J>ncol-3:
            J=ncol-3
        MatrInv = (mat([[-1, 1, -1, 1], [0, 0, 0, 1], [1, 1, 1, 1], [8, 4, 2, 1]])).I # < Jogar para fora da funcao
        MAT  = mat([[MDE[I-1, J-1],   MDE[I-1, J],   MDE[I-1, J+1],  MDE[I-2, J+2]],
                             [MDE[I, J-1],      MDE[I, J],      MDE[I, J+1],      MDE[I, J+2]],
                             [MDE[I+1, J-1],  MDE[I+1, J], MDE[I+1, J+1], MDE[I+1, J+2]],
                             [MDE[I+2, J-1],  MDE[I+2, J], MDE[I+2, J+1], MDE[I+2, J+2]]])
        coef = MatrInv*MAT.transpose()
        # Horizontal
        pi = coef[0,:]*pow(dj,3)+coef[1,:]*pow(dj,2)+coef[2,:]*dj+coef[3,:]
        # Vertical
        coef2 = MatrInv*pi.transpose()
        pj = coef2[0]*pow(di,3)+coef2[1]*pow(di,2)+coef2[2]*di+coef2[3]
        return float(pj)

# Abrir Raster layer como array
import gdal
from osgeo import osr
image = gdal.Open(MDE)
band = image.GetRasterBand(1).ReadAsArray()
prj=image.GetProjection()
geotransform = image.GetGeoTransform()
distance = QgsDistanceArea()
# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
image=None # Close image
# Origem e resolucao da imagem
origem = (geotransform[0], geotransform[3])
resol_X = abs(geotransform[1])
resol_Y = abs(geotransform[5])

# Abrir Shapefile
layer = processing.getObject(linha)

# Conferir CRS
crs = QgsCoordinateReferenceSystem()
crs.createFromWkt(prj)
# Verificar se as duas camadas tem o mesmo CRS e sao projetadas
if crs != layer.crs() or layer.crs().geographicFlag():
    progress.setInfo('<b>Problema(s) durante a execucao da ferramenta.</b><br/>')
    progress.setInfo('<b>Verifique se as camadas tem o mesmo SRC e ambas sao projetadas.</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Erro', "Problema(s) com os parametros de entrada.", level=QgsMessageBar.CRITICAL, duration=5) 
else:
    # Criar Camada de Saida de Pontos
    fields = QgsFields()
    fields.append(QgsField('ID', QVariant.Int))
    fields.append(QgsField('cota', QVariant.Double, "numeric", 14, 3))
    SRC = layer.crs()
    encoding = u'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(saida_ponto, encoding, fields, QGis.WKBPoint, SRC, formato)
    feature = QgsFeature(fields)
    
    # Criar Camada de Saida de Linhas
    fields = QgsFields()
    fields.append(QgsField('ID', QVariant.Int))
    SRC = layer.crs()
    encoding = u'utf-8'
    formato = 'ESRI Shapefile'
    writer2 = QgsVectorFileWriter(saida_linha, encoding, fields, QGis.WKBLineString, SRC, formato)
    fet = QgsFeature(fields)
    
    ID = 1
    for feat in layer.getFeatures():
        geom = feat.geometry()
        comprimento = geom.length()
        coord = geom.asPolyline()
        LIST_COORD = []
        # Criar lista de pontos e distancias
        ListaDist = [0]
        soma = 0
        for i in range(len(coord)-1):
            point1 = coord[i]
            point2 = coord[i+1]
            m = distance.measureLine(point1, point2)
            soma += m
            ListaDist += [soma]
        # Numero de Secoes e Nova Distancia
        NumSec = floor(comprimento/distSec)
        DistSecNova = comprimento/NumSec
        dist = arange(0, comprimento+DistSecNova, DistSecNova)
        # Algoritmo para pegar secoes transversais
        cont = 0
        for k in range(len(coord)-1):
            while ListaDist[k] <= dist[cont] and dist[cont] < ListaDist[k+1]:
                point1 = array([coord[k].x(), coord[k].y()])
                point2 = array([coord[k+1].x(), coord[k+1].y()])
                vetor = point2 - point1
                vetor/= norm(vetor)
                MultDist = dist[cont]-ListaDist[k]
                centro = point1 + vetor*MultDist
                # Aqui pode ser criado o perfil do terreno...
                # Pontos extremos de cada secao
                p1 = centro + array([vetor[1], -1*vetor[0]])*tamSec/2.0
                p2 = centro + array([-1*vetor[1], vetor[0]])*tamSec/2.0
                LIST_COORD += [[QgsPoint(float(p1[0]), float(p1[1])), QgsPoint(float(p2[0]), float(p2[1]))]]
                cont +=1
                if cont == NumSec +1:
                    break
            if cont == NumSec +1:
                break
        # Ultima secao
        point1 = array([coord[-2].x(), coord[-2].y()])
        point2 = array([coord[-1].x(), coord[-1].y()])
        vetor = point2 - point1
        vetor/= norm(vetor)
        centro = array([coord[-1].x(), coord[-1].y()])
        p1 = centro + array([vetor[1], -1*vetor[0]])*tamSec/2.0
        p2 = centro + array([-1*vetor[1], vetor[0]])*tamSec/2.0
        LIST_COORD += [[QgsPoint(float(p1[0]), float(p1[1])), QgsPoint(float(p2[0]), float(p2[1]))]]
        
        # Para cada Secao Transversal pegar o ponto mais baixo
        TALVEGUE =[]
        for coord in LIST_COORD:
            # Numero de Pontos e Nova Distancia
            NumPnts = floor(tamSec/distPnts)
            DistPnts = tamSec/NumPnts
            dist = arange(0, tamSec+DistPnts, DistPnts)
            # Algoritmo para pegar Pontos da secao
            point1 = array([coord[0].x(), coord[0].y()])
            point2 = array([coord[-1].x(), coord[-1].y()])
            vetor = point2 - point1
            vetor/= norm(vetor)
            LIST_PNTS = []
            for MultDist in dist:
                ponto = point1 + vetor*MultDist
                LIST_PNTS += [(float(ponto[0]), float(ponto[1]))]
            # Identificar Minimo na Lista de Pontos
            LIST_Z = []
            for pnt in LIST_PNTS:
                X = pnt[0]
                Y = pnt[1]
                Z = Interpolar(X, Y, band, origem, resol_X, resol_Y, metodo)
                LIST_Z += [Z]
            # Verificar se ha apenas um minimo na secao
            Minimo = (array(LIST_Z)).min()
            cont_Min = (array(LIST_Z) == Minimo).sum()
            if cont_Min == 1:
                indice = LIST_Z.index(Minimo)
                pnt = QgsPoint(LIST_PNTS[indice][0],LIST_PNTS[indice][1])
                geom = QgsGeometry.fromPoint(pnt)
                feature.setGeometry(geom)
                feature.setAttributes([ID, float(Minimo)])
                ID +=1
                writer.addFeature(feature)
                TALVEGUE += [pnt]
        # Salvando a feicao do talvegue
        geom = QgsGeometry.fromPolyline(TALVEGUE)
        fet.setGeometry(geom)
        fet.setAttributes([feat.id()])
        writer2.addFeature(fet)

    del writer, writer2
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)