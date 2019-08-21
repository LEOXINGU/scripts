"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2019-08-19
        copyright            : (C) 2019 by Leandro Franca - Cartographic Engineer
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
# CARREGAR RASTER
##7. CARREGAR RASTER=name
##LF01) PostGIS=group
##Raster=raster
##database=string BDGeo
##schema=string public
##table=string tabela
##Versao_do_PostgreSQL=selection 10;9.3;9.4;9.5;9.6
##Usuario=string postgres
##Host=string localhost

# Inputs
host = str(Host)
lista = [10,9.3,9.4,9.5,9.6]
version = str(lista[Versao_do_PostgreSQL])

import os
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import gdal
from osgeo import osr

# Pegar SRC do Raster de entrada
image = gdal.Open(Raster)
prj=image.GetProjection()
crs = QgsCoordinateReferenceSystem()
crs.createFromWkt(prj)
SRID = (crs.authid()).split(':')[-1]

local = 'C:/Program Files/PostgreSQL/'+version+'/bin'
sentinela = False
if os.path.isdir(local):
    os.chdir(local)
    sentinela = True
else:
    local = 'C:/Program Files (x86)/PostgreSQL/'+version+'/bin'
    if os.path.isdir(local):
        os.chdir(local)
        sentinela = True
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        progress.setInfo('<b>Verifique se a versao do PostgreSQL foi definida corretamente.</b><br/>')
        time.sleep(8)
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=5) 

if sentinela:
    arqSQL = 'C:/Users/Public/raster2postgis.sql'
    comando = 'raster2pgsql -s ' + SRID + ' -I -C -M ' + Raster + ' -F -t 100x100 ' +schema+ '.'+ table + ' > '+ arqSQL
    progress.setInfo('<b>Raster para SQL...</b><br/>')
    result = os.system(comando)
    os.remove(arqSQL)
    if result==0:
        progress.setInfo('<b>Carregando raster no BDGeo...</b><br/>')
        comando2 = 'psql -d ' +database+' -U '+Usuario+' -h '+host+' -p 5432 -f ' + arqSQL
        result2 = os.system(comando2)
        if result2 == 0:
            progress.setInfo('<b>Operacao concluida com sucesso!</b><br/><br/>')
            progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
            time.sleep(4)
            iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
        else:
            progress.setInfo('<b>Problema(s) durante a execucao da operacao.</b><br/>')
            progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
            time.sleep(8)
            iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=10) 
    else:
        progress.setInfo('<b>Problema(s) durante a execucao da operacao.</b><br/>')
        progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
        time.sleep(8)
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=10) 
