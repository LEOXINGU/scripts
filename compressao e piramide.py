"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-04-13
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
# COMPRESSAO
##Compressao=name
##LF05) Raster=group
##Entrada=raster
##Saida=output raster
##Tipo_de_Compressao=selection JPEG_PHOTOMETRIC;JPEG;Photometric
##Qualidade_JPEG=selection 75%;65%;85%
##Criar_Piramides=boolean False

# Inputs
lista = ['JPEG_PHOTOMETRIC','JPEG', 'PHOTOMETRIC']
compress = lista[Tipo_de_Compressao]
lista = ['75%', '65%', '85%']
qualidade = lista[Qualidade_JPEG][0:2]

import os
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.core import *
import time
import qgis.utils
from qgis.utils import iface
#version = qgis.utils.QGis.QGIS_VERSION
#version = version.split('.')
#version = version[0]+'.'+version[1]
#path = 'C:/Program Files/QGIS '+ version+'/bin'
path = qgis.core.QgsApplication.applicationDirPath().encode("utf-8")
os.chdir(path)

if compress == 'JPEG_PHOTOMETRIC':
    comando = 'gdal_translate --config GDAL_NUM_THREADS ALL_CPUS -of GTiff -ot Byte -co PHOTOMETRIC=YCBCR -co TILED=YES -co COMPRESS=JPEG -co JPEG_QUALITY='+qualidade+' '+Entrada+' '+Saida
elif compress == 'JPEG':
    comando = 'gdal_translate --config GDAL_NUM_THREADS ALL_CPUS -of GTiff -ot Byte -co COMPRESS=JPEG -co JPEG_QUALITY='+qualidade+' '+Entrada+' '+Saida
elif compress == 'PHOTOMETRIC':
    comando = 'gdal_translate --config GDAL_NUM_THREADS ALL_CPUS -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR -co TILED=YES '+Entrada+' '+Saida

# Realizando a compressao
progress.setInfo('<b>Iniciando processo de Compressao da Imagem...</b><br/>')
result = os.system(comando)

# Gerando piramides
if Criar_Piramides and result==0:
    progress.setInfo('<b>Criando piramides...</b><br/>')
    comando = 'gdaladdo -ro --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL -r average '+ Saida + ' 2 4 8 16 32 64'
    result = os.system(comando)

if result==0:
    progress.setInfo('<b>Operacao concluida com sucesso!</b><br/><br/>')
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
    progress.setInfo('<b>3 CGEO</b><br/>')
    progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
    time.sleep(4)
else:
    progress.setInfo('<b>Problema(s) durante a execucao da compressao.</b><br/>')
    iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao da compressao.", level=QgsMessageBar.CRITICAL, duration=5) 
    progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
    time.sleep(8)
