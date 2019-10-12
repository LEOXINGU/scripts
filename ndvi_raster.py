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
##NDVI=name
##LF05) Raster=group
##Band_R=raster
##Band_NIR=raster
##NDVI_Raster=output raster

import numpy, gdal
from osgeo import osr
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

# Open band R 
image = gdal.Open(Band_R)
bandR = image.GetRasterBand(1).ReadAsArray()
prj=image.GetProjection()
geotransform = image.GetGeoTransform()
# Open band G
image = gdal.Open(Band_NIR)
bandNIR = image.GetRasterBand(1).ReadAsArray()
# Create CRS object
CRS=osr.SpatialReference(wkt=prj)
# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
image=None # Close image

# Calculo do NDVI
R = bandR.astype('float')
NIR = bandNIR.astype('float')
NDVI = (NIR - R)/(NIR + R)

# Create RGB image
nova_imagem = gdal.GetDriverByName('GTiff').Create(NDVI_Raster, cols, rows, 1, gdal.GDT_Float32)
nova_imagem.SetGeoTransform(geotransform)    # specify coords
nova_imagem.SetProjection(CRS.ExportToWkt()) # export coords to file
nova_imagem.GetRasterBand(1).WriteArray(NDVI)   # write R band to the raster

nova_imagem.FlushCache()                     # write to disk
nova_imagem = None                           # save, close
CRS = None

progress.setInfo('<b>Opera&ccedil;&atilde;o conclu&iacute;da!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
time.sleep(4)