"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-05-29
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
##2. Fotos Geo=name
##Escolha_uma_pasta_de_imagens=optional folder
##Shapefile_de_Fotos=output vector
##LF3) GPS, Fotos e Midias=group

pasta = str(Escolha_uma_pasta_de_imagens)
import os
os.chdir(str(pasta))
lista = os.listdir(pasta)
tam = len(lista)
ExistePasta = os.path.isdir('Nao GEO')
if not ExistePasta:
    os.mkdir('Nao GEO')

import PIL.Image, PIL.ExifTags
import datetime
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
from qgis.utils import iface
from qgis.gui import QgsMessageBar
import time
import shutil

# Funcao para transformar os dados do EXIF em coordenadas em graus decimais
def coordenadas(exif):
    ref_lat = exif['GPSInfo'][1][0]
    ref_lon = exif['GPSInfo'][3][0]
    sinal_lat, sinal_lon = 0, 0
    if ref_lat == 'S':
        sinal_lat = -1
    elif ref_lat == 'N':
        sinal_lat = 1
    if ref_lon == 'W':
        sinal_lon = -1
    elif ref_lon == 'E':
        sinal_lon = 1
    grausLat,grausLon = exif['GPSInfo'][2][0][0], exif['GPSInfo'][4][0][0]
    minLat, minLon = exif['GPSInfo'][2][1][0], exif['GPSInfo'][4][1][0]
    segLat = exif['GPSInfo'][2][2][0]/float(exif['GPSInfo'][2][2][1])
    segLon = exif['GPSInfo'][4][2][0]/float(exif['GPSInfo'][4][2][1])
    if sinal_lat!=0 and sinal_lon!=0:
        lat = sinal_lat*(float(grausLat)+minLat/60.0+segLat/3600.0)
        lon = sinal_lon*(float(grausLon)+minLon/60.0+segLon/3600.0)
    return lat, lon

# Funcao para gerar o padrao data-hora
def data_hora(texto):
    data_hora = texto.replace(' ',':')
    data_hora = data_hora.split(':')
    ano = int(data_hora[0])
    mes = int(data_hora[1])
    dia = int(data_hora[2])
    hora = int(data_hora[3])
    minuto = int(data_hora[4])
    segundo = int(data_hora[5])
    data_hora = unicode(datetime.datetime(ano, mes, dia, hora, minuto, segundo))
    return data_hora

# Criar campos
fields = QgsFields()
fields.append(QgsField('file_name', QVariant.String))
fields.append(QgsField('azimuth', QVariant.Int))
fields.append(QgsField('date_time', QVariant.String))
# Criando o shapefile
path_name = Shapefile_de_Fotos
encoding = 'utf-8'
formato = 'ESRI Shapefile'
crs_epsg =4326
crs = QgsCoordinateReferenceSystem()
crs.createFromSrid(crs_epsg)
writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBPoint, crs, formato)

# Abrindo todas as imagens e salvando suas informacoes "Geo" em um shapefile
feature = QgsFeature()
for index, arquivo in enumerate(lista):
    if (arquivo[-3:]).lower() == 'jpg':
        img = PIL.Image.open(arquivo)
        if img._getexif():
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
        else:
            exif = {}
        lon, lat = 0, 0
        Az = None
        date_time = None
        if 'GPSInfo' in exif:
            lat, lon = coordenadas(exif)
        if 17 in exif['GPSInfo']:
            Az = exif['GPSInfo'][17]
        if 'DateTimeOriginal' in exif:
            date_time = data_hora(exif['DateTimeOriginal'])
        elif 'DateTime' in exif:
            date_time = data_hora(exif['DateTimeOriginal'])
        if abs(lon)>0.1:
            feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
            feature.setAttributes([arquivo, Az, date_time])
            writer.addFeature(feature)
        else:
            progress.setInfo('A imagem %s nao eh GEO!<br/>' %arquivo)
            if not ExistePasta:
                shutil.copy2(pasta+'\\'+arquivo, pasta+'\\Nao GEO\\'+arquivo)
    progress.setPercentage(int((index/float(tam))*100))

del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)