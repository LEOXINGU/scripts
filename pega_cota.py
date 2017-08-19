"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-03-28
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
# Pega Cotas
##2. Pega cotas=name
##LF6) Terreno=group
##Modelo_Digital_de_Elevacao=raster
##Camada_de_Cotas=vector
##Campo_valor_da_cota=field Camada_de_Cotas
##Escala=selection 1:25.000;1:50.000;1:100.000;1:250.000

MDS = Modelo_Digital_de_Elevacao
path_name = Camada_de_Cotas
campo = Campo_valor_da_cota
equid = [10, 20, 50, 100]
equid = equid[Escala]

from qgis.core import *
from PyQt4.QtCore import *
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from math import floor, ceil

# Abrir Raster layer como array
import gdal
from osgeo import osr
image = gdal.Open(MDS)
band = image.GetRasterBand(1).ReadAsArray()
prj=image.GetProjection()
geotransform = image.GetGeoTransform()

# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
image=None # Close image
# Origem e resolucao da imagem
origem = (geotransform[0], geotransform[3])
resol = abs(geotransform[1])

# Abrir Shapefile
vetor = QgsVectorLayer(path_name, "", "ogr")
indice = vetor.pendingFields().fieldNameIndex(campo)
myDataProvider = vetor.dataProvider()

# Conferir CRS
crs = QgsCoordinateReferenceSystem()
crs.createFromWkt(prj)
# Verificar se as duas camadas tem o mesmo CRS
if crs != vetor.crs():
    iface.messageBar().pushMessage(u'Erro', "Raster e camada de cotas devem ter o mesmo SRC", level=QgsMessageBar.CRITICAL, duration=10) #  PODE SER TAMBEM :CRITICAL OU INFO
else:
    # Varrer shapefile e verificar as feicoes que tem cota nula e preencher com o valor da cota
    for feat in vetor.getFeatures(QgsFeatureRequest()):
        att = feat.attributes()
        if att[indice] == None or att[indice] ==0:
            geom = feat.geometry()
            coord = geom.asPoint()
            X = coord[0]
            Y = coord[1]
            linha = round((origem[1]-Y)/resol - 0.5)
            coluna = round((X - origem[0])/resol - 0.5)
            # Arredondar cota
            cota = float(band[linha][coluna])
            if round(cota) % equid == 0:
                if cota < round(cota):
                    cota = floor(cota)
                else:
                    cota = ceil(cota)
            else:
                cota = round(cota)
            newColumnValueMap = {indice : cota} # Aqui pode entrar mais de um atributo
            newAttributesValuesMap = {feat.id() : newColumnValueMap}
            myDataProvider.changeAttributeValues(newAttributesValuesMap)

progress.setInfo('Cotas obtidas com sucesso!')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(4)
iface.messageBar().pushMessage(u'Informacao', "Cotas obtidas com sucesso", level=QgsMessageBar.INFO, duration=10) #  PODE SER TAMBEM :WARNING, CRITICAL OU INFO