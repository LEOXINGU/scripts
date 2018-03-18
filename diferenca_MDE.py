"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-01-26
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
# Diferenca entre MDE
##Diferenca entre MDE=name
##LF07) Qualidade=group
##MDE_Avaliado=raster
##MDE_de_Referencia=raster
##Tipo_de_Interpolacao=selection Bicubica;Bilinear;Vizinho Mais Proximo
##Pixel_Nulo=number -1000
##Diferenca=output raster

interpolacao = ['bicubic', 'bilinear', 'nearest']
metodo = interpolacao[Tipo_de_Interpolacao]
MDE = MDE_Avaliado
nuloDifer = Pixel_Nulo

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from numpy import sqrt, array, mat, zeros
from math import ceil, floor
from osgeo import gdal_array

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
        

# Abrir camada raster de teste
import gdal
from osgeo import osr
image = gdal.Open(MDE)
band = image.GetRasterBand(1).ReadAsArray()
NULO = image.GetRasterBand(1).GetNoDataValue()
if NULO == None:
    NULO =-1e6
prj=image.GetProjection()
# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
# Origem e resolucao da imagem
ulx, xres, xskew, uly, yskew, yres  = image.GetGeoTransform()
origem = (ulx, uly)
resol_X = abs(xres)
resol_Y = abs(yres)
prj=image.GetProjection()
n_bands = image.RasterCount
geotransform  = image.GetGeoTransform()
CRS=osr.SpatialReference(wkt=prj)
image=None # Fechar imagem

# Abrir camada de referencia
image = gdal.Open(MDE_de_Referencia)
bandRef = image.GetRasterBand(1).ReadAsArray()
nuloRef = image.GetRasterBand(1).GetNoDataValue()
if nuloRef == None:
    nuloRef =-1e6
prjRef=image.GetProjection()
# Number of rows and columns
colsRef = image.RasterXSize # Number of columns
rowsRef = image.RasterYSize # Number of rows
# Origem e resolucao da imagem
ulx, xres, xskew, uly, yskew, yres  = image.GetGeoTransform()
origemRef = (ulx, uly)
resol_XRef = abs(xres)
resol_YRef = abs(yres)
lrx = ulx + (colsRef * xres)
lry = uly + (rowsRef * yres)
bbox = [ulx, lrx, lry, uly]
image=None # Fechar imagem

#Criar Raster de Saida
DIFER = zeros([rows,cols], dtype='f')

# Verificacoes
if False: #prj != prjRef:
    iface.messageBar().pushMessage(u'Erro', "Problema(s) com os parametros de entrada.", level=QgsMessageBar.CRITICAL, duration=5) 
    progress.setInfo('<b><font  color="#ff0000">Erro nos parametros de entrada.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000">Verifique se os MDE tem o mesmo SRC.</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Situacao', "Problema com os dados de entrada!", level=QgsMessageBar.WARNING, duration=8)

else:
    progress.setInfo('<b>Iniciando processamento...</b><br/>')
    cont = 0
    valor2=0
    valor3=-1
    for lin in range(rows):
        for col in range(cols):
            # Determinar a coordenada do pixel da cota
            X = origem[0] + resol_X*(col+0.5)
            Y = origem[1] - resol_Y*(lin+0.5)
            cota = band[lin][col]
            if cota!=NULO:
                if bbox[0]<X and bbox[1]>X and bbox[2]<Y and bbox[3]>Y:
                   cotaRef = Interpolar(X, Y, bandRef, origemRef, resol_XRef, resol_YRef, metodo, nuloRef)
                   if cotaRef != nuloRef:
                        difer = cota-cotaRef
                        DIFER[lin][col]=difer
                   else:
                       DIFER[lin][col]=nuloDifer
                else:
                    DIFER[lin][col]=nuloDifer
            else:
                DIFER[lin][col]=nuloDifer
        cont +=1
        valor = int(100*float(cont)/float(rowsRef))
        if valor==valor2 and valor!=valor3:
            valor2 +=1
            valor3 = valor
            progress.setPercentage(valor)
    
    del band, bandRef
    
    # Gerando Raster da Diferenca
    GDT = gdal_array.NumericTypeCodeToGDALTypeCode(DIFER.dtype)
    RASTER = gdal.GetDriverByName('GTiff').Create(Diferenca, cols, rows, n_bands, GDT)
    RASTER.SetGeoTransform(geotransform)    # specify coords
    RASTER.SetProjection(CRS.ExportToWkt()) # export coords to file
    outband = RASTER.GetRasterBand(1)
    outband.WriteArray(DIFER)   # write band to the raster
    outband.SetNoDataValue(nuloDifer)
    RASTER.FlushCache()                     # write to disk
    RASTER = None                           # save, close
    RASTER = None
    
    
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)