"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-04-28
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
##3. Gerador de Cotas=name
##LF06) Terreno=group
##MDT=raster
##Saida=output vector
##Escala=selection 1:25.000;1:50.000;1:100.000;1:250.000
MDS = MDT
path_name = Saida
equid = [10, 20, 50, 100]
equid = equid[Escala]

import processing
from qgis.core import *
from PyQt4.QtCore import *
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from math import floor, ceil

# Gerar curvas de nivel
progress.setInfo('<b>Etapa 1:</b> Geracao de Curvas de Nivel...<br/>')
output = processing.runalg('gdalogr:contour', MDS, int(floor(equid/3.0)), 'ELEV', None, None)
nome = output['OUTPUT_VECTOR']
vetor = QgsVectorLayer(nome, "CN", "ogr")

# Verificar todas as feicoes e armazenar aquelas que sao anel linear
progress.setInfo('<b>Etapa 2:</b> Verificando curvas que contem cota...<br/>')
poligonos = []
pontos = []
for feature in vetor.getFeatures():
    geom = feature.geometry()
    coord = geom.asPolyline()
    if len(coord)>7 and coord[0] == coord[-1]:
        poligonos += [coord]
        pontos += [coord[0]]

# Verificando qual Curva esta dentro de outra
lista = []
for poligono in poligonos:
    polygon = QgsGeometry.fromPolygon([poligono])
    ponto_poly = poligono[0]
    sentinela = True
    for ponto in pontos:
        point = QgsGeometry.fromPoint(ponto)
        if polygon.contains(point) and ponto_poly != ponto:
            sentinela = False
            break
    if sentinela:
        lista += [poligono]

# Abrir Raster layer como array
progress.setInfo('<b>Etapa 3:</b> Abrindo Raster...<br/>')
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

# Criar Shapefile
# Criar campos
from PyQt4.QtCore import QVariant
fields = QgsFields()
fields.append(QgsField('Cota', QVariant.Double))
fields.append(QgsField('CotaRound', QVariant.Int))
fields.append(QgsField('Tipo', QVariant.Int))
crs = QgsCoordinateReferenceSystem()
crs.createFromWkt(prj)
# Criando o shapefile
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBPoint, crs, formato)

# Amostra de Raster por poligono
progress.setInfo('<b>Etapa 4:</b> Obtendo os valores das cotas...<br/>')
from matplotlib import path
import numpy as np

for poly in lista:
    caminho = []
    lin_min = 1e8
    col_min = 1e8
    lin_max = -1e8
    col_max = -1e8
    for ponto in poly:
        linha = (origem[1]-ponto.y())/resol
        if linha > lin_max:
            lin_max = linha
        if linha < lin_min:
            lin_min = linha
        coluna = (ponto.x() - origem[0])/resol
        if coluna > col_max:
            col_max = coluna
        if coluna < col_min:
            col_min = coluna
        caminho += [(linha, coluna)]
    p = path.Path(caminho)
    lin_min = np.floor(lin_min)
    lin_max = np.floor(lin_max)
    col_min = np.floor(col_min)
    col_max = np.floor(col_max)
    nx, ny = (lin_max-lin_min+1, col_max-col_min+1)
    lin = np.linspace(lin_min, lin_max, nx)
    col = np.linspace(col_min, col_max, ny)
    COL, LIN = np.meshgrid(col, lin)
    recorte = np.zeros((nx, ny), dtype=bool)
    for x in range(int(nx)):
        for y in range(int(ny)):
            pixel = (LIN[x][y]+0.5, COL[x][y]+0.5) # 0.5 eh o centro do pixel
            contem = p.contains_points([pixel])
            recorte[x][y] = contem[0]
    # Determinar qual(is) pixel(s) eh de maximo ou minimo
    recorte_img = band[lin_min:lin_max+1, col_min:col_max+1]
    if np.shape(recorte)==np.shape(recorte_img):
        produto = recorte*recorte_img
    else:
        recorte = recorte[0:np.shape(recorte_img)[0], 0:np.shape(recorte_img)[1]]
        produto = recorte*recorte_img
    min = 1e8
    max = -1e8
    tam = np.shape(produto)
    MIN = -1
    MAX = -1
    for x in range(tam[0]):
        for y in range(tam[1]):
            if produto[x][y] < min and produto[x][y]!=0:
                min = produto[x][y]
                MIN = (x,y)
            if produto[x][y] > max and produto[x][y]!=0:
                max = produto[x][y]
                MAX = (x,y)
    # Saber se eh depressao ou pico
    CN = feature.attributes()[1]
    TIPO = 0
    if np.sum(produto)/np.sum(recorte) > CN:
        TIPO = 1 # pico
        VALOR = max
        coord = MAX
    else:
        TIPO = -1 # depressao
        VALOR = min
        coord = MIN
    cota = float(VALOR)
    # Arredondar o valor da cota
    if round(cota) % equid == 0:
        if cota < round(cota):
            cota = floor(cota)
        else:
            cota = ceil(cota)
    else:
            cota = round(cota)
    # Determinar a coordenada do pixel da cota
    X = origem[0] + resol*(col_min+0.5+coord[1])
    Y = origem[1] - resol*(lin_min+0.5+coord[0])
    # Criar feicao
    feicao = QgsFeature()
    feicao.setGeometry(QgsGeometry.fromPoint(QgsPoint(X,Y)))
    feicao.setAttributes([cota, int(cota), TIPO])
    writer.addFeature(feicao)
    
del writer

progress.setInfo('<b>Cotas geradas com sucesso!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Informacao', "Cotas geradas com sucesso", level=QgsMessageBar.INFO, duration=10) #  PODE SER TAMBEM :WARNING, CRITICAL OU INFO