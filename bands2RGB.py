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
##Bandas para RGB=name
##LF5) Raster=group
##Band_R=raster
##Band_G=raster
##Band_B=raster
##RGB_Output_image_file=output raster

import numpy, gdal
from osgeo import osr

# Open band R 
image = gdal.Open(Band_R)
bandR = image.GetRasterBand(1).ReadAsArray()
prj=image.GetProjection()
geotransform = image.GetGeoTransform()
# Open band G
image = gdal.Open(Band_G)
bandG = image.GetRasterBand(1).ReadAsArray()
# Open band B
image = gdal.Open(Band_B)
bandB = image.GetRasterBand(1).ReadAsArray()
# Create CRS object
CRS=osr.SpatialReference(wkt=prj)
# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
image=None # Close image

# Create RGB image
RGB = gdal.GetDriverByName('GTiff').Create(RGB_Output_image_file, cols, rows, 3, gdal.GDT_UInt16)
RGB.SetGeoTransform(geotransform)    # specify coords
RGB.SetProjection(CRS.ExportToWkt()) # export coords to file
RGB.GetRasterBand(1).WriteArray(bandR)   # write R band to the raster
RGB.GetRasterBand(2).WriteArray(bandG)   # write G band to the raster
RGB.GetRasterBand(3).WriteArray(bandB)   # write B band to the raster
RGB.FlushCache()                     # write to disk
RGB = None                           # save, close
CRS = None

progress.setInfo('<b><font  color="#ff0000">Suas altera&ccedil;&otilde;es ser&atilde;o salvas e seu Projeto QGIS ser&aacute; fechado em 9 segundos.</b><br/><br/>')
progress.setInfo('<b>Opera&ccedil;&atilde;o conclu&iacute;da!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
time.sleep(4)