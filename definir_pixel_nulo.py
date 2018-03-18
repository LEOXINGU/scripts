"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-01-25
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
# Definir pixels nulos de um MDE
##LF05) Raster=group
##Definir Nulos de MDE=name
##Raster_de_entrada=raster
##Valor_Minimo=number 350
##Valor_Maximo=number 950
##Pixel_Nulo=number -1000
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

MIN = Valor_Minimo
MAX = Valor_Maximo

if MAX > MIN:
    image = gdal.Open(Raster_de_entrada)
    band = image.GetRasterBand(1).ReadAsArray()
    GDT = gdal_array.NumericTypeCodeToGDALTypeCode(band.dtype)
    prj=image.GetProjection()
    n_bands = image.RasterCount
    cols = image.RasterXSize # Number of columns
    rows = image.RasterYSize # Number of rows
    geotransform  = image.GetGeoTransform()
    image=None # Fechar imagem
    # Gerando banda corrigida
    new_band = ((band>=MIN)*(band<=MAX))*band + ((band<MIN)*(band>MAX))*Pixel_Nulo
    # Create CRS object
    CRS=osr.SpatialReference(wkt=prj)
    # Create DEM
    DEM = gdal.GetDriverByName('GTiff').Create(Saida, cols, rows, n_bands, GDT)
    DEM.SetGeoTransform(geotransform)    # specify coords
    DEM.SetProjection(CRS.ExportToWkt()) # export coords to file
    outband = DEM.GetRasterBand(1)
    outband.WriteArray(new_band)   # write band to the raster
    outband.SetNoDataValue(Pixel_Nulo)
    DEM.FlushCache()                     # write to disk
    DEM = None                           # save, close
    DEM = None

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