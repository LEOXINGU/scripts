"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-09-25
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
# BACKUP DE SERVIDOR
##6. BACKUP DE SERVIDOR=name
##LF01) PostGIS=group
##Host=string localhost
##Versao_do_PostgreSQL=selection 9.5;9.3;9.4;9.6
##Arquivo_de_backup=output file
##Usuario=string postgres

# Inputs
host = str(Host)
lista = [9.5,9.3,9.4,9.6]
version = str(lista[Versao_do_PostgreSQL])
saida = Arquivo_de_backup
if saida[-4:] != '.sql':
    saida += '.sql'

import os
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

local = 'C:/Program Files/PostgreSQL/'+version+'/bin'
sentinela = False
if os.path.isdir(local):
    os.chdir(local)
    sentinela = True
else:
    local = 'C:\Program Files (x86)/PostgreSQL/'+version+'/bin'
    if os.path.isdir(local):
        os.chdir(local)
        sentinela = True
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        progress.setInfo('<b>Verifique se a versao do PostgreSQL foi definida corretamente.</b><br/>')
        time.sleep(8)
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=5) 

if 'backup.file' in saida:
    sentinela = False
    progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
    progress.setInfo('<b>Verifique se o nome do banco de dados foi escrito corretamente.</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=5)
   
if sentinela:
    comando = 'pg_dumpall -h %s -p 5432 -U ' %host  +Usuario+ ' -v -f "%s"' %saida
    progress.setInfo('<b>Realizando backup do servidor...</b><br/>')
    result = os.system(comando)
    if result==0:
        progress.setInfo('<b>Operacao concluida com sucesso!</b><br/><br/>')
        progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
        time.sleep(4)
        iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
        time.sleep(8)
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do backup.", level=QgsMessageBar.CRITICAL, duration=10) 
