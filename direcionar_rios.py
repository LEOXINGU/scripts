"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-05-19
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

# Direcionar Trecho de Drenagem
##5. Direcionar rios=name
##LF06) Terreno=group
##MDE=raster
##Trecho_de_drenagem=vector
##Tipo_de_Interpolacao=selection Bicubica;Bilinear;Vizinho Mais Proximo
##Linhas_Direcionadas=output vector

linha = Trecho_de_drenagem
saida_linha = Linhas_Direcionadas
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
def Interpolar(X, Y, MDE, origem, resol_X, resol_Y, metodo, nulo):
    if metodo == 'nearest':
        linha = int(round((origem[1]-Y)/resol_Y - 0.5))
        coluna = int(round((X - origem[0])/resol_X - 0.5))
        if MDE[linha][coluna] != nulo:
            return float(MDE[linha][coluna])
        else:
            return nulo
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
        if (MDE[int(floor(I)):int(ceil(I))+1, int(floor(J)):int(ceil(J))+1] == nulo).sum() == 0:
            Z = (1-di)*(1-dj)*MDE[int(floor(I))][int(floor(J))] + (1-dj)*di*MDE[int(ceil(I))][int(floor(J))] + (1-di)*dj*MDE[int(floor(I))][int(ceil(J))] + di*dj*MDE[int(ceil(I))][int(ceil(J))]
            return float(Z)
        else:
            return nulo
    elif metodo == 'bicubic':
        nlin = len(MDE)
        ncol = len(MDE[0])
        I = (origem[1]-Y)/resol_Y - 0.5
        J = (X - origem[0])/resol_X - 0.5
        di = I - floor(I)
        dj = J - floor(J)
        I=int(floor(I))
        J=int(floor(J))
        if I<2:
            I=2
        if I>nlin-3:
            I=nlin-3
        if J<2:
            J=2
        if J>ncol-3:
            J=ncol-3
        if (MDE[I-1:I+3, J-1:J+3] == nulo).sum() == 0:
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
        else:
            return nulo

# Abrir Raster layer como array
import gdal
from osgeo import osr
image = gdal.Open(MDE)
band = image.GetRasterBand(1).ReadAsArray()
nulo = image.GetRasterBand(1).GetNoDataValue()
if nulo == None:
    nulo =-1e6
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
    # Criar Camada de Saida
    SRC = layer.crs()
    fields = layer.pendingFields()
    encoding = u'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(saida_linha, encoding, fields, QGis.WKBLineString, SRC, formato)
    feature = QgsFeature(fields)
    
    for feat in layer.getFeatures():
        geom = feat.geometry()
        att = feat.attributes()
        coord = geom.asPolyline()
        if coord:
            PM = coord[0]
            PJ = coord[-1]
            cotaM = Interpolar(PM[0], PM[1], band, origem, resol_X, resol_Y, metodo, nulo)
            cotaJ = Interpolar(PJ[0], PJ[1], band, origem, resol_X, resol_Y, metodo, nulo)
            if cotaM < cotaJ:
                coord = coord[::-1]
            feature.setGeometry(QgsGeometry.fromPolyline(coord))
            feature.setAttributes(att)
            writer.addFeature(feature)
        else:
            coord = geom.asMultiPolyline()
            for item in coord:
                PM = item[0]
                PJ = item[-1]
                cotaM = Interpolar(PM[0], PM[1], band, origem, resol_X, resol_Y, metodo, nulo)
                cotaJ = Interpolar(PJ[0], PJ[1], band, origem, resol_X, resol_Y, metodo, nulo)
                if cotaM < cotaJ:
                    item = item[::-1]
                feature.setGeometry(QgsGeometry.fromPolyline(item))
                feature.setAttributes(att)
                writer.addFeature(feature)

    del writer
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)