"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-16
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
# Transladar Raster
##LF05) Raster=group
##Transladar Raster=name
##Camada_Raster=raster
##Ponto_Inicial=string
##Ponto_Final=string
##Saida=output raster

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time
from numpy import array
import numpy, gdal
from osgeo import osr
from osgeo import gdal_array

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Validacao dos dados de entrada
def Validacao(Vetor_XY):
    problema = False
    deslc = Vetor_XY.replace('  ', ' ').replace(', ', ',').replace(' ', ',').split(',')
    # Deve-ser ter 2 numeros para deslocamento
    if len(deslc) ==2 and isfloat(deslc[0]) and isfloat(deslc[1]):
        deslc = [float(deslc[0]), float(deslc[1])]
    else:
        problema = True
    return (problema, deslc)

problema = Validacao(Ponto_Inicial)[0] and Validacao(Ponto_Final)[0]
if not problema:
    Pi = array(Validacao(Ponto_Inicial)[1])
    Pf = array(Validacao(Ponto_Final)[1])
    vetor = Pf-Pi
    progress.setInfo('Parametros de deslocamento: dX = %.5f e dY = %.5f<br/>' %(vetor[0], vetor[1]))
    # Abrir imagem 
    image = gdal.Open(Camada_Raster)
    n_bands = image.RasterCount
    matrizes = []
    CTs = []
    for i in range(1, n_bands+1):
        banda = image.GetRasterBand(i)
        matrizes += [banda.ReadAsArray()]
        CTs += [banda.GetColorTable()]

    # Tipo de dado
    GDT = gdal_array.NumericTypeCodeToGDALTypeCode(matrizes[0].dtype)
    # Dados de SRC
    prj=image.GetProjection()
    geotransform = image.GetGeoTransform()
    # Create CRS object
    CRS=osr.SpatialReference(wkt=prj)
    # Number of rows and columns
    cols = image.RasterXSize # Number of columns
    rows = image.RasterYSize # Number of rows
    image=None # Close image

    # Novo geotransform
    g = geotransform
    geotransform = (float(vetor[0])+g[0], g[1], g[2], float(vetor[0])+g[3], g[4], g[5])

    # Create RGB image
    RGB = gdal.GetDriverByName('GTiff').Create(Saida, cols, rows, n_bands, GDT)
    RGB.SetGeoTransform(geotransform)    # specify coords
    RGB.SetProjection(CRS.ExportToWkt()) # export coords to file
    for i, matriz in enumerate(matrizes):
        outband = RGB.GetRasterBand(i+1)
        outband.WriteArray(matriz)   # write band to the raster
        if CTs[i]:
            CT = CTs[i]
            outband.SetColorTable(CT)
    RGB.FlushCache()                     # write to disk
    RGB = None                           # save, close
    CRS = None

    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(3)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)
else:
    progress.setInfo('<b>Problema(s) durante a execucao do processo.</b><br/>')
    progress.setInfo('<b>lista: %s </b><br/>' %(str(Ponto_Inicial)))
    progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do processo.", level=QgsMessageBar.CRITICAL, duration=7) 